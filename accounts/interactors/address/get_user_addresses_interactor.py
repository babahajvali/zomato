from typing import List

from accounts.interactors.dtos import AddressDTO
from accounts.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.mixin.user_mixin import UserMixin


# TODO: Fix file name and interactor name mismatch

# TODO: As there is only one module we dont need a package for address interactors.
class AddressesInteractor(UserMixin):
    def __init__(
        self,
        address_storage: AddressStorageInterface,
        user_storage: UserStorageInterface,
    ):
        super().__init__(user_storage=user_storage)
        self.address_storage = address_storage
        self.user_storage = user_storage

    def get_user_addresses(self, user_id: str) -> List[AddressDTO]:
        self.validate_user_exists(user_id=user_id)

        return self.address_storage.get_user_addresses(user_id=user_id)

    def get_address(self, address_id: int):
        # TODO: Here the input should have user_id as well right?
        return self.address_storage.get_address_by_id(address_id=address_id)


