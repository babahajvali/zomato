from abc import ABC, abstractmethod
from typing import List

from account.interactors.dtos import CreateAddressDTO, AddressDTO


class AddressStorageInterface(ABC):
    @abstractmethod
    def get_existing_addresses(
        self, emails: List[str], labels: List[str]
    ) -> List[tuple]:
        pass

    @abstractmethod
    def create_bulk_addresses(self, addresses_dto: List[CreateAddressDTO]) -> List:
        pass

    @abstractmethod
    def get_address_by_id(self, address_id: int) -> AddressDTO:
        pass
