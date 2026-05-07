import graphene


class PlaceOrderInputParams(graphene.InputObjectType):
    restaurant_id = graphene.String(required=True)
    address_id = graphene.Int(required=True)
    promo_code_id = graphene.Int(required=False, default_value=None)


class PlaceScheduledOrderInputParams(graphene.InputObjectType):
    restaurant_id = graphene.String(required=True)
    address_id = graphene.Int(required=True)
    scheduled_for = graphene.DateTime(required=True)
    promo_code_id = graphene.Int(required=False, default_value=None)


class UpdateOrderStatusInputParams(graphene.InputObjectType):
    order_id = graphene.String(required=True)
    status = graphene.String(required=True)


class GetOrderInputParams(graphene.InputObjectType):
    order_id = graphene.String(required=True)


class GetRestaurantOrdersInputParams(graphene.InputObjectType):
    restaurant_id = graphene.String(required=True)
    limit = graphene.Int(required=True)
    offset = graphene.Int(required=True)


class GetUserOrdersInputParams(graphene.InputObjectType):
    limit = graphene.Int(required=True)
    offset = graphene.Int(required=True)


class GetUserScheduledOrdersInputParams(graphene.InputObjectType):
    limit = graphene.Int(required=True)
    offset = graphene.Int(required=True)


class GetTodayRestaurantOrdersInputParams(graphene.InputObjectType):
    restaurant_id = graphene.String(required=True)
    limit = graphene.Int(required=True)
    offset = graphene.Int(required=True)


class GetTodayRestaurantScheduledOrdersInputParams(graphene.InputObjectType):
    restaurant_id = graphene.String(required=True)
    limit = graphene.Int(required=True)
    offset = graphene.Int(required=True)


class CancelOrderInputParams(graphene.InputObjectType):
    order_id = graphene.String(required=True)
