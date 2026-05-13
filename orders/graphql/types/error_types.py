import graphene


class PromoCodeUsageLimitReached(graphene.ObjectType):
    max_usage_count = graphene.Int(required=True)


class PromoCodeNotEligible(graphene.ObjectType):
    # TODO: min_order_value is Decimal in the DTO but exposed here as Float — lossy and inconsistent with items_total below.
    min_order_value = graphene.Float(required=True)
    items_total = graphene.Decimal(required=True)


class DeliveryUnavailableForAddress(graphene.ObjectType):
    restaurant_id = graphene.String(required=True)
    pin_code = graphene.String(required=True)


class AddressIdNotFound(graphene.ObjectType):
    address_id = graphene.Int(required=True)


class RestaurantNotOpen(graphene.ObjectType):
    restaurant_id = graphene.String(required=True)
    day_of_week = graphene.Int(required=True)


class RestaurantClosed(graphene.ObjectType):
    restaurant_id = graphene.String(required=True)


class PromoCodeNotFound(graphene.ObjectType):
    # TODO: every other error type has required=True — inconsistent contract.
    promo_code_id = graphene.Int()


class CartIsEmpty(graphene.ObjectType):
    cart_id = graphene.String(required=True)


class OrderNotFound(graphene.ObjectType):
    order_id = graphene.String(required=True)


class InvalidOrderStatusTransition(graphene.ObjectType):
    current_status = graphene.String(required=True)
    new_status = graphene.String(required=True)
    allowed = graphene.List(graphene.String)


class OrderCancellationWindowExpired(graphene.ObjectType):
    order_id = graphene.String(required=True)
    minutes = graphene.Int(required=True)


class OrderCancellationNotAllowed(graphene.ObjectType):
    order_id = graphene.String(required=True)


class OrderNotOwnedByUser(graphene.ObjectType):
    order_id = graphene.String(required=True)


class CustomerCartNotFound(graphene.ObjectType):
    customer_id = graphene.String(required=True)


class MenuItemsUnavailable(graphene.ObjectType):
    unavailable_item_ids = graphene.List(graphene.String)


class PromoCodeExpired(graphene.ObjectType):
    code = graphene.String(required=True)


class PromoCodeNotYetValid(graphene.ObjectType):
    code = graphene.String(required=True)


class OrderAlreadyCancelled(graphene.ObjectType):
    order_id = graphene.String(required=True)
