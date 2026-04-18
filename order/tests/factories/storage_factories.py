from datetime import timedelta

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from order.models import PromoCode


class PromoCodeFactory(DjangoModelFactory):
    class Meta:
        model = PromoCode

    code = factory.Sequence(lambda n: f"CODE{n}")
    discount_type = "FLAT"
    discount_value = factory.Sequence(lambda n: float(n + 1))
    min_order_value = factory.Sequence(lambda n: float(n + 100))
    max_usage = factory.Sequence(lambda n: n + 1)
    valid_from = factory.LazyFunction(timezone.now)
    valid_until = factory.LazyAttribute(
        lambda obj: obj.valid_from + timedelta(days=7)
    )
