from restaurants.interactors.dtos import UpdateRestaurantTimingDTO, RestaurantTimingDTO
from restaurants.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from restaurants.mixins.restaurant_timing_mixin import TimingMixin


class UpdateRestaurantTimingInteractor(TimingMixin):
    def __init__(self, restaurant_timing_storage: RestaurantTimingStorageInterface):
        super().__init__(restaurant_timing_storage=restaurant_timing_storage)
        self.restaurant_timing_storage = restaurant_timing_storage

    def update_restaurant_timing(
        self, update_restaurant_timing_dto: UpdateRestaurantTimingDTO
    ) -> RestaurantTimingDTO:
        self.validate_restaurant_timing_exists(
            timing_id=update_restaurant_timing_dto.timing_id
        )
        self.validate_user_is_restaurant_owner_through_timing_id(
            timing_id=update_restaurant_timing_dto.timing_id,
            user_id=update_restaurant_timing_dto.user_id,
        )

        open_time = update_restaurant_timing_dto.open_time
        close_time = update_restaurant_timing_dto.close_time

        self.validate_restaurant_timings(
            open_time=open_time,
            close_time=close_time,
            timing_id=update_restaurant_timing_dto.timing_id,
        )

        return self.restaurant_timing_storage.update_restaurant_timing(
            update_restaurant_timing_dto=update_restaurant_timing_dto
        )
