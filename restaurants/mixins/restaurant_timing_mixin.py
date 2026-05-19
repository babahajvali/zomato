import datetime
from typing import List, Optional

from django.utils import timezone

from restaurants.interactors.dtos import (
    BrowseRestaurantDTO,
    RestaurantReviewSummaryDTO,
    RestaurantTimingDTO,
    RestaurantDTO,
)
from restaurants.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from restaurants.exception.custom_exceptions import (
    InvalidTimingRange,
    RestaurantTimingNotFound,
    UserNotRestaurantOwner,
    InvalidDayOfWeek,
)


class TimingMixin:
    @staticmethod
    def validate_restaurant_timing_exists(
        timing_id: int, restaurant_timing_storage: RestaurantTimingStorageInterface
    ) -> RestaurantTimingDTO:
        timing_data = restaurant_timing_storage.get_restaurant_timing(
            timing_id=timing_id
        )

        if timing_data is None:
            raise RestaurantTimingNotFound(id=timing_id)

        return timing_data

    @staticmethod
    def validate_user_is_restaurant_owner_through_timing_id(
        timing_id: int,
        user_id: str,
        restaurant_timing_storage: RestaurantTimingStorageInterface,
    ):

        owner_id = restaurant_timing_storage.get_restaurant_owner_id(
            timing_id=timing_id
        )
        if owner_id != user_id:
            raise UserNotRestaurantOwner(user_id=user_id)

    @staticmethod
    def validate_restaurant_timing_within_range(
        open_time: datetime.time, close_time: datetime.time
    ):
        if open_time > close_time:
            raise InvalidTimingRange(open_time=open_time, close_time=close_time)

    def validate_restaurant_timings(
        self,
        open_time: Optional[datetime.time],
        close_time: Optional[datetime.time],
        actual_open_time: datetime.time,
        actual_close_time: datetime.time,
    ):
        if open_time is not None and close_time is not None:
            self.validate_restaurant_timing_within_range(
                open_time=open_time, close_time=close_time
            )
        elif open_time is not None:
            self.validate_open_time(
                actual_close_time=actual_close_time, open_time=open_time
            )
        elif close_time is not None:
            self.validate_close_time(
                actual_open_time=actual_open_time, close_time=close_time
            )

    @staticmethod
    def validate_open_time(actual_close_time: datetime.time, open_time: datetime.time):

        if open_time >= actual_close_time:
            raise InvalidTimingRange(open_time=open_time, close_time=actual_close_time)

    @staticmethod
    def validate_close_time(actual_open_time: datetime.time, close_time: datetime.time):

        if close_time <= actual_open_time:
            raise InvalidTimingRange(open_time=actual_open_time, close_time=close_time)

    def compute_is_open_bulk(
        self,
        restaurants: List[RestaurantDTO],
        timings: List[RestaurantTimingDTO],
        review_summaries: List[RestaurantReviewSummaryDTO],
    ) -> List[BrowseRestaurantDTO]:

        now = timezone.localtime()
        day_of_week = now.isoweekday()
        current_time = now.time()
        review_summary_map = {
            summary.restaurant_id: summary for summary in review_summaries
        }

        browse_restaurants = []
        for restaurant in restaurants:
            todays_timing = self._get_todays_timing(timings, restaurant.id, day_of_week)
            is_open = self._check_is_open(todays_timing, current_time)
            review_summary = review_summary_map.get(str(restaurant.id))

            browse_restaurants.append(
                self._build_browse_restaurant_dto(restaurant, review_summary, is_open)
            )

        return browse_restaurants

    @staticmethod
    def _get_todays_timing(
        timings: List[RestaurantTimingDTO],
        restaurant_id: str,
        day_of_week: int,
    ) -> Optional[RestaurantTimingDTO]:
        return next(
            (
                t
                for t in timings
                if t.restaurant_id == restaurant_id and t.day_of_week == day_of_week
            ),
            None,
        )

    @staticmethod
    def _check_is_open(
        timing: Optional[RestaurantTimingDTO],
        current_time: datetime.time,
    ) -> bool:
        if not timing or not timing.open_time or not timing.close_time:
            return False

        if timing.open_time < timing.close_time:
            return timing.open_time <= current_time <= timing.close_time
        else:
            return current_time >= timing.open_time or current_time < timing.close_time

    @staticmethod
    def _build_browse_restaurant_dto(
        restaurant: RestaurantDTO,
        review_summary: Optional[RestaurantReviewSummaryDTO],
        is_open: bool,
    ) -> BrowseRestaurantDTO:
        return BrowseRestaurantDTO(
            restaurant_id=restaurant.id,
            name=restaurant.name,
            description=restaurant.description,
            pin_code=restaurant.pin_code,
            address=restaurant.address,
            is_veg_only=restaurant.is_veg_only,
            is_deleted=restaurant.is_deleted,
            average_rating=review_summary.average_rating if review_summary else 0.0,
            total_reviews=review_summary.total_reviews if review_summary else 0,
            is_open=is_open,
            cuisine_type=restaurant.cuisine_type,
        )

    @staticmethod
    def validate_day_of_week(day_of_week: int) -> None:
        if day_of_week < 0 or day_of_week > 7:
            raise InvalidDayOfWeek(day_of_week=day_of_week)
