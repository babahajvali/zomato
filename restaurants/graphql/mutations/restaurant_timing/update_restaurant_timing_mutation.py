import graphene

from restaurants.exception import custom_exceptions
from restaurants.interactors.dtos import UpdateRestaurantTimingDTO
from restaurants.interactors.restaurant_timing.update_restaurant_timing_interactor import (
    UpdateRestaurantTimingInteractor,
)

from restaurants.graphql.types.error_types import (
    InvalidTimingRange,
    RestaurantTimingNotFound,
)
from restaurants.graphql.types.input_types import UpdateRestaurantTimingInputParams
from restaurants.graphql.types.response_types import UpdateRestaurantTimingResponse
from restaurants.graphql.types.types import RestaurantTimingType
from restaurants.storages.restaurant_timing_storage import RestaurantTimingStorage
from utils.graphql_types import UserNotRestaurantOwner
from utils.auth_decorators import require_auth


class UpdateRestaurantTimingMutation(graphene.Mutation):
    class Arguments:
        params = UpdateRestaurantTimingInputParams(required=True)

    Output = UpdateRestaurantTimingResponse

    @staticmethod
    @require_auth
    def mutate(root, info, params):
        restaurant_timing_storage = RestaurantTimingStorage()
        interactor = UpdateRestaurantTimingInteractor(
            restaurant_timing_storage=restaurant_timing_storage
        )
        try:
            update_restaurant_timing_dto = UpdateRestaurantTimingDTO(
                timing_id=params.timing_id,
                user_id=info.context.user_id,
                open_time=params.open_time,
                close_time=params.close_time,
            )
            result = interactor.update_restaurant_timing(
                update_restaurant_timing_dto=update_restaurant_timing_dto
            )

            return RestaurantTimingType(
                id=result.timing_id,
                restaurant_id=result.restaurant_id,
                day_of_week=result.day_of_week,
                open_time=result.open_time,
                close_time=result.close_time,
            )

        except custom_exceptions.RestaurantTimingNotFound as exc:
            return RestaurantTimingNotFound(id=exc.id)

        except custom_exceptions.InvalidTimingRange as exc:
            return InvalidTimingRange(
                open_time=exc.open_time,
                close_time=exc.close_time,
            )

        except custom_exceptions.UserNotRestaurantOwner as exc:
            return UserNotRestaurantOwner(user_id=exc.user_id)
