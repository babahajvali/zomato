import graphene

from order.graphql.types.error_types import PromoCodeMaximumUsed, \
    PromoCodeNotEligible, InvalidDeliveryZoneFound, InvalidAddressFound, \
    RestaurantDayTimingNotFound, RestaurantClosed, PromoCodeNotFound
from order.graphql.types.types import OrderType


class PlaceOrderResponse(graphene.Union):
    class Meta:
        types=(
            OrderType,
            PromoCodeMaximumUsed,
            PromoCodeNotEligible,
            InvalidDeliveryZoneFound,
            InvalidAddressFound,
            RestaurantDayTimingNotFound,
            RestaurantClosed,
            PromoCodeNotFound,
        )

