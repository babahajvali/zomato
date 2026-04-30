import graphene

from orders.graphql.types.error_types import (
    PromoCodeUsageLimitReached,
    PromoCodeNotEligible,
    DeliveryUnavailableForAddress,
    AddressIdNotFound,
    RestaurantNotOpen,
    RestaurantClosed,
    PromoCodeNotFound,
    CartIsEmpty,
    InvalidOrderStatusTransition,
    OrderNotFound,
    OrderCancellationNotAllowed,
    OrderNotOwnedByUser,
    OrderCancellationWindowExpired,
    CustomerCartNotFound,
    MenuItemsUnavailable,
    PromoCodeExpired,
    PromoCodeNotYetValid,
    OrderAlreadyCancelled,
)
from orders.graphql.types.types import (
    OrderType,
    OrdersType,
    OrderSummaryType,
    PromoCodesType,
    OrderSummariesType,
)
from utils.graphql_types import UserNotRestaurantOwner


class PlaceOrderResponse(graphene.Union):
    class Meta:
        types = (
            OrderSummaryType,
            PromoCodeUsageLimitReached,
            PromoCodeNotEligible,
            DeliveryUnavailableForAddress,
            AddressIdNotFound,
            RestaurantNotOpen,
            RestaurantClosed,
            PromoCodeNotFound,
            CartIsEmpty,
            CustomerCartNotFound,
            MenuItemsUnavailable,
            PromoCodeExpired,
            PromoCodeNotYetValid,
        )


class UpdateOrderStatusResponse(graphene.Union):
    class Meta:
        types = (
            OrderType,
            OrderNotFound,
            UserNotRestaurantOwner,
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
            UserNotRestaurantOwner,
        )


class TodayRestaurantOrdersResponse(graphene.Union):
    class Meta:
        types = (
            OrderSummariesType,
            UserNotRestaurantOwner,
        )


class CancelOrderResponse(graphene.Union):
    class Meta:
        types = (
            OrderType,
            OrderNotFound,
            OrderNotOwnedByUser,
            OrderCancellationWindowExpired,
            OrderCancellationNotAllowed,
            OrderAlreadyCancelled,
        )


class AutoCancelOrderResponse(graphene.Union):
    class Meta:
        types = (
            OrderType,
            OrderNotFound,
            OrderCancellationNotAllowed,
        )


class GetAvailablePromoCodesResponse(graphene.Union):
    class Meta:
        types = (PromoCodesType,)
