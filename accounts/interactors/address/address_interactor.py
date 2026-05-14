from typing import List

from accounts.interactors.dtos import AddressDTO, CreateAddressDTO, UpdateAddressDTO
from accounts.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.mixin.user_mixin import UserMixin
from utils.caching_decorators import interactor_cache


class AddressInteractor(UserMixin):
    def __init__(
        self,
        address_storage: AddressStorageInterface,
        user_storage: UserStorageInterface,
    ):
        super().__init__(user_storage=user_storage)
        self.address_storage = address_storage
        self.user_storage = user_storage

    @interactor_cache(cache_name="get_user_addresses", timeout=10 * 60)
    def get_user_addresses(self, user_id: str) -> List[AddressDTO]:
        self.validate_user_exists(user_id=user_id)

        return self.address_storage.get_user_addresses(user_id=user_id)

    def get_address(self, address_id: int, user_id: str) -> AddressDTO:
        self.validate_user_exists(user_id=user_id)

        return self.address_storage.get_address_by_id(
            address_id=address_id, user_id=user_id
        )

    def create_bulk_addresses(
        self, create_address_dtos: List[CreateAddressDTO]
    ) -> List[AddressDTO]:

        return self.address_storage.create_bulk_addresses(
            address_dtos=create_address_dtos
        )

    def update_bulk_addresses(self, update_address_dtos: List[UpdateAddressDTO]):

        return self.address_storage.update_bulk_addresses(
            address_dtos=update_address_dtos
        )
