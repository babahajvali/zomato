import graphene


class OrderType(graphene.ObjectType):
    order_id = graphene.String(required=True)
    customer_id = graphene.String(required=True)
    restaurant_id = graphene.String(required=True)
    promo_code_id = graphene.Int()
    status = graphene.String(required=True)
    items_total = graphene.Decimal(required=True)
    delivery_fee = graphene.Decimal(required=True)
    tax_fee = graphene.Decimal(required=True)
    final_amount = graphene.Decimal(required=True)
    address_id = graphene.Int(required=True)
    placed_at = graphene.String(required=True)


class OrdersType(graphene.ObjectType):
    orders = graphene.List(OrderType)
