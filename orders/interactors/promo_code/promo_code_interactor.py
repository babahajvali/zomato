from orders.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)


class PromoCodeInteractor:
    def __init__(self, promo_code_storage: PromoCodeStorageInterface):
        self.promo_code_storage = promo_code_storage

    def get_available_promo_codes(self):

        return self.promo_code_storage.get_available_promo_codes()
