from typing import List

from django.db import transaction

from accounts.exception.custom_exceptions import (
    AddressAlreadyExists,
    DuplicateAddresses,
    InvalidUsersFound,
    AddressNotBelongsToUser,
    AddressNotFound,
)
from accounts.interactors.dtos import (
    AddressDTO,
    CreateAddressDTO,
    UpdateAddressDTO,
    AddressLookupDTO,
)
from accounts.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.mixin.user_mixin import UserMixin
from utils.caching_decorators import interactor_cache, invalidate_interactor_cache


class AddressInteractor(UserMixin):
    def __init__(
        self,
        address_storage: AddressStorageInterface,
        user_storage: UserStorageInterface,
    ):
        self.address_storage = address_storage
        self.user_storage = user_storage

    @interactor_cache(cache_name="get_user_addresses", timeout=10 * 60)
    def get_user_addresses(self, user_id: str) -> List[AddressDTO]:
        self.validate_user_exists(user_id=user_id, user_storage=self.user_storage)

        return self.address_storage.get_user_addresses(user_id=user_id)

    @invalidate_interactor_cache(cache_name="get_user_addresses")
    def create_address(self, create_address_dto: CreateAddressDTO) -> AddressDTO:
        self.validate_user_exists(
            user_id=create_address_dto.user_id, user_storage=self.user_storage
        )
        self._validate_address_not_exists(create_address_dto=create_address_dto)

        return self.address_storage.create_address(address_dto=create_address_dto)

    def get_address(self, address_id: int, user_id: str) -> AddressDTO:
        self.validate_user_exists(user_id=user_id, user_storage=self.user_storage)

        address_dto = self._validate_address(address_id=address_id)
        self._validate_address_belongs_to_user(address_dto=address_dto, user_id=user_id)

        return address_dto

    @transaction.atomic
    def create_or_update_bulk_addresses(
        self, create_address_dtos: List[CreateAddressDTO]
    ) -> str:

        address_pairs = self._get_user_label_pincode_pairs(
            address_dtos=create_address_dtos
        )
        user_ids = [addr.user_id for addr in create_address_dtos]
        self._validate_users(user_ids=user_ids)

        self._validate_duplicate_addresses(address_pairs=address_pairs)
        to_create, to_update = self._split_new_and_existing(
            address_dtos=create_address_dtos, address_pairs=address_pairs
        )
        created_addresses = []
        updated_addresses = []
        if to_create:
            created_addresses = self.address_storage.create_bulk_addresses(
                address_dtos=to_create
            )

        if to_update:
            updated_addresses = self.address_storage.update_bulk_addresses(
                address_dtos=to_update
            )

        return f"{len(created_addresses)} created and {len(updated_addresses)} updated address!!!"

    @staticmethod
    def _validate_address_belongs_to_user(address_dto: AddressDTO, user_id: str):

        if address_dto.user_id != user_id:
            raise AddressNotBelongsToUser(
                user_id=user_id, address_id=address_dto.address_id
            )

    def _validate_address_not_exists(self, create_address_dto: CreateAddressDTO):
        address_pairs = self._get_user_label_pincode_pairs(
            address_dtos=[create_address_dto]
        )
        existing_addresses = self.address_storage.get_existing_addresses(
            address_pairs=address_pairs
        )

        if existing_addresses:
            raise AddressAlreadyExists(
                addresses=[(create_address_dto.label, create_address_dto.pincode)]
            )

    def _validate_address(self, address_id: int) -> AddressDTO:
        address_dto = self.address_storage.get_address_by_id(address_id=address_id)
        if address_dto is None:
            raise AddressNotFound(address_id=address_id)

        return address_dto

    @staticmethod
    def _validate_duplicate_addresses(
        address_pairs: List[AddressLookupDTO],
    ):
        seen = set()
        duplicates = []

        for pair in address_pairs:
            key = (pair.user_id, pair.label, pair.pincode)
            if key in seen:
                duplicates.append(pair)
            seen.add(key)

        if duplicates:
            raise DuplicateAddresses(addresses=duplicates)

    def _split_new_and_existing(
        self,
        address_dtos: List[CreateAddressDTO],
        address_pairs: List[AddressLookupDTO],
    ) -> tuple[List[CreateAddressDTO], List[UpdateAddressDTO]]:

        existing_addresses = self.address_storage.get_existing_addresses(
            address_pairs=address_pairs
        )

        existing_lookup = {
            (addr.user_id, addr.label, addr.pincode): addr.address_id
            for addr in existing_addresses
        }

        to_create = []
        to_update = []

        for dto in address_dtos:
            key = (dto.user_id, dto.label, dto.pincode)
            if key in existing_lookup:
                address_id = existing_lookup[key]
                update_dto = self._build_update_address_dto(
                    address_dto=dto,
                    address_id=address_id,
                )
                to_update.append(update_dto)
            else:
                to_create.append(dto)

        return to_create, to_update

    @staticmethod
    def _build_update_address_dto(
        address_dto: CreateAddressDTO, address_id: int
    ) -> UpdateAddressDTO:
        return UpdateAddressDTO(
            id=address_id,
            user_id=address_dto.user_id,
            label=address_dto.label,
            pincode=address_dto.pincode,
            full_address=address_dto.full_address,
            is_default=address_dto.is_default,
            city=address_dto.city,
        )

    @staticmethod
    def _get_user_label_pincode_pairs(
        address_dtos: List[CreateAddressDTO],
    ) -> List[AddressLookupDTO]:

        pairs = []

        for address in address_dtos:
            pairs.append(
                AddressLookupDTO(
                    user_id=address.user_id,
                    label=address.label,
                    pincode=address.pincode,
                )
            )

        return pairs

    def _validate_users(self, user_ids: List[str]):

        existed_users = self.user_storage.get_users_by_user_ids(user_ids=user_ids)
        existed_user_ids = [each.id for each in existed_users]

        in_valid_users = []

        for user_id in user_ids:
            if user_id not in existed_user_ids:
                in_valid_users.append(user_id)

        if in_valid_users:
            raise InvalidUsersFound(user_ids=in_valid_users)
