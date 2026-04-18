import graphene

from restaurant.graphql.types.error_types import \
    RestaurantTimingNoFoundTpe, OpenTimeGreaterThanCloseTimeType, \
    UserIsNotRestaurantOwnerType, RestaurantNotFoundType, \
    InvalidCategoriesFoundType, InvalidCuisineTypeExceptionType, \
    InvalidMinRatingExceptionType
from restaurant.graphql.types.types import \
    RestaurantTimingType, MenuItemsType, BrowseRestaurantsType


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


class BrowseRestaurantsResponse(graphene.Union):
    class Meta:
        types = (
            BrowseRestaurantsType,
            InvalidCuisineTypeExceptionType,
            InvalidMinRatingExceptionType,
        )
