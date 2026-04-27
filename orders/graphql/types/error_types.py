import graphene


class PromoCodeMaximumUsed(graphene.ObjectType):
    max_usage_count = graphene.Int(required=True)


class PromoCodeNotEligible(graphene.ObjectType):
    min_order_value = graphene.Float(required=True)
    items_total = graphene.Decimal(required=True)


class DeliveryNotAvailableForAddress(graphene.ObjectType):
    restaurant_id = graphene.String(required=True)
    pin_code = graphene.String(required=True)


class AddressIdNotFound(graphene.ObjectType):
    address_id = graphene.Int(required=True)


class RestaurantNotOpenNow(graphene.ObjectType):
    restaurant_id = graphene.String(required=True)
    day_of_week = graphene.Int(required=True)


class RestaurantClosed(graphene.ObjectType):
    restaurant_id = graphene.String(required=True)


class PromoCodeNotFound(graphene.ObjectType):
    promo_code_id = graphene.Int()


class EmptyCartItemsFound(graphene.ObjectType):
    cart_id = graphene.String(required=True)


class OrderNotFound(graphene.ObjectType):
    order_id = graphene.String(required=True)


class InvalidOrderStatusTransition(graphene.ObjectType):
    current_status = graphene.String(required=True)
    new_status = graphene.String(required=True)
    allowed = graphene.List(graphene.String)


class OrderCancellationTimeExceeded(graphene.ObjectType):
    order_id = graphene.String(required=True)


class OrderCannotBeCancelled(graphene.ObjectType):
    order_id = graphene.String(required=True)


class OrderNotBelongsToUser(graphene.ObjectType):
    order_id = graphene.String(required=True)


class CustomerCartNotFound(graphene.ObjectType):
    customer_id = graphene.String(required=True)
