from datetime import time
from typing import Optional

from restaurants.exception.custom_exceptions import NothingToUpdate
from restaurants.interactors.dtos import UpdateRestaurantTimingDTO, RestaurantTimingDTO
from restaurants.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from restaurants.mixins.restaurant_timing_mixin import TimingMixin
from utils.caching_decorators import invalidate_interactor_cache


class UpdateRestaurantTimingInteractor(TimingMixin):
    def __init__(self, restaurant_timing_storage: RestaurantTimingStorageInterface):
        super().__init__(restaurant_timing_storage=restaurant_timing_storage)
        self.restaurant_timing_storage = restaurant_timing_storage

    @invalidate_interactor_cache(cache_name="restaurant_timings")
    def update_restaurant_timing(
        self, update_restaurant_timing_dto: UpdateRestaurantTimingDTO
    ) -> RestaurantTimingDTO:

        timing_data = self.validate_restaurant_timing_exists(
            timing_id=update_restaurant_timing_dto.timing_id
        )
        self.validate_user_is_restaurant_owner_through_timing_id(
            timing_id=update_restaurant_timing_dto.timing_id,
            user_id=update_restaurant_timing_dto.user_id,
        )
        self._validate_update_properties(
            open_time=update_restaurant_timing_dto.open_time,
            close_time=update_restaurant_timing_dto.close_time,
        )

        self.validate_restaurant_timings(
            open_time=update_restaurant_timing_dto.open_time,
            close_time=update_restaurant_timing_dto.close_time,
            actual_open_time=timing_data.open_time,
            actual_close_time=timing_data.close_time,
        )

        return self.restaurant_timing_storage.update_restaurant_timing(
            update_restaurant_timing_dto=update_restaurant_timing_dto
        )

    @staticmethod
    def _validate_update_properties(
        open_time: Optional[time], close_time: Optional[time]
    ):

        if open_time is None and close_time is None:
            raise NothingToUpdate()
