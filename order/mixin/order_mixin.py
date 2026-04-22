from order.constants.enums import OrderStatus
from order.exception.custom_exceptions import OrderNotFound, \
    InvalidOrderStatusTransition
from order.interactors.storage_interface.order_storage_interface import (
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

    def validate_order_is_exists(self, order_id: str):

        order_dto = self.order_storage.get_order(order_id=order_id)

        if order_dto is None:
            raise OrderNotFound(order_id=order_id)

    @staticmethod
    def validate_order_status_transition(
        current_status: OrderStatus,
        new_status: OrderStatus,
    ):
        allowed = VALID_TRANSITIONS.get(current_status, [])
        if new_status not in allowed:
            raise InvalidOrderStatusTransition(
                current_status=current_status.value,
                new_status=new_status.value,
                allowed=allowed,
            )
