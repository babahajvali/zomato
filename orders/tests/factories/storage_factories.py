from datetime import timedelta

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from orders.constants.enums import OrderStatus
from orders.models import Order, OrderItem, PromoCode


class PromoCodeFactory(DjangoModelFactory):
    class Meta:
        model = PromoCode

    code = factory.Sequence(lambda n: f"CODE{n}")
    discount_type = "FLAT"
    discount_value = factory.Sequence(lambda n: float(n + 1))
    min_order_value = factory.Sequence(lambda n: float(n + 100))
    max_usage = factory.Sequence(lambda n: n + 1)
    valid_from = factory.LazyFunction(timezone.now)
    valid_until = factory.LazyAttribute(lambda obj: obj.valid_from + timedelta(days=7))


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    id = factory.Sequence(lambda n: f"order-{n}")
    customer_id = factory.Sequence(lambda n: f"00000000-0000-0000-0000-{n + 1:012d}")
    restaurant_id = factory.Sequence(
        lambda n: f"00000000-0000-0000-0000-{n + 101:012d}"
    )
    promo_code = factory.SubFactory(PromoCodeFactory)
    status = OrderStatus.PLACED.value
    items_total = 400.0
    delivery_fee = 30.0
    tax_fee = 20.0
    final_amount = 450.0
    address_id = 1


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    item_id = factory.Sequence(lambda n: f"item-{n}")
    quantity = 2
    item_price = 200.0
