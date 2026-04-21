from order.exception.custom_exceptions import PromoCodeNotFound
from order.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)


class PromoCodeMixin:
    def __init__(self, promo_code_storage: PromoCodeStorageInterface):
        self.promo_code_storage = promo_code_storage

    def validate_promo_code_exist(self, promo_code_id: int):

        promo_code_dto = self.promo_code_storage.get_promo_code_by_id(
            promo_code_id=promo_code_id
        )

        if promo_code_dto is None:
            raise PromoCodeNotFound(promo_code_id=promo_code_id)
