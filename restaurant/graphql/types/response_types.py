import graphene

from restaurant.graphql.types.error_types import \
    RestaurantTimingNotFoundType, OpenTimeGreaterThanCloseTimeType, \
    UserIsNotRestaurantOwnerType, RestaurantNotFoundType, \
    InvalidCategoriesFoundType, InvalidCuisineTypeExceptionType, \
    InvalidMinRatingExceptionType
from restaurant.graphql.types.types import \
    RestaurantTimingType, MenuItemsType, BrowseRestaurantsType, \
    RestaurantMenuType, DeleteRestaurantTimingSuccessType, \
    RestaurantTimingsListType


class UpdateRestaurantTimingResponse(graphene.Union):
    class Meta:
        types = (
            RestaurantTimingType,
            RestaurantTimingNotFoundType,
            OpenTimeGreaterThanCloseTimeType,
            UserIsNotRestaurantOwnerType,
        )


class DeleteRestaurantTimingResponse(graphene.Union):
    class Meta:
        types = (
            DeleteRestaurantTimingSuccessType,
            RestaurantTimingNotFoundType,
            UserIsNotRestaurantOwnerType,
        )


class GetRestaurantTimingsResponse(graphene.Union):
    class Meta:
        types = (
            RestaurantTimingsListType,
            RestaurantNotFoundType,
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

class ViewRestaurantMenuResponse(graphene.Union):
    class Meta:
        types = (
            RestaurantMenuType,
            RestaurantNotFoundType,
        )