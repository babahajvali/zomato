from orders.exception.custom_exceptions import PromoCodeNotFound
from orders.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)


class PromoCodeMixin:
    @staticmethod
    def validate_promo_code_exist(
        promo_code_id: int, promo_code_storage: PromoCodeStorageInterface
    ):

        promo_code_dto = promo_code_storage.get_promo_code_by_id(
            promo_code_id=promo_code_id
        )

        if promo_code_dto is None:
            raise PromoCodeNotFound(promo_code_id=promo_code_id)
