from typing import List

from restaurants.interactors.dtos import RestaurantTimingDTO, CreateRestaurantTimingDTO
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from restaurants.mixins.restaurant_mixin import RestaurantMixin
from restaurants.mixins.restaurant_timing_mixin import TimingMixin
from utils.caching_decorators import invalidate_interactor_cache, interactor_cache


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

    @invalidate_interactor_cache(cache_name="restaurant_timings")
    def create_restaurant_timing(
        self, create_restaurant_timing_dto: CreateRestaurantTimingDTO, user_id: str
    ) -> RestaurantTimingDTO:
        self.validate_day_of_week(day_of_week=create_restaurant_timing_dto.day_of_week)
        self.validate_restaurant_exists(
            restaurant_id=create_restaurant_timing_dto.restaurant_id
        )
        self.validate_user_is_restaurant_owner(
            restaurant_id=create_restaurant_timing_dto.restaurant_id, user_id=user_id
        )

        self.validate_restaurant_timing_within_range(
            open_time=create_restaurant_timing_dto.open_time,
            close_time=create_restaurant_timing_dto.close_time,
        )

        return self.restaurant_timing_storage.create_bulk_restaurant_timing(
            create_restaurant_timing_dto=[create_restaurant_timing_dto]
        )[0]

    @interactor_cache(cache_name="restaurant_timings")
    def get_restaurant_timings(self, restaurant_id: str) -> List[RestaurantTimingDTO]:
        self.validate_restaurant_exists(restaurant_id=restaurant_id)

        return self.restaurant_timing_storage.get_restaurant_timings(
            restaurant_id=restaurant_id
        )

    @invalidate_interactor_cache(cache_name="restaurant_timings")
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
        self.validate_restaurant_exists(restaurant_id=restaurant_id)

        return self.restaurant_timing_storage.get_day_restaurant_timing(
            restaurant_id=restaurant_id, day_of_week=day_of_week
        )
