import graphene

from restaurant.graphql.types.error_types import (
    RestaurantTimingNotFound,
    OpenTimeGreaterThanCloseTime,
    RestaurantNotFound,
    InvalidCategoriesFound,
    InvalidCuisineTypeException,
    InvalidMinRatingException,
    CartNotFound,
    MenuItemNotFound,
    InvalidQuantity,
    CartItemNotFound,
)
from restaurant.graphql.types.types import (
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
            InvalidMinRatingException,
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
