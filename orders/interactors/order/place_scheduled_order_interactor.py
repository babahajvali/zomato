from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional

from django.db import transaction
from django.utils import timezone

from orders.adapter.account import AccountAdapter
from orders.adapter.dtos import CartItemDTO
from orders.adapter.restaurant import RestaurantAdapter
from orders.constants.enums import OrderStatus
from orders.exception.custom_exceptions import (
    PromoCodeUsageLimitReached,
    PromoCodeNotEligible,
    DeliveryUnavailableForAddress,
    AddressNotFound,
    CartIsEmpty,
    PromoCodeNotYetValid,
    PromoCodeExpired,
    CustomerCartNotFound,
    MenuItemsUnavailable,
    ScheduledTimeTooSoon,
    RestaurantNotOpenAtScheduledTime,
)
from orders.interactors.dtos import (
    PlaceScheduledOrderDTO,
    OrderDTO,
    CreateOrderDTO,
    CreateOrderItemDTO,
    PromoCodeDTO,
    ScheduledOrderDTO,
)
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)
from orders.mixin.order_mixin import OrderMixin
from orders.mixin.promocode_mixin import PromoCodeMixin
from utils.redis_util import redis_lock

REDIS_LOCK_TIMEOUT = 30
SCHEDULED_MIN_MINS = 30


