import graphene

from restaurant.graphql.types.error_types import \
    RestaurantTimingNoFoundTpe, OpenTimeGreaterThanCloseTimeType, \
    UserIsNotRestaurantOwnerType, RestaurantNotFoundType, \
    InvalidCategoriesFoundType
from restaurant.graphql.types.types import \
    RestaurantTimingType, MenuItemsType


class UpdateRestaurantTimingResponse(graphene.Union):
    class Meta:
        types = (
            RestaurantTimingType,
            RestaurantTimingNoFoundTpe,
            OpenTimeGreaterThanCloseTimeType,
            UserIsNotRestaurantOwnerType,
        )


class CreateMenuItemsResponse(graphene.Union):
    class Meta:
        types = (
            MenuItemsType,
            RestaurantNotFoundType,
            InvalidCategoriesFoundType,
            UserIsNotRestaurantOwnerType,
        )