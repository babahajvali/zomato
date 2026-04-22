import graphene


class OrderType(graphene.ObjectType):
    order_id = graphene.String()
    customer_id = graphene.String()
    restaurant_id = graphene.String()
    promo_code_id = graphene.Int()
    status = graphene.String()
    items_total = graphene.Float()
    delivery_fee = graphene.Float()
    tax_fee = graphene.Float()
    final_amount = graphene.Float()
    address_id = graphene.Int()
    placed_at = graphene.String()


class OrdersType(graphene.ObjectType):
    orders = graphene.List(OrderType)
