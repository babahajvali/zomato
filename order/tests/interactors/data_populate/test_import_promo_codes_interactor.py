from unittest.mock import create_autospec, patch

import pytest

from order.exception.custom_exceptions import (
    AlreadyExistsPromoCode,
    DuplicatePromoCodes,
    EmptyPromoCodeFound,
    InvalidPromoCodeDateRange,
)
from order.interactors.populate_data.import_promo_codes import ImportPromoCodes
from order.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)
from order.tests.factories import CreatePromoCodeDTOFactory


class TestImportPromoCodes:
    def setup_method(self):
        self.promo_code_storage = create_autospec(PromoCodeStorageInterface)
        self.interactor = ImportPromoCodes(
            promo_code_storage=self.promo_code_storage,
        )

    def test_import_promo_codes_success(self):
        rows = [
            {
                "code": "SAVE50",
                "discount_type": "FLAT",
                "discount_value": "50",
                "min_order_value": "299",
                "max_usage": "100",
                "valid_from": "2026-04-17T10:30:00Z",
                "valid_until": "2026-04-30T23:59:59Z",
            }
        ]
        expected_dto = CreatePromoCodeDTOFactory(
            code="SAVE50",
            discount_type="FLAT",
            discount_value=50.0,
            min_order_value=299.0,
            max_usage=100,
            valid_from="2026-04-17T10:30:00Z",
            valid_until="2026-04-30T23:59:59Z",
        )

        self.promo_code_storage.get_existing_codes.return_value = []

        with patch(
            "order.interactors.populate_data.import_promo_codes.read_csv",
            return_value=rows,
        ):
            self.interactor.import_promo_codes(file_path="promo_codes.csv")

        self.promo_code_storage.get_existing_codes.assert_called_once_with(["SAVE50"])
        self.promo_code_storage.create_bulk_promo_codes.assert_called_once_with(
            [expected_dto]
        )

    def test_import_promo_codes_duplicate_codes(self):
        rows = [
            {
                "code": "SAVE50",
                "discount_type": "FLAT",
                "discount_value": "50",
                "min_order_value": "299",
                "max_usage": "100",
            },
            {
                "code": "SAVE50",
                "discount_type": "PERCENTAGE",
                "discount_value": "10",
                "min_order_value": "199",
                "max_usage": "50",
            },
        ]

        with patch(
            "order.interactors.populate_data.import_promo_codes.read_csv",
            return_value=rows,
        ):
            with pytest.raises(DuplicatePromoCodes) as exc:
                self.interactor.import_promo_codes(file_path="promo_codes.csv")

        assert exc.value.codes == ["SAVE50"]

    def test_import_promo_codes_already_exists(self):
        rows = [
            {
                "code": "SAVE50",
                "discount_type": "FLAT",
                "discount_value": "50",
                "min_order_value": "299",
                "max_usage": "100",
            }
        ]

        self.promo_code_storage.get_existing_codes.return_value = ["SAVE50"]

        with patch(
            "order.interactors.populate_data.import_promo_codes.read_csv",
            return_value=rows,
        ):
            with pytest.raises(AlreadyExistsPromoCode) as exc:
                self.interactor.import_promo_codes(file_path="promo_codes.csv")

        assert exc.value.codes == ["SAVE50"]
        self.promo_code_storage.create_bulk_promo_codes.assert_not_called()

    def test_check_empty_promo_codes_raises_exception(self):
        with pytest.raises(EmptyPromoCodeFound) as exc:
            self.interactor._check_empty_promo_codes(["SAVE50", ""])

        assert str(exc.value) == "1 Empty promo codes found"

    def test_import_promo_codes_invalid_date_range(self):
        rows = [
            {
                "code": "SAVE50",
                "discount_type": "FLAT",
                "discount_value": "50",
                "min_order_value": "299",
                "max_usage": "100",
                "valid_from": "2026-04-30T23:59:59Z",
                "valid_until": "2026-04-17T10:30:00Z",
            }
        ]

        self.promo_code_storage.get_existing_codes.return_value = []

        with patch(
            "order.interactors.populate_data.import_promo_codes.read_csv",
            return_value=rows,
        ):
            with pytest.raises(InvalidPromoCodeDateRange) as exc:
                self.interactor.import_promo_codes(file_path="promo_codes.csv")

        assert (
            str(exc.value)
            == "valid_until should be greater than valid_from in row SAVE50"
        )
        self.promo_code_storage.create_bulk_promo_codes.assert_not_called()
