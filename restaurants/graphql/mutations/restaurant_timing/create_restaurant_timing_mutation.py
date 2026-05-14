import graphene

from restaurants.exception import custom_exceptions
from restaurants.graphql.types.error_types import (
    RestaurantNotFound,
    InvalidTimingRange,
    InvalidDayOfWeek,
)
from restaurants.graphql.types.input_types import CreateRestaurantTimingInputParams
from restaurants.graphql.types.response_types import CreateRestaurantTimingResponse
from restaurants.graphql.types.types import RestaurantTimingType
from restaurants.interactors.dtos import CreateRestaurantTimingDTO
from restaurants.interactors.restaurant_timing.restaurant_timing_interactor import (
    RestaurantTimingInteractor,
)
from restaurants.storages.restaurant_storage import RestaurantStorage
from restaurants.storages.restaurant_timing_storage import RestaurantTimingStorage
from utils.graphql_types import UserNotRestaurantOwner


class CreateRestaurantTimingMutation(graphene.Mutation):
    class Arguments:
        params = CreateRestaurantTimingInputParams(required=True)

    Output = CreateRestaurantTimingResponse

    @staticmethod
    def mutate(root, info, params):
        restaurant_timing_storage = RestaurantTimingStorage()
        restaurant_storage = RestaurantStorage()

        interactor = RestaurantTimingInteractor(
            restaurant_storage=restaurant_storage,
            restaurant_timing_storage=restaurant_timing_storage,
        )

        # TODO: model uses CHOICES 1–7 but there's no app-layer guard on day_of_week — invalid values (0/8) only fail at Postgres-level integrity.
        create_timing_dto = CreateRestaurantTimingDTO(
            restaurant_id=params.restaurant_id,
            open_time=params.open_time,
            close_time=params.close_time,
            day_of_week=params.day_of_week,
        )

        try:
            result = interactor.create_restaurant_timing(
                create_restaurant_timing_dto=create_timing_dto,
                user_id=info.context.user_id,
            )

            return RestaurantTimingType(
                id=result.timing_id,
                restaurant_id=result.restaurant_id,
                day_of_week=result.day_of_week,
                close_time=result.close_time,
                open_time=result.open_time,
            )
        except custom_exceptions.RestaurantNotFound as e:
            return RestaurantNotFound(restaurant_id=e.restaurant_id)
        except custom_exceptions.UserNotRestaurantOwner as e:
            return UserNotRestaurantOwner(user_id=e.user_id)
        except custom_exceptions.InvalidTimingRange as e:
            return InvalidTimingRange(close_time=e.close_time, open_time=e.open_time)
        except custom_exceptions.InvalidDayOfWeek as e:
            return InvalidDayOfWeek(day_of_week=e.day_of_week)
