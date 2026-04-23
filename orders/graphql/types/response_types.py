import graphene

from orders.graphql.types.error_types import (
    PromoCodeMaximumUsed,
    PromoCodeNotEligible,
    DeliveryNotAvailableForAddress,
    InvalidAddressFound,
    RestaurantNotOpenNow,
    RestaurantClosed,
    PromoCodeNotFound,
    EmptyCartItemsFound,
    InvalidOrderStatusTransition,
    OrderNotFound,
    OrderCannotBeCancelled,
    OrderNotBelongsToUser,
    OrderCancellationTimeExceeded,
)
from orders.graphql.types.types import OrderType, OrdersType
from utils.graphql_types import UserIsNotRestaurantOwner


class PlaceOrderResponse(graphene.Union):
    class Meta:
        types = (
            OrderType,
            PromoCodeMaximumUsed,
            PromoCodeNotEligible,
            DeliveryNotAvailableForAddress,
            InvalidAddressFound,
            RestaurantNotOpenNow,
            RestaurantClosed,
            PromoCodeNotFound,
            EmptyCartItemsFound,
        )


class UpdateOrderStatusResponse(graphene.Union):
    class Meta:
        types = (
            OrderType,
            OrderNotFound,
            UserIsNotRestaurantOwner,
            InvalidOrderStatusTransition,
        )


class GetOrderResponse(graphene.Union):
    class Meta:
        types = (
            OrderType,
            OrderNotFound,
        )


class UserOrdersResponse(graphene.Union):
    class Meta:
        types = (OrdersType,)


class RestaurantOrdersResponse(graphene.Union):
    class Meta:
        types = (
            OrdersType,
            UserIsNotRestaurantOwner,
        )


class TodayRestaurantOrdersResponse(graphene.Union):
    class Meta:
        types = (
            OrdersType,
            UserIsNotRestaurantOwner,
        )


class CancelOrderResponse(graphene.Union):
    class Meta:
        types = (
            OrderType,
            OrderNotFound,
            OrderNotBelongsToUser,
            OrderCancellationTimeExceeded,
            OrderCannotBeCancelled,
        )


class AutoCancelOrderResponse(graphene.Union):
    class Meta:
        types = (
            OrderType,
            OrderNotFound,
            OrderCannotBeCancelled,
        )
