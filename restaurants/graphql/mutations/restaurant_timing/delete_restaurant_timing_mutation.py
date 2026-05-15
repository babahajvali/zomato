import graphene

from restaurants.exception import custom_exceptions
from restaurants.graphql.types.error_types import (
    RestaurantTimingNotFound,
)
from restaurants.graphql.types.input_types import DeleteRestaurantTimingInputParams
from restaurants.graphql.types.response_types import DeleteRestaurantTimingResponse
from restaurants.graphql.types.types import DeleteRestaurantTimingSuccessType
from restaurants.interactors.restaurant_timing.restaurant_timing_interactor import (
    RestaurantTimingInteractor,
)
from restaurants.storages.restaurant_storage import RestaurantStorage

from restaurants.storages.restaurant_timing_storage import RestaurantTimingStorage
from utils.graphql_types import UserNotRestaurantOwner
from utils.auth_decorators import require_auth


class DeleteRestaurantTimingMutation(graphene.Mutation):
    class Arguments:
        params = DeleteRestaurantTimingInputParams(required=True)

    Output = DeleteRestaurantTimingResponse

    @staticmethod
    @require_auth
    def mutate(root, info, params):
        restaurant_timing_storage = RestaurantTimingStorage()
        restaurant_storage = RestaurantStorage()
        interactor = RestaurantTimingInteractor(
            restaurant_timing_storage=restaurant_timing_storage,
            restaurant_storage=restaurant_storage,
        )
        try:
            interactor.delete_restaurant_timing(
                timing_id=params.timing_id, user_id=info.context.user_id
            )

            return DeleteRestaurantTimingSuccessType(
                timing_id=params.timing_id, success=True
            )

        except custom_exceptions.RestaurantTimingNotFound as exc:
            return RestaurantTimingNotFound(id=exc.id)

        except custom_exceptions.UserNotRestaurantOwner as exc:
            return UserNotRestaurantOwner(user_id=exc.user_id)
