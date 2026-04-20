
from restaurant.interactors.dtos import UpdateRestaurantTimingDTO, \
    RestaurantTimingDTO
from restaurant.interactors.storage_interface.restaurant_timing_storage_interface import \
    RestaurantTimingStorageInterface
from restaurant.mixins.restaurant_timing_mixin import TimingMixin


class UpdateRestaurantTimingInteractor(TimingMixin):

    def __init__(
            self, restaurant_timing_storage: RestaurantTimingStorageInterface):
        super().__init__(restaurant_timing_storage=restaurant_timing_storage)
        self.restaurant_timing_storage = restaurant_timing_storage

    def update_restaurant_timing(
            self, update_restaurant_timing_dto: UpdateRestaurantTimingDTO) \
            -> RestaurantTimingDTO:

        self.check_restaurant_timing_exists(id=update_restaurant_timing_dto.id)
        self.check_user_is_restaurant_owner_through_timing_id(
            id=update_restaurant_timing_dto.id,
            user_id=update_restaurant_timing_dto.user_id,
        )

        open_time = update_restaurant_timing_dto.open_time
        close_time = update_restaurant_timing_dto.close_time

        if open_time is not None and close_time is not None:
            self.check_restaurant_timing_within_range(
                open_time=open_time, close_time=close_time)

        if open_time is not None:
            self.check_open_time_valid(
                open_time=open_time, id=update_restaurant_timing_dto.id)

        if close_time is not None:
            self.check_close_time_valid(
                close_time=close_time, id=update_restaurant_timing_dto.id)

        return self.restaurant_timing_storage.update_restaurant_timing(
            update_restaurant_timing_dto=update_restaurant_timing_dto)
