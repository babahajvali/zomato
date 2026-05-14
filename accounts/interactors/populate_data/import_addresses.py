from typing import List

from accounts.exception.custom_exceptions import DuplicateAddresses
from accounts.interactors.address.address_interactor import AddressInteractor
from accounts.interactors.dtos import (
    CreateAddressDTO,
    AddressLookupDTO,
    UpdateAddressDTO,
)
from accounts.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportAddresses:
    def __init__(
        self,
        address_storage: AddressStorageInterface,
        user_storage: UserStorageInterface,
    ):
        self.address_storage = address_storage
        self.user_storage = user_storage

    def import_addresses(self, file_path="./sample_data/addresses.csv"):
        rows = list(read_csv(file_path=file_path))

        address_lookups = self._validate_rows_and_get_address_lookups(rows)

        self._validate_duplicate_addresses(address_lookups)

        address_dtos = [
            CreateAddressDTO(
                user_id=row["user_id"],
                label=row["label"],
                full_address=row["full_address"],
                city=row["city"],
                pincode=int(row["pin_code"]),
                is_default=row.get("is_default", "").strip().lower() == "true",
            )
            for row in rows
        ]

        to_create, to_update = self._split_new_and_existing(
            address_dtos=address_dtos, pairs=address_lookups
        )

        interactor = AddressInteractor(
            address_storage=self.address_storage, user_storage=self.user_storage
        )

        created = interactor.create_bulk_addresses(create_address_dtos=to_create)
        updated = interactor.update_bulk_addresses(update_address_dtos=to_update)

        return f"{len(created)} addresses created, {len(updated)} addresses updated"

    @staticmethod
    def _validate_rows_and_get_address_lookups(
        rows: list,
    ) -> List[AddressLookupDTO]:

        pairs = []

        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                ["user_id", "label", "full_address", "pin_code", "city"],
                f"address row {index}",
            )

            user_id = row["user_id"].strip()
            label = row["label"].strip()
            pincode = int(row["pin_code"])

            row["user_id"] = user_id
            row["label"] = label
            row["pin_code"] = pincode

            pairs.append(
                AddressLookupDTO(
                    user_id=user_id,
                    label=label,
                    pincode=pincode,
                )
            )

        return pairs

    @staticmethod
    def _validate_duplicate_addresses(
        pairs: List[AddressLookupDTO],
    ):
        seen = set()
        duplicates = []

        for pair in pairs:
            key = (pair.user_id, pair.label, pair.pincode)
            if key in seen:
                duplicates.append(pair)
            seen.add(key)

        if duplicates:
            raise DuplicateAddresses(addresses=duplicates)

    def _split_new_and_existing(
        self,
        address_dtos: List[CreateAddressDTO],
        pairs: List[AddressLookupDTO],
    ) -> tuple[List[CreateAddressDTO], List[UpdateAddressDTO]]:

        existing_addresses = self.address_storage.get_existing_addresses(pairs=pairs)

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
                    id=address_id,
                )
                to_update.append(update_dto)
            else:
                to_create.append(dto)

        return to_create, to_update

    @staticmethod
    def _build_update_address_dto(
        address_dto: CreateAddressDTO, id: int
    ) -> UpdateAddressDTO:
        return UpdateAddressDTO(
            id=id,
            user_id=address_dto.user_id,
            label=address_dto.label,
            pincode=address_dto.pincode,
            full_address=address_dto.full_address,
            is_default=address_dto.is_default,
            city=address_dto.city,
        )
