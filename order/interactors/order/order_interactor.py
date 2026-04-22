from datetime import timedelta
from typing import List

from django.utils import timezone

from order.exception.custom_exceptions import (
    OrderCancellationTimeExceeded,
    OrderCannotBeCancelled,
)
from order.interactors.dtos import OrderDTO
from order.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from order.mixin.order_mixin import OrderMixin


class OrderInteractor(OrderMixin):
    def __init__(self, order_storage: OrderStorageInterface):
        super().__init__(order_storage=order_storage)
        self.order_storage = order_storage

    def cancel_order(self, order_id: str, user_id: str) -> OrderDTO:
        self.validate_order_exists(order_id=order_id)
        self.validate_order_belongs_to_user(order_id=order_id, user_id=user_id)
        self._validate_cancel_order_time(order_id=order_id)

        return self.order_storage.cancel_order(order_id=order_id)

    def auto_cancel_order(self, order_id: str) -> OrderDTO:
        self.validate_order_exists(order_id=order_id)
        self._validate_order_is_cancellable(order_id=order_id)

        return self.order_storage.cancel_order(order_id=order_id)

    def user_orders(self, user_id: str) -> List[OrderDTO]:
        return self.order_storage.get_user_orders(user_id=user_id)

    def get_order(self, order_id: str) -> OrderDTO:
        self.validate_order_exists(order_id=order_id)

        return self.order_storage.get_order(order_id=order_id)

    def _validate_cancel_order_time(self, order_id: str):
        placed_at = self.order_storage.get_order_placed_at(order_id=order_id)
        now = timezone.now()

        if now - placed_at > timedelta(minutes=5):
            raise OrderCancellationTimeExceeded(order_id=order_id)

    def _validate_order_is_cancellable(self, order_id: str):
        order_dto = self.order_storage.get_order(order_id=order_id)

        if order_dto.status not in ["PLACED"]:
            raise OrderCannotBeCancelled(order_id=order_id)
