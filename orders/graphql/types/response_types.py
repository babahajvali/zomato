import graphene

from orders.graphql.types.error_types import (
    PromoCodeMaximumUsed,
    PromoCodeNotEligible,
    DeliveryNotAvailableForAddress,
    AddressIdNotFound,
    RestaurantNotOpenNow,
    RestaurantClosed,
    PromoCodeNotFound,
    EmptyCartItemsFound,
    InvalidOrderStatusTransition,
    OrderNotFound,
    OrderCannotBeCancelled,
    OrderNotBelongsToUser,
    OrderCancellationTimeExceeded,
    CustomerCartNotFound,
)
from orders.graphql.types.types import (
    OrderType,
    OrdersType,
    OrderSummaryType,
    PromoCodesType,
)
from utils.graphql_types import UserIsNotRestaurantOwner


class PlaceOrderResponse(graphene.Union):
    class Meta:
        types = (
            OrderSummaryType,
            PromoCodeMaximumUsed,
            PromoCodeNotEligible,
            DeliveryNotAvailableForAddress,
            AddressIdNotFound,
            RestaurantNotOpenNow,
            RestaurantClosed,
            PromoCodeNotFound,
            EmptyCartItemsFound,
            CustomerCartNotFound,
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
            OrderSummaryType,
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


class GetAvailablePromoCodesResponse(graphene.Union):
    class Meta:
        types = (PromoCodesType,)
