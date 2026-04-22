from account.interactors.dtos import AddressDTO
from account.storages.address_storage import AddressStorage


class ServiceInterface:
    def __init__(self):
        self.address_storage = AddressStorage()

    def get_address_by_id(self, address_id: int) -> AddressDTO:
        address_dto = self.address_storage.get_address_by_id(address_id)

        return address_dto
