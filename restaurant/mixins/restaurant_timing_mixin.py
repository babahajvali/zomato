import datetime
from typing import List

from restaurant.interactors.dtos import BrowseRestaurantDTO, \
    RestaurantTimingDTO
from restaurant.interactors.storage_interface.restaurant_timing_storage_interface import \
    RestaurantTimingStorageInterface
from restaurant.exception.custom_exceptions import \
    OpenTimeGreaterThanCloseTime, RestaurantTimingNotFound, \
    UserIsNotRestaurantOwner


class TimingMixin:

    def __init__(self,
                 restaurant_timing_storage: RestaurantTimingStorageInterface, **kwargs):
        self.restaurant_timing_storage = restaurant_timing_storage
        super().__init__(**kwargs)

    def check_restaurant_timing_valid(self, id: int):
        timing_data = self.restaurant_timing_storage.get_restaurant_timing(
            id=id)

        if timing_data is None:
            raise RestaurantTimingNotFound(id=id)

    def check_user_is_restaurant_owner(self, id: int, user_id: str):

        owner_id = self.restaurant_timing_storage.get_restaurant_owner_id(id=id)
        if owner_id != user_id:
            raise UserIsNotRestaurantOwner(user_id=user_id)

    @staticmethod
    def check_restaurant_timing_within_range(
            open_time: datetime.time, close_time: datetime.time):
        if open_time > close_time:
            raise OpenTimeGreaterThanCloseTime(
                open_time=open_time, close_time=close_time)

    def check_open_time_valid(self, id: int, open_time: datetime.time):
        timing_data = self.restaurant_timing_storage.get_restaurant_timing(
            id=id)

        if open_time >= timing_data.close_time:
            raise OpenTimeGreaterThanCloseTime(
                open_time=open_time, close_time=timing_data.close_time)

    def check_close_time_valid(self, id: int, close_time: datetime.time):

        timing_data = self.restaurant_timing_storage.get_restaurant_timing(
            id=id)

        if close_time <= timing_data.open_time:
            raise OpenTimeGreaterThanCloseTime(
                open_time=timing_data.open_time, close_time=close_time
            )

    @staticmethod
    def compute_is_open_bulk(
            restaurants: List[BrowseRestaurantDTO],
            timings: List[RestaurantTimingDTO],
    ) -> None:

        now = datetime.datetime.now()
        day_of_week = now.isoweekday()
        current_time = now.time()

        for restaurant in restaurants:

            todays_timing = next(
                (
                    t for t in timings
                    if t.restaurant_id == restaurant.restaurant_id
                       and t.day_of_week == day_of_week
                ),
                None
            )

            if not todays_timing:
                restaurant.is_open = False
                continue

            if not todays_timing.open_time or not todays_timing.close_time:
                restaurant.is_open = False
                continue

            restaurant.is_open = (
                    todays_timing.open_time <= current_time <= todays_timing.close_time
            )
