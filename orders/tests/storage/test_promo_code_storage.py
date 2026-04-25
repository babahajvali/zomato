from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from orders.models import PromoCode
from orders.storages.promo_code_storage import PromoCodeStorage
from orders.tests.factories.dto_factories import CreatePromoCodeDTOFactory
from orders.tests.factories.storage_factories import PromoCodeFactory


class TestPromoCodeStorage(TestCase):
    def setUp(self):
        self.storage = PromoCodeStorage()

    def test_create_bulk_promo_codes_success(self):
        now = timezone.now()
        promo_codes_dto = [
            CreatePromoCodeDTOFactory(
                code="SAVE50",
                discount_type="FLAT",
                discount_value=50.0,
                min_order_value=299.0,
                max_usage=100,
                valid_from=now,
                valid_until=now + timedelta(days=7),
            )
        ]

        result = self.storage.create_bulk_promo_codes(promo_code_dtos=promo_codes_dto)

        assert len(result) == 1
        assert PromoCode.objects.filter(code="SAVE50").exists()

    def test_get_existing_codes(self):
        PromoCodeFactory(code="SAVE50")
        PromoCodeFactory(code="WELCOME10")

        result = self.storage.get_existing_codes(
            codes=["SAVE50", "NOT_EXIST"],
        )

        assert result == ["SAVE50"]

    def test_get_promo_code_by_id(self):
        promo_code = PromoCodeFactory(
            code="SAVE50",
            discount_type="FLAT",
            discount_value=50.0,
            min_order_value=299.0,
            max_usage=100,
        )

        result = self.storage.get_promo_code_by_id(promo_code_id=promo_code.id)

        assert result.promo_code_id == promo_code.id
        assert result.code == "SAVE50"
        assert result.discount_type == "FLAT"
        assert result.discount_value == 50.0
        assert result.min_order_value == 299.0
        assert result.max_usage == 100
