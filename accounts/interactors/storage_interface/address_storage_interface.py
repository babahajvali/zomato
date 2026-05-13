from abc import ABC, abstractmethod
from typing import List, Optional

from accounts.interactors.dtos import (
    CreateAddressDTO,
    AddressDTO,
    AddressLookupDTO,
    UpdateAddressDTO,
)


class AddressStorageInterface(ABC):
    @abstractmethod
    def get_existing_addresses(self, pairs: List[AddressLookupDTO]) -> List[AddressDTO]:
        pass

    @abstractmethod
    def create_bulk_addresses(self, address_dtos: List[CreateAddressDTO]) -> List:
        pass

    @abstractmethod
    def get_address_by_id(self, address_id: int, user_id: str) -> Optional[AddressDTO]:
        pass

    @abstractmethod
    def get_user_addresses(self, user_id: str) -> List[AddressDTO]:
        pass

    @abstractmethod
    def update_bulk_addresses(self, address_dtos: List[UpdateAddressDTO]):
        pass
