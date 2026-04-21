from typing import List

from restaurant.interactors.dtos import RestaurantTimingDTO
from restaurant.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurant.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from restaurant.mixins.restaurant_mixin import RestaurantMixin
from restaurant.mixins.restaurant_timing_mixin import TimingMixin


class RestaurantTimingInteractor(RestaurantMixin, TimingMixin):
    def __init__(
        self,
        restaurant_timing_storage: RestaurantTimingStorageInterface,
        restaurant_storage: RestaurantStorageInterface,
    ):
        super().__init__(
            restaurant_storage=restaurant_storage,
            restaurant_timing_storage=restaurant_timing_storage,
        )
        self.restaurant_timing_storage = restaurant_timing_storage
        self.restaurant_storage = restaurant_storage

    def get_restaurant_timings(self, restaurant_id: str) -> List[RestaurantTimingDTO]:
        self.validate_restaurant_is_exists(restaurant_id=restaurant_id)

        return self.restaurant_timing_storage.get_restaurant_timings(
            restaurant_id=restaurant_id
        )

    def delete_restaurant_timing(self, id: int, user_id: str):
        self.validate_restaurant_timing_exists(id=id)
        self.validate_user_is_restaurant_owner_through_timing_id(id=id, user_id=user_id)

        return self.restaurant_timing_storage.delete_restaurant_timing(id=id)
