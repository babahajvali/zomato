import graphene


class PromoCodeMaximumUsed(graphene.ObjectType):
    max_usage_count = graphene.Int()


class PromoCodeNotEligible(graphene.ObjectType):
    min_order_value = graphene.Float()
    items_total = graphene.Float()


class InvalidDeliveryZoneFound(graphene.ObjectType):
    restaurant_id = graphene.String()
    pin_code = graphene.String()


class InvalidAddressFound(graphene.ObjectType):
    address_id = graphene.Int()


class RestaurantDayTimingNotFound(graphene.ObjectType):
    restaurant_id = graphene.String()
    day_of_week = graphene.Int()


class RestaurantClosed(graphene.ObjectType):
    restaurant_id = graphene.String()


class PromoCodeNotFound(graphene.ObjectType):
    promo_code_id = graphene.Int()


class EmptyCartItemsFound(graphene.ObjectType):
    cart_id = graphene.String()
