import factory
from datetime import datetime

from orders.constants.enums import OrderStatus
from orders.interactors.dtos import (
    CreateOrderDTO,
    CreateOrderItemDTO,
    CreatePromoCodeDTO,
    OrderDTO,
    OrderItemDTO,
    OrderItemSummaryDTO,
    OrderSummaryDTO,
    PlaceOrderDTO,
    PlaceScheduledOrderDTO,
    PromoCodeDTO,
    ScheduledOrderDTO,
)


class CreatePromoCodeDTOFactory(factory.Factory):
    class Meta:
        model = CreatePromoCodeDTO

    id = factory.Sequence(lambda n: n + 1)
    code = factory.Sequence(lambda n: f"CODE{n}")
    discount_type = "FLAT"
    discount_value = factory.Sequence(lambda n: float(n + 1))
    min_order_value = factory.Sequence(lambda n: float(n + 10))
    max_usage = factory.Sequence(lambda n: n + 1)
    valid_from = None
    valid_until = None


class PromoCodeDTOFactory(factory.Factory):
    class Meta:
        model = PromoCodeDTO

    promo_code_id = factory.Sequence(lambda n: n + 1)
    code = factory.Sequence(lambda n: f"CODE{n}")
    discount_type = "FLAT"
    discount_value = 50.0
    min_order_value = 100.0
    max_usage = 10
    valid_from = None
    valid_until = None


class PlaceOrderDTOFactory(factory.Factory):
    class Meta:
        model = PlaceOrderDTO

    customer_id = "00000000-0000-0000-0000-000000000001"
    restaurant_id = "00000000-0000-0000-0000-000000000002"
    promo_code_id = None
    address_id = 1


class CreateOrderDTOFactory(factory.Factory):
    class Meta:
        model = CreateOrderDTO

    customer_id = "00000000-0000-0000-0000-000000000001"
    restaurant_id = "00000000-0000-0000-0000-000000000002"
    promo_code_id = None
    status = OrderStatus.PLACED
    items_total = 400.0
    delivery_fee = 30.0
    tax_fee = 20.0
    final_amount = 450.0
    address_id = 1
    scheduled_for = None


class OrderDTOFactory(factory.Factory):
    class Meta:
        model = OrderDTO

    order_id = "00000000-0000-0000-0000-000000000003"
    customer_id = "00000000-0000-0000-0000-000000000001"
    restaurant_id = "00000000-0000-0000-0000-000000000002"
    promo_code_id = None
    status = OrderStatus.PLACED.value
    items_total = 400.0
    delivery_fee = 30.0
    tax_fee = 20.0
    final_amount = 450.0
    address_id = 1
    placed_at = factory.LazyFunction(datetime.now)
    scheduled_for = factory.LazyFunction(datetime.now)


class CreateOrderItemDTOFactory(factory.Factory):
    class Meta:
        model = CreateOrderItemDTO

    order_id = "00000000-0000-0000-0000-000000000003"
    item_id = "00000000-0000-0000-0000-000000000004"
    quantity = 2
    item_price = 200.0


class OrderItemSummaryDTOFactory(factory.Factory):
    class Meta:
        model = OrderItemSummaryDTO

    item_id = "00000000-0000-0000-0000-000000000004"
    quantity = 2
    item_price = 200.0
    subtotal = 400.0


class OrderItemDTOFactory(factory.Factory):
    class Meta:
        model = OrderItemDTO

    order_id = "00000000-0000-0000-0000-000000000003"
    item_id = "00000000-0000-0000-0000-000000000004"
    quantity = 2
    item_price = 200.0
    subtotal = 400.0


class OrderSummaryDTOFactory(factory.Factory):
    class Meta:
        model = OrderSummaryDTO

    order_id = "00000000-0000-0000-0000-000000000003"
    customer_id = "00000000-0000-0000-0000-000000000001"
    restaurant_id = "00000000-0000-0000-0000-000000000002"
    promo_code_id = None
    status = OrderStatus.PLACED
    items = factory.List([factory.SubFactory(OrderItemSummaryDTOFactory)])
    items_total = 400.0
    delivery_fee = 30.0
    tax_fee = 20.0
    final_amount = 450.0
    placed_at = factory.LazyFunction(datetime.now)
    address_id = 1


class PlaceScheduledOrderDTOFactory(factory.Factory):
    class Meta:
        model = PlaceScheduledOrderDTO

    customer_id = "00000000-0000-0000-0000-000000000001"
    restaurant_id = "00000000-0000-0000-0000-000000000002"
    address_id = 1
    scheduled_for = factory.LazyFunction(datetime.now)
    promo_code_id = None


class ScheduledOrderDTOFactory(factory.Factory):
    class Meta:
        model = ScheduledOrderDTO

    order_id = "00000000-0000-0000-0000-000000000003"
    customer_id = "00000000-0000-0000-0000-000000000001"
    restaurant_id = "00000000-0000-0000-0000-000000000002"
    promo_code_id = None
    scheduled_for = factory.LazyFunction(datetime.now)
    status = OrderStatus.SCHEDULED
    items = factory.List([factory.SubFactory(OrderItemSummaryDTOFactory)])
    items_total = 400.0
    delivery_fee = 30.0
    tax_fee = 20.0
    final_amount = 450.0
    placed_at = factory.LazyFunction(datetime.now)
    address_id = 1
