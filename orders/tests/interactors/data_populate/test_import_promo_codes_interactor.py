from unittest.mock import create_autospec, patch

import pytest

from orders.exception.custom_exceptions import (
    PromoCodeAlreadyExists,
    DuplicatePromoCodes,
    EmptyPromoCode,
    InvalidPromoCodeDateRange,
)
from orders.interactors.populate_data.import_promo_codes import ImportPromoCodes
from orders.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)
from orders.tests.factories import CreatePromoCodeDTOFactory


READ_CSV = "orders.interactors.populate_data.import_promo_codes.read_csv"


class TestImportPromoCodes:
    def setup_method(self):
        self.promo_code_storage = create_autospec(PromoCodeStorageInterface)
        self.interactor = ImportPromoCodes(
            promo_code_storage=self.promo_code_storage,
        )

    @patch(READ_CSV)
    def test_import_promo_codes_success(self, mock_read_csv):
        rows = [
            {
                "id": "1",
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
            id=1,
            code="SAVE50",
            discount_type="FLAT",
            discount_value=50.0,
            min_order_value=299.0,
            max_usage=100,
            valid_from="2026-04-17T10:30:00Z",
            valid_until="2026-04-30T23:59:59Z",
        )
        mock_read_csv.return_value = rows

        self.promo_code_storage.get_existing_codes.return_value = []

        self.interactor.import_promo_codes(file_path="promo_codes.csv")

        self.promo_code_storage.get_existing_codes.assert_called_once_with(["SAVE50"])
        self.promo_code_storage.create_bulk_promo_codes.assert_called_once_with(
            [expected_dto]
        )

    @patch(READ_CSV)
    def test_import_promo_codes_duplicate_codes(self, mock_read_csv):
        rows = [
            {
                "id": "1",
                "code": "SAVE50",
                "discount_type": "FLAT",
                "discount_value": "50",
                "min_order_value": "299",
                "max_usage": "100",
                "valid_from": "2026-04-17T10:30:00Z",
                "valid_until": "2026-04-30T23:59:59Z",
            },
            {
                "id": "2",
                "code": "SAVE50",
                "discount_type": "PERCENTAGE",
                "discount_value": "10",
                "min_order_value": "199",
                "max_usage": "50",
                "valid_from": "2026-04-18T10:30:00Z",
                "valid_until": "2026-05-01T23:59:59Z",
            },
        ]
        mock_read_csv.return_value = rows

        with pytest.raises(DuplicatePromoCodes) as exc:
            self.interactor.import_promo_codes(file_path="promo_codes.csv")

        assert exc.value.codes == ["SAVE50"]

    @patch(READ_CSV)
    def test_import_promo_codes_already_exists(self, mock_read_csv):
        rows = [
            {
                "id": "1",
                "code": "SAVE50",
                "discount_type": "FLAT",
                "discount_value": "50",
                "min_order_value": "299",
                "max_usage": "100",
                "valid_from": "2026-04-17T10:30:00Z",
                "valid_until": "2026-04-30T23:59:59Z",
            }
        ]
        mock_read_csv.return_value = rows

        self.promo_code_storage.get_existing_codes.return_value = ["SAVE50"]

        with pytest.raises(PromoCodeAlreadyExists) as exc:
            self.interactor.import_promo_codes(file_path="promo_codes.csv")

        assert exc.value.codes == ["SAVE50"]
        self.promo_code_storage.create_bulk_promo_codes.assert_not_called()

    def test_check_empty_promo_codes_raises_exception(self):
        with pytest.raises(EmptyPromoCode) as exc:
            self.interactor._validate_empty_promo_codes(["SAVE50", ""])

        assert str(exc.value) == "1 Empty promo codes found"

    @patch(READ_CSV)
    def test_import_promo_codes_invalid_date_range(self, mock_read_csv):
        rows = [
            {
                "id": "1",
                "code": "SAVE50",
                "discount_type": "FLAT",
                "discount_value": "50",
                "min_order_value": "299",
                "max_usage": "100",
                "valid_from": "2026-04-30T23:59:59Z",
                "valid_until": "2026-04-17T10:30:00Z",
            }
        ]
        mock_read_csv.return_value = rows

        self.promo_code_storage.get_existing_codes.return_value = []

        with pytest.raises(InvalidPromoCodeDateRange) as exc:
            self.interactor.import_promo_codes(file_path="promo_codes.csv")

        assert (
            str(exc.value)
            == "valid_until should be greater than valid_from in row 1 (code: SAVE50)"
        )
        self.promo_code_storage.create_bulk_promo_codes.assert_not_called()
