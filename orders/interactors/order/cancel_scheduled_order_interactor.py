from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from orders.constants.constants import CANCEL_TIME, REDIS_LOCK_TIMEOUT_SECS
from orders.constants.enums import OrderStatus
from orders.exception.custom_exceptions import (
    OrderCancellationWindowExpired,
    OrderAlreadyCancelled,
    OrderCancellationNotAllowed,
)
from orders.interactors.dtos import OrderDTO
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.mixin.order_mixin import OrderMixin
from utils.redis_util import redis_lock


class CancelScheduledOrderInteractor(OrderMixin):
    def __init__(self, order_storage: OrderStorageInterface):
        super().__init__(order_storage=order_storage)
        self.order_storage = order_storage

    def cancel_scheduled_order(self, order_id: str, user_id: str) -> OrderDTO:

        with redis_lock(
            lock_key=f"order_status_{order_id}",
            timeout=REDIS_LOCK_TIMEOUT_SECS,
        ):
            with transaction.atomic():
                order_dto = self.validate_order_exists(
                    order_id=order_id, user_id=user_id
                )

                self._validate_not_already_cancelled(order_dto=order_dto)
                self._validate_cancellable_status(order_dto=order_dto)

                return self.order_storage.update_order_status(
                    order_id=order_id,
                    status=OrderStatus.CANCELLED,
                )

    @staticmethod
    def _validate_not_already_cancelled(order_dto: OrderDTO):
        if order_dto.status == OrderStatus.CANCELLED:
            raise OrderAlreadyCancelled(order_id=order_dto.order_id)

    def _validate_cancellable_status(self, order_dto: OrderDTO):

        if order_dto.status == OrderStatus.SCHEDULED:
            return

        if order_dto.status == OrderStatus.PLACED:
            self._validate_cancellation_window(
                order_id=order_dto.order_id,
            )
            return

        raise OrderCancellationNotAllowed(
            order_id=order_dto.order_id,
        )

    def _validate_cancellation_window(self, order_id: str):
        now = timezone.now()
        updated_at = self.order_storage.get_order_updated_at(order_id=order_id)
        cancellation_limit = updated_at + timedelta(minutes=CANCEL_TIME)

        if now > cancellation_limit:
            raise OrderCancellationWindowExpired(order_id=order_id, minutes=CANCEL_TIME)
