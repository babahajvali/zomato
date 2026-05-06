from datetime import datetime, timedelta, date
from typing import List, Optional
from django.db import transaction
from django.utils import timezone

from orders.app_service.dtos import RestaurantOrdersSummaryDTO, OrdersByStatusDTO
from orders.constants.constants import CANCEL_TIME
from orders.constants.enums import OrderStatus
from orders.exception.custom_exceptions import (
    OrderCancellationWindowExpired,
    OrderCancellationNotAllowed,
    OrderAlreadyCancelled,
)
from orders.interactors.dtos import (
    OrderDTO,
    OrderSummaryDTO,
    PeakHourDTO,
    TopSellingItemDTO,
    ScheduledOrderDTO,
)
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.mixin.order_mixin import OrderMixin
from utils.redis_util import redis_lock


class OrderInteractor(OrderMixin):
    def __init__(self, order_storage: OrderStorageInterface):
        super().__init__(order_storage=order_storage)
        self.order_storage = order_storage

    def cancel_order(self, order_id: str, user_id: str) -> OrderDTO:

        with redis_lock(
            lock_key=f"order_status_{order_id}",
            timeout=10,
        ):
            with transaction.atomic():
                order_dto = self.validate_order_exists(
                    order_id=order_id, user_id=user_id
                )

                self._validate_order_is_not_already_cancelled(order_dto=order_dto)
                self._validate_order_is_cancellable(
                    order_id=order_dto.order_id, order_status=order_dto.status.value
                )
                self._validate_cancel_order_time(
                    placed_at=order_dto.placed_at, order_id=order_dto.order_id
                )

                return self.order_storage.update_order_status(
                    order_id=order_id,
                    status=OrderStatus.CANCELLED,
                )

    def get_user_orders(self, user_id: str, limit: int, offset: int) -> List[OrderDTO]:

        return self.order_storage.get_user_orders(
            user_id=user_id, limit=limit, offset=offset
        )

    def get_order(self, order_id: str) -> OrderSummaryDTO:
        order_dto = self.validate_order_exists(order_id=order_id, user_id=None)

        order_items = self.order_storage.get_order_items(order_id=order_id)

        return self._build_order_summary(order_dto=order_dto, order_items=order_items)

    def get_restaurant_orders_summary(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> RestaurantOrdersSummaryDTO:

        return self.order_storage.get_restaurant_orders_summary(
            restaurant_id=restaurant_id, date_from=date_from, date_to=date_to
        )

    def get_orders_count_by_status(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> List[OrdersByStatusDTO]:

        return self.order_storage.get_orders_count_by_status(
            restaurant_id=restaurant_id, date_from=date_from, date_to=date_to
        )

    def get_peak_hours(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> List[PeakHourDTO]:

        return self.order_storage.get_peak_hours(
            restaurant_id=restaurant_id, date_from=date_from, date_to=date_to
        )

    def get_top_selling_items(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> List[TopSellingItemDTO]:

        return self.order_storage.get_top_selling_items(
            restaurant_id=restaurant_id, date_from=date_from, date_to=date_to
        )

    def get_user_scheduled_orders(
        self, user_id: str, limit: int, offset: int
    ) -> List[ScheduledOrderDTO]:

        order_dtos = self.order_storage.get_user_scheduled_orders(
            user_id=user_id,
            limit=limit,
            offset=offset,
        )
        order_ids = [order.order_id for order in order_dtos]

        order_items = self.order_storage.get_orders_items(order_ids=order_ids)

        return self.build_schedule_order_summaries(
            order_items=order_items,
            orders=order_dtos,
        )

    def _validate_cancel_order_time(self, order_id: str, placed_at: Optional[datetime]):
        if placed_at is None:
            placed_at = self.order_storage.get_order_placed_at(order_id=order_id)
        now = timezone.now()

        if now - placed_at > timedelta(minutes=CANCEL_TIME):
            raise OrderCancellationWindowExpired(order_id=order_id, minutes=CANCEL_TIME)

    @staticmethod
    def _validate_order_is_cancellable(order_status: str, order_id: str):

        if order_status != OrderStatus.PLACED.value:
            raise OrderCancellationNotAllowed(order_id=order_id)

    @staticmethod
    def _validate_order_is_not_already_cancelled(order_dto):
        if order_dto.status == OrderStatus.CANCELLED:
            raise OrderAlreadyCancelled(order_id=order_dto.order_id)

    @staticmethod
    def _build_order_summary(
        order_dto: OrderDTO,
        order_items,
    ) -> OrderSummaryDTO:
        return OrderSummaryDTO(
            order_id=order_dto.order_id,
            customer_id=order_dto.customer_id,
            restaurant_id=order_dto.restaurant_id,
            promo_code_id=order_dto.promo_code_id,
            status=order_dto.status,
            items=order_items,
            items_total=order_dto.items_total,
            delivery_fee=order_dto.delivery_fee,
            tax_fee=order_dto.tax_fee,
            final_amount=order_dto.final_amount,
            placed_at=order_dto.placed_at,
            address_id=order_dto.address_id,
        )
