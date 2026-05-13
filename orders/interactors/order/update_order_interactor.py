from django.db import transaction

from orders.adapter.restaurant import RestaurantAdapter
from orders.constants.enums import OrderStatus
from orders.interactors.dtos import OrderDTO
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.mixin.order_mixin import OrderMixin
from utils.caching_decorators import invalidate_interactor_cache
from utils.redis_util import redis_lock


@invalidate_interactor_cache(cache_name="user_scheduled_orders")
@invalidate_interactor_cache(cache_name="user_orders")
class UpdateOrderInteractor(OrderMixin):
    def __init__(self, order_storage: OrderStorageInterface):
        super().__init__(order_storage=order_storage)
        self.order_storage = order_storage
        self.restaurant_adapter = RestaurantAdapter()

    def update_order_status(
        self, order_id: str, status: OrderStatus, user_id: str
    ) -> OrderDTO:
        order_dto = self._get_validated_order(order_id=order_id)
        self._validate_ownership(
            restaurant_id=order_dto.restaurant_id,
            user_id=user_id,
        )

        with redis_lock(lock_key=f"order_status_{order_id}", timeout=10):
            with transaction.atomic():
                return self._revalidate_and_update(order_id=order_id, status=status)

    def _get_validated_order(self, order_id: str) -> OrderDTO:
        order_dto = self.validate_order_exists(order_id=order_id, user_id=None)

        return order_dto

    def _validate_ownership(self, restaurant_id: str, user_id: str):
        owner_id = self.restaurant_adapter.get_restaurant_owner_id(
            restaurant_id=restaurant_id
        )
        self.validate_user_is_restaurant_owner(user_id=user_id, owner_id=owner_id)

    def _revalidate_and_update(self, order_id: str, status: OrderStatus) -> OrderDTO:
        # TODO: no None check — if the order was deleted between the outer validate and here, order_dto.status → AttributeError.
        order_dto = self.order_storage.get_order(order_id=order_id)
        self.validate_order_status_transition(
            current_status=order_dto.status,
            new_status=status,
        )

        return self.order_storage.update_order_status(order_id=order_id, status=status)
