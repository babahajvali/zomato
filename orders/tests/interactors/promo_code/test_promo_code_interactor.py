from unittest.mock import create_autospec

from orders.interactors.promo_code.promo_code_interactor import PromoCodeInteractor
from orders.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)
from orders.tests.factories import PromoCodeDTOFactory


class TestPromoCodeInteractor:
    def setup_method(self):
        self.promo_code_storage = create_autospec(PromoCodeStorageInterface)
        self.interactor = PromoCodeInteractor(
            promo_code_storage=self.promo_code_storage
        )

    def test_get_available_promo_codes_success(self):
        promo_codes = [
            PromoCodeDTOFactory(promo_code_id=1, code="WELCOME50"),
            PromoCodeDTOFactory(promo_code_id=2, code="SAVE10"),
        ]
        self.promo_code_storage.get_available_promo_codes.return_value = promo_codes

        result = self.interactor.get_available_promo_codes()

        assert result == promo_codes
        self.promo_code_storage.get_available_promo_codes.assert_called_once_with()

    def test_get_available_promo_codes_returns_empty_list(self):
        self.promo_code_storage.get_available_promo_codes.return_value = []

        result = self.interactor.get_available_promo_codes()

        assert result == []
        self.promo_code_storage.get_available_promo_codes.assert_called_once_with()
