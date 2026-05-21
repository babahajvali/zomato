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
    InvalidOffset,
    InvalidLimit,
    CartNotBelongsToUser,
    InvalidDayOfWeek,
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
    ScoredRestaurantsType,
    ScoredItemsType,
    RestaurantSuggestionsType,
)
from utils.graphql_types import UserNotRestaurantOwner, UnauthorizedFound


class UpdateRestaurantTimingResponse(graphene.Union):
    class Meta:
        types = (
            RestaurantTimingType,
            RestaurantTimingNotFound,
            InvalidTimingRange,
            UserNotRestaurantOwner,
            UnauthorizedFound,
        )


class DeleteRestaurantTimingResponse(graphene.Union):
    class Meta:
        types = (
            DeleteRestaurantTimingSuccessType,
            RestaurantTimingNotFound,
            UserNotRestaurantOwner,
            UnauthorizedFound,
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
            UnauthorizedFound,
        )


class BrowseRestaurantsResponse(graphene.Union):
    class Meta:
        types = (
            BrowseRestaurantsType,
            InvalidCuisineTypeException,
            InvalidMinRating,
            InvalidLimit,
            InvalidOffset,
        )


class ViewRestaurantMenuResponse(graphene.Union):
    class Meta:
        types = (
            RestaurantMenuType,
            RestaurantNotFound,
        )


class UpdateCartItemResponse(graphene.Union):
    class Meta:
        types = (
            CartItemType,
            CartNotFound,
            MenuItemNotFound,
            InvalidQuantity,
            CartNotBelongsToUser,
            UnauthorizedFound,
        )


class RemoveCartItemResponse(graphene.Union):
    class Meta:
        types = (
            RemoveCartItemSuccessType,
            CartItemNotFound,
            CartNotFound,
            CartNotBelongsToUser,
            UnauthorizedFound,
        )


class ClearCartItemsResponse(graphene.Union):
    class Meta:
        types = (
            ClearCartItemsSuccessType,
            CartNotFound,
            CartNotBelongsToUser,
            UnauthorizedFound,
        )


class GetCartItemsResponse(graphene.Union):
    class Meta:
        types = (CartItemsType, CartNotFound, CartNotBelongsToUser)


class CreateReviewResponse(graphene.Union):
    class Meta:
        types = (
            ReviewType,
            RestaurantNotFound,
            RestaurantAlreadyReviewedByUser,
            InvalidRatingFound,
            UnauthorizedFound,
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
            InvalidDayOfWeek,
            UnauthorizedFound,
        )


class UpdateMenuItemResponse(graphene.Union):
    class Meta:
        types = (
            MenuItemType,
            MenuItemNotFound,
            UserNotRestaurantOwner,
            UnauthorizedFound,
        )


class DeleteMenuItemResponse(graphene.Union):
    class Meta:
        types = (
            DeleteMenuItemSuccessType,
            MenuItemNotFound,
            UserNotRestaurantOwner,
            UnauthorizedFound,
        )


class GetUserRestaurantReviewResponse(graphene.Union):
    class Meta:
        types = (ReviewType, RestaurantNotFound)


class GetOwnerRestaurantsResponse(graphene.Union):
    class Meta:
        types = (OwnerRestaurantsType, UnauthorizedFound)


class GetCustomerCartIdResponse(graphene.Union):
    class Meta:
        types = (CustomerCartIdType,)


class GetuserScoredRestaurantsResponse(graphene.Union):
    class Meta:
        types = (ScoredRestaurantsType, InvalidOffset, InvalidLimit)


class GetScoredItemsResponse(graphene.Union):
    class Meta:
        types = (
            ScoredItemsType,
            RestaurantNotFound,
        )


class SearchRestaurantsResponse(graphene.Union):
    class Meta:
        types = (RestaurantSuggestionsType,)
