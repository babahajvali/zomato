import pytest
from order.models import PromoCode
from order.management.commands.import_promo_codes import import_promo_codes


class TestPromoCodeImport:

    @pytest.mark.django_db
    def test_creates_new_promo_codes(self, tmp_path):
        file = tmp_path / "promo.csv"

        file.write_text(
            "code,discount_type,discount_value,min_order_value,max_usage,valid_from,valid_until\n"
            "SAVE10,PERCENTAGE,10,100,50,2026-04-01 00:00:00,2026-04-30 23:59:59\n"
        )

        import_promo_codes(str(file))

        assert PromoCode.objects.count() == 1
        assert PromoCode.objects.filter(code="SAVE10").exists()

    @pytest.mark.django_db
    def test_updates_existing_promo_code(self, tmp_path):
        PromoCode.objects.create(
            code="SAVE10",
            discount_type="PERCENTAGE",
            discount_value=10,
            min_order_value=100,
            max_usage=50,
            valid_from="2026-04-01 00:00:00",
            valid_until="2026-04-30 23:59:59"
        )

        file = tmp_path / "promo.csv"

        file.write_text(
            "code,discount_type,discount_value,min_order_value,max_usage,valid_from,valid_until\n"
            "SAVE10,PERCENTAGE,20,200,100,2026-04-01 00:00:00,2026-04-30 23:59:59\n"
        )

        import_promo_codes(str(file))

        promo = PromoCode.objects.get(code="SAVE10")

        assert promo.discount_value == 20
        assert promo.min_order_value == 200

    @pytest.mark.django_db
    def test_skips_empty_code_rows(self, tmp_path):
        file = tmp_path / "promo.csv"

        file.write_text(
            "code,discount_type,discount_value,min_order_value,max_usage,valid_from,valid_until\n"
            ",PERCENTAGE,10,100,50,2026-04-01 00:00:00,2026-04-30 23:59:59\n"
        )

        import_promo_codes(str(file))

        assert PromoCode.objects.count() == 0

    @pytest.mark.django_db
    def test_multiple_promos_created(self, tmp_path):
        file = tmp_path / "promo.csv"

        file.write_text(
            "code,discount_type,discount_value,min_order_value,max_usage,valid_from,valid_until\n"
            "SAVE10,PERCENTAGE,10,100,50,2026-04-01 00:00:00,2026-04-30 23:59:59\n"
            "FLAT50,FLAT,50,200,30,2026-04-01 00:00:00,2026-04-30 23:59:59\n"
        )

        import_promo_codes(str(file))

        assert PromoCode.objects.count() == 2
