from datetime import datetime, timedelta
from decimal import Decimal
from typing import List

from django.db import transaction
from django.utils import timezone

from orders.adapter.dtos import CartItemDTO
from orders.constants.constants import REDIS_LOCK_TIMEOUT_SECS, RELEASE_WINDOW_MINS
from orders.constants.enums import OrderStatus
from orders.exception.custom_exceptions import (
    RestaurantNotOpenAtScheduledTime,
    ScheduledTimeTooSoon,
)
from orders.interactors.dtos import (
    CreateOrderDTO,
    OrderDTO,
    PlaceScheduledOrderDTO,
    ScheduledOrderDTO,
)
from orders.interactors.order.order_placement_base import OrderPlacementBase
from utils.caching_decorators import invalidate_interactor_cache
from utils.redis_util import redis_lock


@invalidate_interactor_cache(cache_name="user_scheduled_orders")
class PlaceScheduledOrderInteractor(OrderPlacementBase):
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
            timeout=REDIS_LOCK_TIMEOUT_SECS,
        ):
            cart_id = self._get_validated_cart_id(customer_id=order_data.customer_id)
            cart_items = self._get_validated_cart_items(cart_id=cart_id)
            items_total = self.calculate_items_total(cart_items=cart_items)

            self._validate_items_available(cart_items=cart_items)

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
                timeout=REDIS_LOCK_TIMEOUT_SECS,
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
        min_time = now + timedelta(minutes=RELEASE_WINDOW_MINS)

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
