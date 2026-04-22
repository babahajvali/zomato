from django.db import transaction

from order.adapter.restaurant import RestaurantAdapter
from order.constants.enums import OrderStatus
from order.exception.custom_exceptions import UserIsNotRestaurantOwner
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
        self.restaurant_adapter = RestaurantAdapter()

    def update_order_status(
        self, order_id: str, status: OrderStatus, user_id: str
    ) -> OrderDTO:

        self.validate_order_is_exists(order_id=order_id)

        order_dto = self.order_storage.get_order(order_id=order_id)

        self._validate_user_is_restaurant_owner(
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

    def _validate_user_is_restaurant_owner(self, user_id: str, restaurant_id: str):
        owner_id = self.restaurant_adapter.get_restaurant_owner_id(
            restaurant_id=restaurant_id
        )
        if owner_id != user_id:
            raise UserIsNotRestaurantOwner(user_id=user_id)
