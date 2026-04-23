from typing import List

from account.interactors.dtos import AddressDTO
from account.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from account.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from account.mixin.user_mixin import UserMixin


class GetUserAddressesInteractor(UserMixin):
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
