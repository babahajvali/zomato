import graphene

from restaurants.graphql.types.error_types import (
    RestaurantTimingNotFound,
    OpenTimeGreaterThanCloseTime,
    RestaurantNotFound,
    InvalidCategoriesFound,
    InvalidCuisineTypeException,
    InvalidMinRating,
    CartNotFound,
    MenuItemNotFound,
    InvalidQuantity,
    CartItemNotFound,
    UserAlreadyReviewedRestaurant,
    InvalidRatingFound,
    InvalidDateRange,
)
from restaurants.graphql.types.types import (
    RestaurantTimingType,
    MenuItemsType,
    BrowseRestaurantsType,
    RestaurantMenuType,
    DeleteRestaurantTimingSuccessType,
    RestaurantTimingsListType,
    CartItemType,
    CartItemsType,
    RemoveCartItemSuccessType,
    ClearCartItemsSuccessType,
    ReviewType,
    RestaurantDashboardType,
)
from utils.graphql_types import UserIsNotRestaurantOwner


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
            InvalidCuisineTypeException,
            InvalidMinRating,
        )


class ViewRestaurantMenuResponse(graphene.Union):
    class Meta:
        types = (
            RestaurantMenuType,
            RestaurantNotFound,
        )


class UpdateCartItemResponse(graphene.Union):
    class Meta:
        types = (CartItemType, CartNotFound, MenuItemNotFound, InvalidQuantity)


class RemoveCartItemResponse(graphene.Union):
    class Meta:
        types = (
            RemoveCartItemSuccessType,
            CartItemNotFound,
        )


class ClearCartItemsResponse(graphene.Union):
    class Meta:
        types = (
            ClearCartItemsSuccessType,
            CartNotFound,
        )


class GetCartItemsResponse(graphene.Union):
    class Meta:
        types = (
            CartItemsType,
            CartNotFound,
        )


class CreateReviewResponse(graphene.Union):
    class Meta:
        types = (
            ReviewType,
            RestaurantNotFound,
            UserAlreadyReviewedRestaurant,
            InvalidRatingFound,
        )


class GetRestaurantDashboardResponse(graphene.Union):
    class Meta:
        types = (
            RestaurantDashboardType,
            RestaurantNotFound,
            InvalidDateRange,
            UserAlreadyReviewedRestaurant,
        )
