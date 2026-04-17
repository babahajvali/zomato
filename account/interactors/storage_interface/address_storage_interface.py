from abc import ABC, abstractmethod
from typing import List

from account.interactors.dtos import CreateAddressDTO


class AddressStorageInterface(ABC):

    @abstractmethod
    def get_existing_addresses(self, emails: List[str], labels: List[str]) -> List[tuple]:
        pass

    @abstractmethod
    def create_bulk_addresses(self, addresses_dto: List[CreateAddressDTO]) -> List:
        pass
