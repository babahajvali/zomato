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


class OrderNotFound(graphene.ObjectType):
    order_id = graphene.String()


class UserIsNotRestaurantOwner(graphene.ObjectType):
    user_id = graphene.String()


class InvalidOrderStatusTransition(graphene.ObjectType):
    current_status = graphene.String()
    new_status = graphene.String()
    allowed = graphene.List(graphene.String)


class OrderCancellationTimeExceeded(graphene.ObjectType):
    order_id = graphene.String()


class OrderCannotBeCancelled(graphene.ObjectType):
    order_id = graphene.String()


class OrderNotBelongsToUser(graphene.ObjectType):
    order_id = graphene.String()


class OrderCancellationTimeExceededType(graphene.ObjectType):
    order_id = graphene.String()


class OrderCannotBeCancelledType(graphene.ObjectType):
    order_id = graphene.String()


class OrderNotBelongsToUserType(graphene.ObjectType):
    order_id = graphene.String()


class OrderNotFoundType(graphene.ObjectType):
    order_id = graphene.String()
