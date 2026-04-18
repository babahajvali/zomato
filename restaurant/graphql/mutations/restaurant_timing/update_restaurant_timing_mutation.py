import graphene

from restaurant.interactors.dtos import UpdateRestaurantTimingDTO
from restaurant.interactors.restaurant_timing.update_restaurant_timing_interactor import \
    UpdateRestaurantTimingInteractor
from restaurant.exception.custom_exceptions import (
    OpenTimeGreaterThanCloseTime,
    RestaurantTimingNotFound,
    UserIsNotRestaurantOwner,
)
from restaurant.graphql.types.error_types import (
    OpenTimeGreaterThanCloseTimeType,
    RestaurantTimingNoFoundTpe,
    UserIsNotRestaurantOwnerType,
)
from restaurant.graphql.types.input_types import \
    UpdateRestaurantTimingInputParams
from restaurant.graphql.types.response_types import \
    UpdateRestaurantTimingResponse
from restaurant.graphql.types.types import \
    RestaurantTimingType
from restaurant.storages.restaurant_timing_storage import \
    RestaurantTimingStorage


class UpdateRestaurantTimingMutation(graphene.Mutation):

    class Arguments:
        params = UpdateRestaurantTimingInputParams(required=True)

    Output = UpdateRestaurantTimingResponse

    @staticmethod
    def mutate(root, info, params):
        restaurant_timing_storage = RestaurantTimingStorage()
        interactor = UpdateRestaurantTimingInteractor(
            restaurant_timing_storage=restaurant_timing_storage
        )
        try:
            update_restaurant_timing_dto = UpdateRestaurantTimingDTO(
                id=params.id,
                user_id=info.context.user_id,
                open_time=params.open_time,
                close_time=params.close_time,
            )
            result = interactor.update_restaurant_timing(
                update_restaurant_timing_dto=update_restaurant_timing_dto
            )

            return RestaurantTimingType(
                id=result.id,
                restaurant_id=result.restaurant_id,
                day_of_week=result.day_of_week,
                open_time=result.open_time,
                close_time=result.close_time,
            )

        except RestaurantTimingNotFound as exc:
            return RestaurantTimingNoFoundTpe(id=exc.id)

        except OpenTimeGreaterThanCloseTime as exc:
            return OpenTimeGreaterThanCloseTimeType(
                open_time=exc.open_time,
                close_time=exc.close_time,
            )

        except UserIsNotRestaurantOwner as exc:
            return UserIsNotRestaurantOwnerType(user_id=exc.user_id)

