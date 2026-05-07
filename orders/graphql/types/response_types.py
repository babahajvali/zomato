import graphene

from orders.graphql.types.error_types import (
    PromoCodeUsageLimitReached,
    PromoCodeNotEligible,
    DeliveryUnavailableForAddress,
    AddressIdNotFound,
    RestaurantNotOpen,
    RestaurantClosed,
    ScheduledTimeTooSoon,
    RestaurantNotOpenAtScheduledTime,
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
    ScheduledOrderSummaryType,
    PromoCodesType,
    OrderSummariesType,
    ScheduledOrderSummariesType,
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


class PlaceScheduledOrderResponse(graphene.Union):
    class Meta:
        types = (
            ScheduledOrderSummaryType,
            PromoCodeUsageLimitReached,
            PromoCodeNotEligible,
            DeliveryUnavailableForAddress,
            AddressIdNotFound,
            ScheduledTimeTooSoon,
            RestaurantNotOpenAtScheduledTime,
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


class UserScheduledOrdersResponse(graphene.Union):
    class Meta:
        types = (ScheduledOrderSummariesType,)


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


class TodayRestaurantScheduledOrdersResponse(graphene.Union):
    class Meta:
        types = (
            ScheduledOrderSummariesType,
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


class GetAvailablePromoCodesResponse(graphene.Union):
    class Meta:
        types = (PromoCodesType,)
