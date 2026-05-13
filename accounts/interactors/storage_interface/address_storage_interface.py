from abc import ABC, abstractmethod
from typing import List

from accounts.interactors.dtos import CreateAddressDTO, AddressDTO, AddressLookupDTO, \
    UpdateAddressDTO


class AddressStorageInterface(ABC):
    @abstractmethod
    def get_existing_addresses(self, pairs: List[AddressLookupDTO]) -> List[AddressDTO]:
        pass

    @abstractmethod
    def create_bulk_addresses(self, address_dtos: List[CreateAddressDTO]) -> List:
        pass

    @abstractmethod
    def get_address_by_id(self, address_id: int) -> AddressDTO:
        pass

    @abstractmethod
    def get_user_addresses(self, user_id: str) -> List[AddressDTO]:
        pass

    @abstractmethod
    def update_bulk_addresses(self, address_dtos: List[UpdateAddressDTO]):
        pass
