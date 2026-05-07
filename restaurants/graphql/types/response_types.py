import graphene

from restaurants.graphql.types.error_types import (
    RestaurantTimingNotFound,
    InvalidTimingRange,
    RestaurantNotFound,
    InvalidCategories,
    InvalidCuisineTypeException,
    InvalidMinRating,
    CartNotFound,
    MenuItemNotFound,
    InvalidQuantity,
    CartItemNotFound,
    RestaurantAlreadyReviewedByUser,
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
    MenuItemType,
    DeleteMenuItemSuccessType,
    OwnerRestaurantsType,
    CustomerCartIdType,
)
from utils.graphql_types import UserNotRestaurantOwner


class UpdateRestaurantTimingResponse(graphene.Union):
    class Meta:
        types = (
            RestaurantTimingType,
            RestaurantTimingNotFound,
            InvalidTimingRange,
            UserNotRestaurantOwner,
        )


class DeleteRestaurantTimingResponse(graphene.Union):
    class Meta:
        types = (
            DeleteRestaurantTimingSuccessType,
            RestaurantTimingNotFound,
            UserNotRestaurantOwner,
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
            InvalidCategories,
            UserNotRestaurantOwner,
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
            RestaurantAlreadyReviewedByUser,
            InvalidRatingFound,
        )


class GetRestaurantDashboardResponse(graphene.Union):
    class Meta:
        types = (
            RestaurantDashboardType,
            RestaurantNotFound,
            InvalidDateRange,
            UserNotRestaurantOwner,
        )


class CreateRestaurantTimingResponse(graphene.Union):
    class Meta:
        types = (
            RestaurantTimingType,
            RestaurantNotFound,
            UserNotRestaurantOwner,
            InvalidTimingRange,
        )


class UpdateMenuItemResponse(graphene.Union):
    class Meta:
        types = (
            MenuItemType,
            MenuItemNotFound,
            UserNotRestaurantOwner,
        )


class DeleteMenuItemResponse(graphene.Union):
    class Meta:
        types = (
            DeleteMenuItemSuccessType,
            MenuItemNotFound,
            UserNotRestaurantOwner,
        )


class GetUserRestaurantReviewResponse(graphene.Union):
    class Meta:
        types = (ReviewType,)


class GetOwnerRestaurantsResponse(graphene.Union):
    class Meta:
        types = (OwnerRestaurantsType,)


class GetCustomerCartIdResponse(graphene.Union):
    class Meta:
        types = (CustomerCartIdType,)
