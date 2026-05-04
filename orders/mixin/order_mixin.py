from typing import Optional

from orders.constants.enums import OrderStatus
from orders.exception.custom_exceptions import (
    InvalidOrderStatusTransition,
    OrderNotFound,
    OrderNotOwnedByUser,
    UserNotRestaurantOwner,
)
from orders.interactors.dtos import OrderDTO
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)

VALID_TRANSITIONS = {
    OrderStatus.PLACED: [OrderStatus.CONFIRMED],
    OrderStatus.CONFIRMED: [OrderStatus.PREPARING],
    OrderStatus.PREPARING: [OrderStatus.OUT_OF_DELIVERY],
    OrderStatus.OUT_OF_DELIVERY: [OrderStatus.DELIVERED],
    OrderStatus.DELIVERED: [],
    OrderStatus.CANCELLED: [],
}


class OrderMixin:
    def __init__(self, order_storage: OrderStorageInterface, **kwargs):
        self.order_storage = order_storage
        super().__init__(**kwargs)

    def validate_order_exists(self, order_id: str, user_id: Optional[str]) -> OrderDTO:

        order_dto = self.order_storage.get_order(order_id=order_id)

        if order_dto is None:
            raise OrderNotFound(order_id=order_id)

        if order_dto.customer_id != user_id and user_id is not None:
            raise OrderNotOwnedByUser(order_id=order_id, user_id=user_id)

        return order_dto

    @staticmethod
    def validate_order_status_transition(
        current_status: OrderStatus,
        new_status: OrderStatus,
    ):
        if isinstance(current_status, str):
            current_status = OrderStatus(current_status)
        if isinstance(new_status, str):
            new_status = OrderStatus(new_status)

        allowed = VALID_TRANSITIONS.get(current_status, [])
        if new_status not in allowed:
            raise InvalidOrderStatusTransition(
                current_status=current_status.value,
                new_status=new_status.value,
                allowed=[status.value for status in allowed],
            )

    @staticmethod
    def validate_user_is_restaurant_owner(user_id: str, owner_id: str):

        if owner_id != user_id:
            raise UserNotRestaurantOwner(user_id=user_id)
