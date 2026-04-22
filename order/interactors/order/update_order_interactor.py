from django.db import transaction

from order.constants.enums import OrderStatus
from order.interactors.dtos import OrderDTO
from order.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from order.mixin.order_mixin import OrderMixin
from utils.redis_util import redis_lock


class UpdateOrderStatusInteractor(OrderMixin):
    def __init__(self, order_storage: OrderStorageInterface):
        super().__init__(order_storage=order_storage)
        self.order_storage = order_storage

    def update_order_status(
        self, order_id: str, status: OrderStatus, user_id: str
    ) -> OrderDTO:

        self.validate_order_exists(order_id=order_id)

        order_dto = self.order_storage.get_order(order_id=order_id)

        self.validate_user_is_restaurant_owner(
            user_id=user_id,
            restaurant_id=order_dto.restaurant_id,
        )

        self.validate_order_status_transition(
            current_status=order_dto.status,
            new_status=status,
        )

        with redis_lock(
            lock_key=f"order_status_{order_id}",
            timeout=10,
        ):
            with transaction.atomic():
                order_dto = self.order_storage.get_order(order_id=order_id)

                self.validate_order_status_transition(
                    current_status=order_dto.status,
                    new_status=status,
                )

                return self.order_storage.update_order_status(
                    order_id=order_id,
                    status=status,
                )
