import graphene

from restaurant.graphql.types.error_types import (
    RestaurantTimingNotFound,
    OpenTimeGreaterThanCloseTime,
    UserIsNotRestaurantOwner,
    RestaurantNotFound,
    InvalidCategoriesFound,
    InvalidCuisineTypeExceptionType,
    InvalidMinRatingExceptionType,
)
from restaurant.graphql.types.types import (
    RestaurantTimingType,
    MenuItemsType,
    BrowseRestaurantsType,
    RestaurantMenuType,
    DeleteRestaurantTimingSuccessType,
    RestaurantTimingsListType,
)


class UpdateRestaurantTimingResponse(graphene.Union):
    class Meta:
        types = (
            RestaurantTimingType,
            RestaurantTimingNotFound,
            OpenTimeGreaterThanCloseTime,
            UserIsNotRestaurantOwner,
        )


class DeleteRestaurantTimingResponse(graphene.Union):
    class Meta:
        types = (
            DeleteRestaurantTimingSuccessType,
            RestaurantTimingNotFound,
            UserIsNotRestaurantOwner,
        )


class GetRestaurantTimingsResponse(graphene.Union):
    class Meta:
        types = (
            RestaurantTimingsListType,
            RestaurantNotFound,
        )


class CreateMenuItemsResponse(graphene.Union):
    class Meta:
        types = (
            MenuItemsType,
            RestaurantNotFound,
            InvalidCategoriesFound,
            UserIsNotRestaurantOwner,
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
            RestaurantNotFound,
        )
