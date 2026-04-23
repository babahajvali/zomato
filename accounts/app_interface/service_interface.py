from accounts.interactors.address.get_user_addresses_interactor import (
    AddressesInteractor,
)
from accounts.interactors.dtos import AddressDTO
from accounts.storages.address_storage import AddressStorage
from accounts.storages.user_storage import UserStorage


class ServiceInterface:
    def __init__(self):
        self.address_storage = AddressStorage()
        self.user_storage = UserStorage()

    def get_address_by_id(self, address_id: int) -> AddressDTO:
        interactor = AddressesInteractor(
            address_storage=self.address_storage,
            user_storage=self.user_storage,
        )

        return interactor.get_address(address_id=address_id)
