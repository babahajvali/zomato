import datetime

from restaurant.Interactors.storage_interface.restaurant_timing_storage_interface import \
    RestaurantTimingStorageInterface
from restaurant.exception.custom_exceptions import \
    OpenTimeGreaterThanCloseTime, RestaurantTimingNotFound, \
    UserIsNotRestaurantOwner


class TimingMixin:

    def __init__(self,
                 restaurant_timing_storage: RestaurantTimingStorageInterface):
        self.restaurant_timing_storage = restaurant_timing_storage

    def check_restaurant_timing_valid(self, id: int):
        timing_data = self.restaurant_timing_storage.get_restaurant_timing(
            id=id)

        if timing_data is None:
            raise RestaurantTimingNotFound(id=id)

    def check_restaurant_owner_valid(self, id: int, user_id: str):

        owner_id = self.restaurant_timing_storage.is_restaurant_owner(id=id)
        if owner_id != user_id:
            raise UserIsNotRestaurantOwner(user_id=user_id)

    @staticmethod
    def check_restaurant_timing_within_range(
            open_time: datetime.datetime, close_time: datetime.datetime):
        if open_time > close_time:
            raise OpenTimeGreaterThanCloseTime(
                open_time=open_time, close_time=close_time)

    def check_open_time_valid(self, id: int, open_time: datetime.datetime):
        timing_data = self.restaurant_timing_storage.get_restaurant_timing(
            id=id)

        if open_time >= timing_data.close_time:
            raise OpenTimeGreaterThanCloseTime(
                open_time=open_time, close_time=timing_data.close_time)

    def check_close_time_valid(self, id: int, close_time: datetime.datetime):

        timing_data = self.restaurant_timing_storage.get_restaurant_timing(
            id=id)

        if close_time <= timing_data.open_time:
            raise OpenTimeGreaterThanCloseTime(
                open_time=timing_data.open_time, close_time=close_time
            )
