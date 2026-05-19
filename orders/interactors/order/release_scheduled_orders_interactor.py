from datetime import datetime

from django.db import transaction
from django.utils import timezone

from orders.adapter.restaurant import RestaurantAdapter
from orders.constants.enums import OrderStatus
from orders.interactors.dtos import OrderDTO
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.mixin.order_mixin import OrderMixin


class ReleaseScheduledOrdersInteractor(OrderMixin):
    def __init__(self, order_storage: OrderStorageInterface):
        self.restaurant_adapter = RestaurantAdapter()
        self.order_storage = order_storage

    def release_scheduled_orders(self):
        with transaction.atomic():
            scheduled_orders = self.order_storage.get_scheduled_orders_due_for_release()
            for order_dto in scheduled_orders:
                if self._should_cancel(order_dto=order_dto):
                    self.order_storage.update_order_status(
                        order_id=order_dto.order_id,
                        status=OrderStatus.CANCELLED,
                    )
                else:
                    self.order_storage.update_order_status(
                        order_id=order_dto.order_id,
                        status=OrderStatus.PLACED,
                    )

    def _should_cancel(self, order_dto: OrderDTO) -> bool:
        return self._has_unavailable_items(
            order_id=order_dto.order_id
        ) or self._is_restaurant_closed(
            scheduled_for=order_dto.scheduled_for,
            restaurant_id=order_dto.restaurant_id,
        )

    def _has_unavailable_items(self, order_id: str) -> bool:
        item_ids = self.order_storage.get_order_item_ids(order_id=order_id)
        unavailable = self.restaurant_adapter.get_unavailable_menu_items(
            menu_item_ids=item_ids,
        )
        return len(unavailable) > 0

    def _is_restaurant_closed(
        self, scheduled_for: datetime, restaurant_id: str
    ) -> bool:
        scheduled_for = timezone.localtime(scheduled_for)
        timing = self.restaurant_adapter.get_restaurant_timing(
            restaurant_id=restaurant_id,
            day_of_week=scheduled_for.isoweekday(),
        )
        if timing is None:
            return True

        current_time = scheduled_for.time()
        return not (timing.open_time <= current_time <= timing.close_time)
