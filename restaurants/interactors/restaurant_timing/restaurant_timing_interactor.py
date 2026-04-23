from typing import List

from restaurants.interactors.dtos import RestaurantTimingDTO
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from restaurants.mixins.restaurant_mixin import RestaurantMixin
from restaurants.mixins.restaurant_timing_mixin import TimingMixin


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

    def delete_restaurant_timing(self, timing_id: int, user_id: str):
        self.validate_restaurant_timing_exists(timing_id=timing_id)
        self.validate_user_is_restaurant_owner_through_timing_id(
            timing_id=timing_id, user_id=user_id
        )

        return self.restaurant_timing_storage.delete_restaurant_timing(
            timing_id=timing_id
        )

    def get_day_restaurant_timing(
        self, restaurant_id: str, day_of_week: int
    ) -> RestaurantTimingDTO:
        self.validate_restaurant_is_exists(restaurant_id=restaurant_id)

        return self.restaurant_timing_storage.get_day_restaurant_timing(
            restaurant_id=restaurant_id, day_of_week=day_of_week
        )