class PlaceScheduledOrderInteractor(PromoCodeMixin, OrderMixin):
    def __init__(
        self,
        promo_code_storage: PromoCodeStorageInterface,
        order_storage: OrderStorageInterface,
    ):
        super().__init__(
            promo_code_storage=promo_code_storage,
            order_storage=order_storage,
        )
        self.promo_code_storage = promo_code_storage
        self.order_storage = order_storage
        self.account_adapter = AccountAdapter()
        self.restaurant_adapter = RestaurantAdapter()

    def place_scheduled_order(
        self, order_data: PlaceScheduledOrderDTO
    ) -> ScheduledOrderDTO:

        self._validate_scheduled_time(scheduled_for=order_data.scheduled_for)
        self._validate_restaurant_timing_for_scheduled_time(
            restaurant_id=order_data.restaurant_id,
            scheduled_for=order_data.scheduled_for,
        )
        delivery_fee = self._validate_address_and_get_delivery_fee(
            address_id=order_data.address_id,
            restaurant_id=order_data.restaurant_id,
        )

        with redis_lock(
            f"order:{order_data.customer_id}",
            timeout=REDIS_LOCK_TIMEOUT,
        ):
            cart_id = self._get_validated_cart_id(customer_id=order_data.customer_id)
            cart_items = self._get_validated_cart_items(cart_id=cart_id)
            items_total = self.calculate_items_total(cart_items=cart_items)

            self._validate_menu_items_available(cart_items=cart_items)

            if order_data.promo_code_id:
                self._validate_promo_code_existence_and_eligibility(
                    promo_code_id=order_data.promo_code_id,
                    items_total=items_total,
                )

            return self._place_scheduled_order_with_locks(
                order_data=order_data,
                cart_items=cart_items,
                cart_id=cart_id,
                items_total=items_total,
                delivery_fee=delivery_fee,
            )

    def _place_scheduled_order_with_locks(
        self,
        order_data: PlaceScheduledOrderDTO,
        cart_items: List[CartItemDTO],
        cart_id: str,
        items_total: Decimal,
        delivery_fee: Decimal,
    ) -> ScheduledOrderDTO:

        def run():
            with transaction.atomic():
                return self._execute_scheduled_order(
                    order_data=order_data,
                    cart_items=cart_items,
                    cart_id=cart_id,
                    items_total=items_total,
                    delivery_fee=delivery_fee,
                )

        if order_data.promo_code_id:
            with redis_lock(
                f"promo:{order_data.promo_code_id}",
                timeout=REDIS_LOCK_TIMEOUT,
            ):
                return run()

        return run()

    def _execute_scheduled_order(
        self,
        order_data: PlaceScheduledOrderDTO,
        cart_items: List[CartItemDTO],
        cart_id: str,
        items_total: Decimal,
        delivery_fee: Decimal,
    ) -> ScheduledOrderDTO:

        discount_price = self._get_discount_price(
            promo_code_id=order_data.promo_code_id,
            items_total=items_total,
        )
        tax_fee = self.calculate_tax_fee(
            items_total=items_total,
            discount_price=discount_price,
        )
        total_amount = (items_total + tax_fee + delivery_fee) - discount_price

        order_dto = self.save_scheduled_order(
            order_data=order_data,
            items_total=items_total,
            delivery_fee=delivery_fee,
            tax_fee=tax_fee,
            total_amount=total_amount,
        )
        self._save_order_items(
            cart_items=cart_items,
            order_id=order_dto.order_id,
        )
        self.restaurant_adapter.clear_customer_cart_items(cart_id=cart_id)

        return self.build_schedule_order_summary_dto(
            order_dto=order_dto,
            cart_items=cart_items,
        )

    @staticmethod
    def _validate_scheduled_time(scheduled_for: datetime):
        now = timezone.now()
        min_time = now + timedelta(minutes=SCHEDULED_MIN_MINS)

        if scheduled_for < min_time:
            raise ScheduledTimeTooSoon(scheduled_for=scheduled_for)

    def _validate_restaurant_timing_for_scheduled_time(
        self,
        restaurant_id: str,
        scheduled_for: datetime,
    ):
        day_of_week = scheduled_for.isoweekday()

        timing = self.restaurant_adapter.get_restaurant_timing(
            restaurant_id=restaurant_id,
            day_of_week=day_of_week,
        )

        if timing is None:
            raise RestaurantNotOpenAtScheduledTime(
                restaurant_id=restaurant_id,
                scheduled_for=scheduled_for,
            )

        scheduled_time = scheduled_for.time()

        if not (timing.open_time <= scheduled_time <= timing.close_time):
            raise RestaurantNotOpenAtScheduledTime(
                restaurant_id=restaurant_id,
                scheduled_for=scheduled_for,
            )

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

    def _get_validated_delivery_fee(self, restaurant_id: str, pincode: str) -> Decimal:
        zone_dto = self.restaurant_adapter.get_delivery_zone_by_restaurant_id(
            restaurant_id=restaurant_id,
            pin_code=pincode,
        )
        if zone_dto is None:
            raise DeliveryUnavailableForAddress(
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
            raise CartIsEmpty(cart_id=cart_id)
        return cart_items

    def _validate_menu_items_available(self, cart_items: List[CartItemDTO]):
        item_ids = [item.menu_item_id for item in cart_items]
        unavailable = self.restaurant_adapter.get_unavailable_menu_items(
            menu_item_ids=item_ids
        )
        if unavailable:
            raise MenuItemsUnavailable(unavailable_item_ids=unavailable)

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
        self._validate_promo_code_usage_limit(
            promo_code_id=promo_code_id,
            max_usage_count=promo_code_dto.max_usage,
        )
        return self.calculate_discount_price(
            items_total=items_total,
            discount_type=promo_code_dto.discount_type,
            discount_value=Decimal(str(promo_code_dto.discount_value)),
        )

    def _validate_promo_code_usage_limit(
        self, promo_code_id: int, max_usage_count: int
    ):
        usage_count = self.order_storage.get_promo_code_usage(
            promo_code_id=promo_code_id
        )
        if usage_count >= max_usage_count:
            raise PromoCodeUsageLimitReached(max_usage_count=max_usage_count)

    def save_scheduled_order(
        self,
        order_data: PlaceScheduledOrderDTO,
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
            status=OrderStatus.SCHEDULED,
            delivery_fee=delivery_fee,
            tax_fee=tax_fee,
            final_amount=total_amount,
            scheduled_for=order_data.scheduled_for,
        )
        return self.order_storage.create_order(create_order_dto=create_order_dto)

    def _save_order_items(
        self,
        cart_items: List[CartItemDTO],
        order_id: str,
    ):
        order_items = [
            CreateOrderItemDTO(
                order_id=order_id,
                item_id=item.menu_item_id,
                item_price=item.item_price,
                quantity=item.quantity,
            )
            for item in cart_items
        ]
        self.order_storage.create_order_items(order_item_dtos=order_items)
