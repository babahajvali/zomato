import graphene

from restaurant.exception import custom_exceptions
from restaurant.graphql.types.error_types import (
    RestaurantTimingNotFound,
)
from restaurant.graphql.types.input_types import DeleteRestaurantTimingInputParams
from restaurant.graphql.types.response_types import DeleteRestaurantTimingResponse
from restaurant.graphql.types.types import DeleteRestaurantTimingSuccessType
from restaurant.interactors.restaurant_timing.restaurant_timing_interactor import (
    RestaurantTimingInteractor,
)
from restaurant.storages.restaurant_storage import RestaurantStorage

from restaurant.storages.restaurant_timing_storage import RestaurantTimingStorage
from utils.graphql_types import UserIsNotRestaurantOwner


class DeleteRestaurantTimingMutation(graphene.Mutation):
    class Arguments:
        params = DeleteRestaurantTimingInputParams(required=True)

    Output = DeleteRestaurantTimingResponse

    @staticmethod
    def mutate(root, info, params):
        restaurant_timing_storage = RestaurantTimingStorage()
        restaurant_storage = RestaurantStorage()
        interactor = RestaurantTimingInteractor(
            restaurant_timing_storage=restaurant_timing_storage,
            restaurant_storage=restaurant_storage,
        )
        try:
            interactor.delete_restaurant_timing(
                id=params.timing_id, user_id=info.context.user_id
            )

            return DeleteRestaurantTimingSuccessType(
                timing_id=params.timing_id, success=True
            )

        except custom_exceptions.RestaurantTimingNotFound as exc:
            return RestaurantTimingNotFound(id=exc.id)

        except custom_exceptions.UserIsNotRestaurantOwner as exc:
            return UserIsNotRestaurantOwner(user_id=exc.user_id)
