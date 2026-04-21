from restaurant.exception import custom_exceptions
from restaurant.graphql.types.error_types import RestaurantNotFound
from restaurant.graphql.types.types import (
    RestaurantTimingsListType,
    RestaurantTimingType,
)
from restaurant.interactors.restaurant_timing.restaurant_timing_interactor import (
    RestaurantTimingInteractor,
)
from restaurant.storages.restaurant_storage import RestaurantStorage

from restaurant.storages.restaurant_timing_storage import RestaurantTimingStorage


def resolve_get_restaurant_timings(self, info, params):
    restaurant_timing_storage = RestaurantTimingStorage()
    restaurant_storage = RestaurantStorage()
    interactor = RestaurantTimingInteractor(
        restaurant_timing_storage=restaurant_timing_storage,
        restaurant_storage=restaurant_storage,
    )
    try:
        timings = interactor.get_restaurant_timings(restaurant_id=params.restaurant_id)

        return RestaurantTimingsListType(
            restaurant_id=params.restaurant_id,
            timings=[
                RestaurantTimingType(
                    id=timing.timing_id,
                    restaurant_id=timing.restaurant_id,
                    day_of_week=timing.day_of_week,
                    open_time=timing.open_time,
                    close_time=timing.close_time,
                )
                for timing in timings
            ],
        )

    except custom_exceptions.RestaurantNotFound as exc:
        return RestaurantNotFound(restaurant_id=exc.restaurant_id)
