import graphene


class PlaceOrderInputParams(graphene.InputObjectType):
    restaurant_id = graphene.String(required=True)
    address_id = graphene.Int(required=True)
    promo_code_id = graphene.Int(required=False, default_value=None)
