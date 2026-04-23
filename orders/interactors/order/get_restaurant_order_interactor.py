from datetime import timedelta
from typing import List

from django.utils import timezone

from orders.interactors.dtos import OrderDTO
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.mixin.order_mixin import OrderMixin


class GetRestaurantOrderInteractor(OrderMixin):
    def __init__(self, order_storage: OrderStorageInterface):
        super().__init__(order_storage=order_storage)
        self.order_storage = order_storage

    def get_restaurant_orders(self, restaurant_id: str, user_id: str) -> List[OrderDTO]:
        self.validate_user_is_restaurant_owner(
            restaurant_id=restaurant_id, user_id=user_id
        )

        return self.order_storage.get_restaurant_orders(restaurant_id=restaurant_id)

    def get_today_restaurant_orders(
        self, restaurant_id: str, user_id: str
    ) -> List[OrderDTO]:

        self.validate_user_is_restaurant_owner(
            restaurant_id=restaurant_id,
            user_id=user_id,
        )

        orders = self.order_storage.get_today_restaurant_orders(
            restaurant_id=restaurant_id,
        )

        return self._filter_orders_after_cancellation_window(orders=orders)

    @staticmethod
    def _filter_orders_after_cancellation_window(
        orders: List[OrderDTO],
    ) -> List[OrderDTO]:

        now = timezone.now()
        five_minutes_ago = now - timedelta(minutes=5)

        return [order for order in orders if order.placed_at <= five_minutes_ago]
