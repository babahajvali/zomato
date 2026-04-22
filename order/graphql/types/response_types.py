import graphene

from order.graphql.types.error_types import (
    PromoCodeMaximumUsed,
    PromoCodeNotEligible,
    InvalidDeliveryZoneFound,
    InvalidAddressFound,
    RestaurantDayTimingNotFound,
    RestaurantClosed,
    PromoCodeNotFound,
    EmptyCartItemsFound,
    InvalidOrderStatusTransition,
    OrderNotFound,
    UserIsNotRestaurantOwner,
    OrderCancellationTimeExceededType,
    OrderCannotBeCancelledType,
    OrderNotBelongsToUserType,
    OrderNotFoundType,
)
from order.graphql.types.types import OrderType, OrdersType


class PlaceOrderResponse(graphene.Union):
    class Meta:
        types = (
            OrderType,
            PromoCodeMaximumUsed,
            PromoCodeNotEligible,
            InvalidDeliveryZoneFound,
            InvalidAddressFound,
            RestaurantDayTimingNotFound,
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
            OrderNotFoundType,
            OrderNotBelongsToUserType,
            OrderCancellationTimeExceededType,
            OrderCannotBeCancelledType,
        )


class AutoCancelOrderResponse(graphene.Union):
    class Meta:
        types = (
            OrderType,
            OrderNotFoundType,
            OrderCannotBeCancelledType,
        )
