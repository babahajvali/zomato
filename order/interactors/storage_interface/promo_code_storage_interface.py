from abc import ABC, abstractmethod
from typing import List

from order.interactors.dtos import CreatePromoCodeDTO


class PromoCodeStorageInterface(ABC):

    @abstractmethod
    def get_existing_codes(self, codes: List[str]) -> List[str]:
        pass

    @abstractmethod
    def create_bulk_promo_codes(self, promo_codes_dto: List[CreatePromoCodeDTO]) -> List:
        pass
