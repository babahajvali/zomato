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


class ScheduledOrderType(graphene.ObjectType):
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
    scheduled_for = graphene.DateTime(required=True)


class OrderItemType(graphene.ObjectType):
    item_id = graphene.String(required=True)
    quantity = graphene.Int(required=True)
    item_price = graphene.Decimal(required=True)
    subtotal = graphene.Decimal(required=True)


class OrderSummaryType(graphene.ObjectType):
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
    items = graphene.List(OrderItemType)


class ScheduledOrderSummaryType(graphene.ObjectType):
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
    scheduled_for = graphene.DateTime(required=True)
    items = graphene.List(OrderItemType)


class OrderSummariesType(graphene.ObjectType):
    order_summaries = graphene.List(OrderSummaryType)


class ScheduledOrderSummariesType(graphene.ObjectType):
    order_summaries = graphene.List(ScheduledOrderSummaryType)


class OrdersType(graphene.ObjectType):
    orders = graphene.List(OrderType)


class ScheduledOrdersType(graphene.ObjectType):
    orders = graphene.List(ScheduledOrderType)


class PromoCodeType(graphene.ObjectType):
    promo_code_id = graphene.Int(required=True)
    code = graphene.String(required=True)
    discount_type = graphene.String(required=True)
    discount_value = graphene.Decimal(required=True)
    min_order_value = graphene.Decimal(required=True)
    max_usage = graphene.Int(required=True)
    valid_from = graphene.DateTime(required=True)
    valid_until = graphene.DateTime(required=True)


class PromoCodesType(graphene.ObjectType):
    promo_codes = graphene.List(PromoCodeType)
