from datetime import datetime
from typing import List, Optional

from django.db import transaction

from order.adapter.account import AccountAdapter
from order.adapter.dtos import CartItemDTO
from order.adapter.restaurant import RestaurantAdapter
from order.constants.constants import TAX_PERCENTAGE
from order.constants.enums import PromoCodeType, OrderStatus
from order.exception.custom_exceptions import (
    PromoCodeMaximumUsed,
    PromoCodeNotEligible,
    InvalidDeliveryZoneFound,
    InvalidAddressFound,
    RestaurantDayTimingNotFound,
    RestaurantClosed,
    EmptyCartItemsFound,
)
from order.interactors.dtos import (
    PlaceOrderDTO,
    OrderDTO,
    CreateOrderDTO,
    CreateOrderItemDTO,
)
from order.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from order.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)
from order.mixin.promocode_mixin import PromoCodeMixin
from utils.redis_util import redis_lock


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

    def place_order(self, order_data: PlaceOrderDTO) -> OrderDTO:
        cart_id = self.restaurant_adapter.get_customer_cart_id(
            customer_id=order_data.customer_id
        )
        cart_items = self._get_validated_cart_items(cart_id=cart_id)
        items_total = self._calculate_items_total(cart_items=cart_items)

        self._run_pre_lock_validations(order_data=order_data, items_total=items_total)

        lock_key = self._get_lock_key(order_data=order_data)
        with redis_lock(lock_key=lock_key, timeout=10):
            with transaction.atomic():
                return self._execute_order(
                    order_data=order_data,
                    cart_items=cart_items,
                    cart_id=cart_id,
                    items_total=items_total,
                )

    def _run_pre_lock_validations(self, order_data: PlaceOrderDTO, items_total: float):
        if order_data.promo_code_id:
            self._validate_promo_code_existence_and_eligibility(
                promo_code_id=order_data.promo_code_id,
                items_total=items_total,
            )
        self._validate_restaurant_timing(restaurant_id=order_data.restaurant_id)
        self._validate_address_and_get_delivery_fee(
            address_id=order_data.address_id,
            restaurant_id=order_data.restaurant_id,
        )

    def _validate_promo_code_existence_and_eligibility(
        self, promo_code_id: int, items_total: float
    ):
        self.validate_promo_code_exist(promo_code_id=promo_code_id)
        promo_code_dto = self.promo_code_storage.get_promo_code_by_id(
            promo_code_id=promo_code_id
        )
        if items_total < promo_code_dto.min_order_value:
            raise PromoCodeNotEligible(
                min_order_value=promo_code_dto.min_order_value,
                items_total=items_total,
            )

    def _validate_restaurant_timing(self, restaurant_id: str):
        now = datetime.now()
        timing = self.restaurant_adapter.get_restaurant_timing(
            restaurant_id=restaurant_id,
            day_of_week=now.isoweekday(),
        )
        if timing is None:
            raise RestaurantDayTimingNotFound(
                restaurant_id=restaurant_id,
                day_of_week=now.isoweekday(),
            )
        if not (timing.open_time <= now.time() <= timing.close_time):
            raise RestaurantClosed(restaurant_id=restaurant_id)

    def _validate_address_and_get_delivery_fee(
        self, address_id: int, restaurant_id: str
    ) -> float:
        pincode = self._get_validated_pincode(address_id=address_id)

        return self._get_validated_delivery_fee(
            restaurant_id=restaurant_id, pincode=pincode
        )

    def _get_validated_pincode(self, address_id: int) -> str:
        address_dto = self.account_adapter.get_address_by_id(address_id=address_id)

        if address_dto is None:
            raise InvalidAddressFound(address_id=address_id)

        return address_dto.pincode

    def _get_validated_delivery_fee(self, restaurant_id: str, pincode: str) -> float:
        zone_dto = self.restaurant_adapter.get_delivery_zone_by_restaurant_id(
            restaurant_id=restaurant_id,
            pin_code=pincode,
        )

        if zone_dto is None:
            raise InvalidDeliveryZoneFound(
                restaurant_id=restaurant_id, pin_code=pincode
            )

        return zone_dto.delivery_fee

    def _execute_order(
        self,
        order_data: PlaceOrderDTO,
        cart_items: List[CartItemDTO],
        cart_id: str,
        items_total: float,
    ) -> OrderDTO:
        delivery_fee = self._validate_address_and_get_delivery_fee(
            address_id=order_data.address_id,
            restaurant_id=order_data.restaurant_id,
        )
        discount_price = self._get_discount_price(
            promo_code_id=order_data.promo_code_id,
            items_total=items_total,
        )
        tax_fee = self._calculate_tax_fee(
            items_total=items_total, discount_price=discount_price
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
        return order_dto

    def _get_discount_price(
        self, promo_code_id: Optional[int], items_total: float
    ) -> float:
        if not promo_code_id:
            return 0.0

        promo_code_dto = self.promo_code_storage.get_promo_code_by_id(
            promo_code_id=promo_code_id
        )
        self._validate_promo_code_available(
            promo_code_id=promo_code_id,
            max_usage_count=promo_code_dto.max_usage,
        )

        return self._calculate_discount_price(
            items_total=items_total,
            discount_type=promo_code_dto.discount_type,
            discount_value=promo_code_dto.discount_value,
        )

    def _validate_promo_code_available(self, promo_code_id: int, max_usage_count: int):
        usage_count = self.order_storage.get_promo_code_usage(
            promo_code_id=promo_code_id
        )

        if usage_count >= max_usage_count:
            raise PromoCodeMaximumUsed(max_usage_count=usage_count)

    def _save_order(
        self,
        order_data: PlaceOrderDTO,
        items_total: float,
        delivery_fee: float,
        tax_fee: float,
        total_amount: float,
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

    def _save_order_items(self, cart_items: List[CartItemDTO], order_id: str):
        order_items = self._build_order_items(cart_items=cart_items, order_id=order_id)
        self.order_storage.create_order_items(order_item_dtos=order_items)

    def _get_validated_cart_items(self, cart_id: str) -> List[CartItemDTO]:
        cart_items = self.restaurant_adapter.get_customer_cart_items(cart_id=cart_id)
        if not cart_items:
            raise EmptyCartItemsFound(cart_id=cart_id)
        return cart_items

    @staticmethod
    def _get_lock_key(order_data: PlaceOrderDTO) -> str:
        if order_data.promo_code_id:
            return f"promo_{order_data.promo_code_id}"
        return f"order_{order_data.customer_id}"

    @staticmethod
    def _calculate_items_total(cart_items: List[CartItemDTO]) -> float:
        return sum(float(item.item_price) * float(item.quantity) for item in cart_items)

    @staticmethod
    def _calculate_discount_price(
        items_total: float, discount_type: str, discount_value: float
    ) -> float:
        if discount_type == PromoCodeType.PERCENTAGE.value:
            return items_total * (discount_value / 100)

        return discount_value

    @staticmethod
    def _calculate_tax_fee(items_total: float, discount_price: float) -> float:
        return (items_total - discount_price) * (TAX_PERCENTAGE / 100)

    @staticmethod
    def _build_order_items(
        cart_items: List[CartItemDTO], order_id: str
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
