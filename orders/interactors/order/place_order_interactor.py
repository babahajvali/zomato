from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional

from django.db import transaction
from django.utils import timezone

from orders.adapter.account import AccountAdapter
from orders.adapter.dtos import CartItemDTO
from orders.adapter.restaurant import RestaurantAdapter
from orders.constants.constants import TAX_PERCENTAGE
from orders.constants.enums import PromoCodeType, OrderStatus
from orders.exception.custom_exceptions import (
    PromoCodeMaximumUsed,
    PromoCodeNotEligible,
    DeliveryNotAvailableForAddress,
    AddressNotFound,
    RestaurantNotOpenNow,
    RestaurantClosed,
    EmptyCartItemsFound,
    PromoCodeNotYetValid,
    PromoCodeExpired,
    CustomerCartNotFound,
)
from orders.interactors.dtos import (
    PlaceOrderDTO,
    OrderDTO,
    CreateOrderDTO,
    CreateOrderItemDTO,
    PromoCodeDTO,
    OrderSummaryDTO,
    OrderItemSummaryDTO,
)
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)
from orders.mixin.promocode_mixin import PromoCodeMixin
from utils.redis_util import redis_lock

REDIS_LOCK_TIMEOUT = 30


class PlaceOrderInteractor(PromoCodeMixin):
    def __init__(
        self,
        promo_code_storage: PromoCodeStorageInterface,
        order_storage: OrderStorageInterface,
    ):
        super().__init__(promo_code_storage=promo_code_storage)
        self.promo_code_storage = promo_code_storage
        self.order_storage = order_storage
        self.account_adapter = AccountAdapter()
        self.restaurant_adapter = RestaurantAdapter()

    def place_order(self, order_data: PlaceOrderDTO) -> OrderSummaryDTO:

        delivery_fee = self._validate_address_and_get_delivery_fee(
            address_id=order_data.address_id,
            restaurant_id=order_data.restaurant_id,
        )

        self._validate_restaurant_timing(restaurant_id=order_data.restaurant_id)
        with redis_lock(f"order:{order_data.customer_id}", timeout=REDIS_LOCK_TIMEOUT):
            cart_id = self._get_validated_cart_id(customer_id=order_data.customer_id)
            cart_items = self._get_validated_cart_items(cart_id=cart_id)
            items_total = self._calculate_items_total(cart_items=cart_items)

            if order_data.promo_code_id:
                self._validate_promo_code_existence_and_eligibility(
                    promo_code_id=order_data.promo_code_id,
                    items_total=items_total,
                )

            return self._place_order_with_locks(
                order_data=order_data,
                cart_items=cart_items,
                cart_id=cart_id,
                items_total=items_total,
                delivery_fee=delivery_fee,
            )

    def _place_order_with_locks(
        self,
        order_data: PlaceOrderDTO,
        cart_items: List[CartItemDTO],
        cart_id: str,
        items_total: Decimal,
        delivery_fee: Decimal,
    ) -> OrderSummaryDTO:

        if order_data.promo_code_id:
            with redis_lock(
                f"promo:{order_data.promo_code_id}", timeout=REDIS_LOCK_TIMEOUT
            ):
                with transaction.atomic():
                    return self._execute_order(
                        order_data=order_data,
                        cart_items=cart_items,
                        cart_id=cart_id,
                        items_total=items_total,
                        delivery_fee=delivery_fee,
                    )

        with transaction.atomic():
            return self._execute_order(
                order_data=order_data,
                cart_items=cart_items,
                cart_id=cart_id,
                items_total=items_total,
                delivery_fee=delivery_fee,
            )

    def _execute_order(
        self,
        order_data: PlaceOrderDTO,
        cart_items: List[CartItemDTO],
        cart_id: str,
        items_total: Decimal,
        delivery_fee: Decimal,
    ) -> OrderSummaryDTO:
        discount_price = self._get_discount_price(
            promo_code_id=order_data.promo_code_id,
            items_total=items_total,
        )
        tax_fee = self._calculate_tax_fee(
            items_total=items_total,
            discount_price=discount_price,
        )
        total_amount = (items_total + tax_fee + delivery_fee) - discount_price

        order_dto = self._save_order(
            order_data=order_data,
            items_total=items_total,
            delivery_fee=delivery_fee,
            tax_fee=tax_fee,
            total_amount=total_amount,
        )
        self._save_order_items(cart_items=cart_items, order_id=order_dto.order_id)
        self.restaurant_adapter.clear_customer_cart_items(cart_id=cart_id)

        return self._build_order_summary_dto(order_dto=order_dto, cart_items=cart_items)

    def _validate_promo_code_existence_and_eligibility(
        self,
        promo_code_id: int,
        items_total: Decimal,
    ):

        self.validate_promo_code_exist(promo_code_id=promo_code_id)

        promo_code_dto = self.promo_code_storage.get_promo_code_by_id(
            promo_code_id=promo_code_id
        )

        self._validate_promo_code_expiry(promo_code_dto=promo_code_dto)

        if items_total < Decimal(str(promo_code_dto.min_order_value)):
            raise PromoCodeNotEligible(
                min_order_value=promo_code_dto.min_order_value,
                items_total=items_total,
            )

    @staticmethod
    def _validate_promo_code_expiry(promo_code_dto: PromoCodeDTO):
        now = timezone.now()

        if promo_code_dto.valid_from and now < promo_code_dto.valid_from:
            raise PromoCodeNotYetValid(code=promo_code_dto.code)

        if promo_code_dto.valid_until and now > promo_code_dto.valid_until:
            raise PromoCodeExpired(code=promo_code_dto.code)

    def _get_discount_price(
        self,
        promo_code_id: Optional[int],
        items_total: Decimal,
    ) -> Decimal:

        if not promo_code_id:
            return Decimal("0.00")

        promo_code_dto = self.promo_code_storage.get_promo_code_by_id(
            promo_code_id=promo_code_id
        )

        self._validate_promo_code_usage_cap(
            promo_code_id=promo_code_id,
            max_usage_count=promo_code_dto.max_usage,
        )

        return self._calculate_discount_price(
            items_total=items_total,
            discount_type=promo_code_dto.discount_type,
            discount_value=Decimal(str(promo_code_dto.discount_value)),
        )

    def _validate_promo_code_usage_cap(
        self,
        promo_code_id: int,
        max_usage_count: int,
    ):
        usage_count = self.order_storage.get_promo_code_usage(
            promo_code_id=promo_code_id
        )
        if usage_count >= max_usage_count:
            raise PromoCodeMaximumUsed(max_usage_count=max_usage_count)

    def _validate_restaurant_timing(self, restaurant_id: str):
        now = datetime.now()
        timing = self.restaurant_adapter.get_restaurant_timing(
            restaurant_id=restaurant_id,
            day_of_week=now.isoweekday(),
        )

        if timing is None:
            raise RestaurantNotOpenNow(
                restaurant_id=restaurant_id,
                day_of_week=now.isoweekday(),
            )

        if not (timing.open_time <= now.time() <= timing.close_time):
            raise RestaurantClosed(restaurant_id=restaurant_id)

    def _validate_address_and_get_delivery_fee(
        self,
        address_id: int,
        restaurant_id: str,
    ) -> Decimal:
        pincode = self._get_validated_pincode(address_id=address_id)
        return self._get_validated_delivery_fee(
            restaurant_id=restaurant_id,
            pincode=pincode,
        )

    def _get_validated_pincode(self, address_id: int) -> str:
        address_dto = self.account_adapter.get_address_by_id(address_id=address_id)
        if address_dto is None:
            raise AddressNotFound(address_id=address_id)
        return address_dto.pincode

    def _get_validated_delivery_fee(
        self,
        restaurant_id: str,
        pincode: str,
    ) -> Decimal:
        zone_dto = self.restaurant_adapter.get_delivery_zone_by_restaurant_id(
            restaurant_id=restaurant_id,
            pin_code=pincode,
        )
        if zone_dto is None:
            raise DeliveryNotAvailableForAddress(
                restaurant_id=restaurant_id,
                pin_code=pincode,
            )
        return Decimal(str(zone_dto.delivery_fee))

    def _get_validated_cart_id(self, customer_id: str) -> str:
        cart_id = self.restaurant_adapter.get_customer_cart_id(customer_id=customer_id)
        if cart_id is None:
            raise CustomerCartNotFound(customer_id=customer_id)
        return cart_id

    def _get_validated_cart_items(self, cart_id: str) -> List[CartItemDTO]:
        cart_items = self.restaurant_adapter.get_customer_cart_items(cart_id=cart_id)
        if not cart_items:
            raise EmptyCartItemsFound(cart_id=cart_id)
        return cart_items

    def _save_order(
        self,
        order_data: PlaceOrderDTO,
        items_total: Decimal,
        delivery_fee: Decimal,
        tax_fee: Decimal,
        total_amount: Decimal,
    ) -> OrderDTO:
        create_order_dto = CreateOrderDTO(
            customer_id=order_data.customer_id,
            restaurant_id=order_data.restaurant_id,
            items_total=items_total,
            promo_code_id=order_data.promo_code_id,
            address_id=order_data.address_id,
            status=OrderStatus.PLACED,
            delivery_fee=delivery_fee,
            tax_fee=tax_fee,
            final_amount=total_amount,
        )
        return self.order_storage.create_order(create_order_dto=create_order_dto)

    def _save_order_items(
        self,
        cart_items: List[CartItemDTO],
        order_id: str,
    ):
        order_items = self._build_order_items(cart_items=cart_items, order_id=order_id)
        self.order_storage.create_order_items(order_item_dtos=order_items)

    @staticmethod
    def _calculate_items_total(cart_items: List[CartItemDTO]) -> Decimal:
        items_total = sum(
            Decimal(str(item.item_price)) * Decimal(str(item.quantity))
            for item in cart_items
        )
        return Decimal(items_total)

    @staticmethod
    def _calculate_discount_price(
        items_total: Decimal,
        discount_type: str,
        discount_value: Decimal,
    ) -> Decimal:
        if discount_type == PromoCodeType.PERCENTAGE.value:
            return (items_total * discount_value / Decimal("100")).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        return discount_value

    @staticmethod
    def _calculate_tax_fee(
        items_total: Decimal,
        discount_price: Decimal,
    ) -> Decimal:
        return (
            (items_total - discount_price)
            * Decimal(str(TAX_PERCENTAGE))
            / Decimal("100")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    def _build_order_items(
        cart_items: List[CartItemDTO],
        order_id: str,
    ) -> List[CreateOrderItemDTO]:
        return [
            CreateOrderItemDTO(
                order_id=order_id,
                item_id=cart_item.menu_item_id,
                item_price=cart_item.item_price,
                quantity=cart_item.quantity,
            )
            for cart_item in cart_items
        ]

    @staticmethod
    def _build_order_summary_dto(
        cart_items: List[CartItemDTO],
        order_dto: OrderDTO,
    ) -> OrderSummaryDTO:
        return OrderSummaryDTO(
            order_id=order_dto.order_id,
            customer_id=order_dto.customer_id,
            restaurant_id=order_dto.restaurant_id,
            status=order_dto.status,
            items=[
                OrderItemSummaryDTO(
                    item_id=item.menu_item_id,
                    quantity=item.quantity,
                    item_price=Decimal(str(item.item_price)),
                    subtotal=Decimal(str(item.item_price)) * item.quantity,
                )
                for item in cart_items
            ],
            items_total=order_dto.items_total,
            delivery_fee=order_dto.delivery_fee,
            tax_fee=order_dto.tax_fee,
            final_amount=order_dto.final_amount,
            address_id=order_dto.address_id,
            promo_code_id=order_dto.promo_code_id,
            placed_at=order_dto.placed_at,
        )
