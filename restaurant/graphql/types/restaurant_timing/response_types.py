import graphene

from restaurant.graphql.types.restaurant_timing.error_types import \
    RestaurantTimingNoFoundTpe, OpenTimeGreaterThanCloseTimeType, \
    UserIsNotRestaurantOwnerType
from restaurant.graphql.types.restaurant_timing.types import \
    RestaurantTimingType


class UpdateRestaurantTimingResponse(graphene.Union):
    class Meta:
        types = (
            RestaurantTimingType,
            RestaurantTimingNoFoundTpe,
            OpenTimeGreaterThanCloseTimeType,
            UserIsNotRestaurantOwnerType,
        )
