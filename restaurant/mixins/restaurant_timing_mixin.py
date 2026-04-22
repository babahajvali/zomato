import datetime
from typing import List, Optional

from restaurant.interactors.dtos import (
    BrowseRestaurantDTO,
    RestaurantTimingDTO,
    RestaurantDTO,
)
from restaurant.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from restaurant.exception.custom_exceptions import (
    OpenTimeGreaterThanCloseTime,
    RestaurantTimingNotFound,
    UserIsNotRestaurantOwner,
)


class TimingMixin:
    def __init__(
        self, restaurant_timing_storage: RestaurantTimingStorageInterface, **kwargs
    ):
        self.restaurant_timing_storage = restaurant_timing_storage
        super().__init__(**kwargs)

    def validate_restaurant_timing_exists(self, id: int):
        timing_data = self.restaurant_timing_storage.get_restaurant_timing(timing_id=id)

        if timing_data is None:
            raise RestaurantTimingNotFound(id=id)

    def validate_user_is_restaurant_owner_through_timing_id(
        self, id: int, user_id: str
    ):

        owner_id = self.restaurant_timing_storage.get_restaurant_owner_id(id=id)
        if owner_id != user_id:
            raise UserIsNotRestaurantOwner(user_id=user_id)

    @staticmethod
    def validate_restaurant_timing_within_range(
        open_time: datetime.time, close_time: datetime.time
    ):
        if open_time > close_time:
            raise OpenTimeGreaterThanCloseTime(
                open_time=open_time, close_time=close_time
            )

    def validate_restaurant_timings(
        self,
        timing_id: Optional[int],
        open_time: Optional[datetime.time],
        close_time: Optional[datetime.time],
    ):
        if open_time is not None and close_time is not None:
            self.validate_restaurant_timing_within_range(
                open_time=open_time, close_time=close_time
            )
        elif open_time is not None:
            self.validate_open_time_valid(timing_id=timing_id, open_time=open_time)
        elif close_time is not None:
            self.validate_close_time_valid(timing_id=timing_id, close_time=close_time)

    def validate_open_time_valid(self, timing_id: int, open_time: datetime.time):
        timing_data = self.restaurant_timing_storage.get_restaurant_timing(
            timing_id=timing_id
        )

        if open_time >= timing_data.close_time:
            raise OpenTimeGreaterThanCloseTime(
                open_time=open_time, close_time=timing_data.close_time
            )

    def validate_close_time_valid(self, timing_id: int, close_time: datetime.time):

        timing_data = self.restaurant_timing_storage.get_restaurant_timing(
            timing_id=timing_id
        )

        if close_time <= timing_data.open_time:
            raise OpenTimeGreaterThanCloseTime(
                open_time=timing_data.open_time, close_time=close_time
            )

    @staticmethod
    def compute_is_open_bulk(
        restaurants: List[RestaurantDTO],
        timings: List[RestaurantTimingDTO],
    ) -> List[BrowseRestaurantDTO]:

        now = datetime.datetime.now()
        day_of_week = now.isoweekday()
        current_time = now.time()

        browse_restaurants = []

        for each_restaurant in restaurants:
            restaurant = BrowseRestaurantDTO(
                restaurant_id=each_restaurant.id,
                name=each_restaurant.name,
                description=each_restaurant.description,
                pin_code=each_restaurant.pin_code,
                address=each_restaurant.address,
                is_veg_only=each_restaurant.is_veg_only,
                is_deleted=each_restaurant.is_deleted,
                average_rating=0.0,
                total_reviews=0,
                is_open=False,
                cuisine_type=each_restaurant.cuisine_type,
            )

            todays_timing = next(
                (
                    t
                    for t in timings
                    if t.restaurant_id == restaurant.restaurant_id
                    and t.day_of_week == day_of_week
                ),
                None,
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

            browse_restaurants.append(restaurant)
        return browse_restaurants
