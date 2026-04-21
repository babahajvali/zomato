from account.interactors.dtos import AddressDTO
from account.storages.address_storage import AddressStorage


class ServiceInterface:
    def __init__(self):
        self.address_storage = AddressStorage()

    def get_address_by_id(self, address_id: int) -> AddressDTO | None:
        address_dto = self.address_storage.get_address_by_id(address_id)
        if address_dto is None:
            return None

        return address_dto
