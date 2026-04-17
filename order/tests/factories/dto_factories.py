import factory

from order.interactors.dtos import CreatePromoCodeDTO


class CreatePromoCodeDTOFactory(factory.Factory):
    class Meta:
        model = CreatePromoCodeDTO

    code = factory.Sequence(lambda n: f"CODE{n}")
    discount_type = "FLAT"
    discount_value = factory.Sequence(lambda n: float(n + 1))
    min_order_value = factory.Sequence(lambda n: float(n + 10))
    max_usage = factory.Sequence(lambda n: n + 1)
    valid_from = None
    valid_until = None

