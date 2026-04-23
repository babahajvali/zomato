from datetime import timedelta
from typing import List, Optional
from datetime import datetime
from django.db import transaction
from django.utils import timezone

from orders.constants.enums import OrderStatus
from orders.exception.custom_exceptions import (
    OrderCancellationTimeExceeded,
    OrderCannotBeCancelled,
    OrderAlreadyCancelled,
)
from orders.interactors.dtos import OrderDTO
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

        self.validate_order_exists(order_id=order_id)
        self.validate_order_belongs_to_user(
            order_id=order_id,
            user_id=user_id,
        )
        self._validate_cancel_order_time(order_id=order_id, placed_at=None)

        with redis_lock(
            lock_key=f"order_status_{order_id}",
            timeout=10,
        ):
            with transaction.atomic():
                order_dto = self.order_storage.get_order(order_id=order_id)

                self._validate_order_is_not_already_cancelled(order_dto=order_dto)
                self._validate_cancel_order_time(
                    placed_at=order_dto.placed_at, order_id=order_dto.order_id
                )

                return self.order_storage.update_order_status(
                    order_id=order_id,
                    status=OrderStatus.CANCELLED,
                )

    def auto_cancel_order(self, order_id: str) -> OrderDTO:
        self.validate_order_exists(order_id=order_id)
        self._validate_order_is_cancellable(order_id=order_id)

        return self.order_storage.update_order_status(
            order_id=order_id, status=OrderStatus.CANCELLED
        )

    def get_user_orders(self, user_id: str, limit: int, offset: int) -> List[OrderDTO]:

        return self.order_storage.get_user_orders(
            user_id=user_id, limit=limit, offset=offset
        )

    def get_order(self, order_id: str) -> OrderDTO:
        self.validate_order_exists(order_id=order_id)

        return self.order_storage.get_order(order_id=order_id)

    def _validate_cancel_order_time(self, order_id: str, placed_at: Optional[datetime]):
        if not placed_at:
            placed_at = self.order_storage.get_order_placed_at(order_id=order_id)
        now = timezone.now()

        if now - placed_at > timedelta(minutes=5):
            raise OrderCancellationTimeExceeded(order_id=order_id)

    def _validate_order_is_cancellable(self, order_id: str):
        order_dto = self.order_storage.get_order(order_id=order_id)

        if order_dto.status != OrderStatus.PLACED:
            raise OrderCannotBeCancelled(order_id=order_id)

    @staticmethod
    def _validate_order_is_not_already_cancelled(order_dto):
        if order_dto.status == OrderStatus.CANCELLED.value:
            raise OrderAlreadyCancelled(order_id=order_dto.order_id)
