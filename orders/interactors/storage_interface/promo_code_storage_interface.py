from abc import ABC, abstractmethod
from typing import List

from orders.interactors.dtos import (
    CreatePromoCodeDTO,
    PromoCodeDTO,
    UpdatePromoCodeDTO,
)


class PromoCodeStorageInterface(ABC):
    @abstractmethod
    def get_existing_codes(self, codes: List[str]) -> List[str]:
        pass

    @abstractmethod
    def get_existing_promo_codes(self, codes: List[str]) -> List[PromoCodeDTO]:
        pass

    @abstractmethod
    def create_bulk_promo_codes(
        self, promo_code_dtos: List[CreatePromoCodeDTO]
    ) -> List:
        pass

    @abstractmethod
    def update_bulk_promo_codes(
        self, promo_code_dtos: List[UpdatePromoCodeDTO]
    ) -> List:
        pass

    @abstractmethod
    def get_promo_code_by_id(self, promo_code_id: int) -> PromoCodeDTO:
        pass

    @abstractmethod
    def get_available_promo_codes(self) -> List[PromoCodeDTO]:
        pass
