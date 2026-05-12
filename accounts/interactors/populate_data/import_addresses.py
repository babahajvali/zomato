from typing import List, Any

from accounts.exception.custom_exceptions import DuplicateAddresses
from accounts.interactors.dtos import CreateAddressDTO
from accounts.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportAddresses:
    def __init__(self, address_storage: AddressStorageInterface):
        self.address_storage = address_storage

    def import_addresses(self, file_path="./sample_data/addresses.csv"):
        rows = read_csv(file_path=file_path)

        user_label_pairs = self._validate_rows_and_get_user_and_label(rows)

        self._validate_duplicate_addresses(user_label_pairs)

        address_dtos = [
            CreateAddressDTO(
                user_id=row["user_id"],
                label=row["label"],
                full_address=row["full_address"],
                city=row["city"],
                pincode=row["pin_code"],
                is_default=row.get("is_default", "").strip().lower() == "true",
            )
            for row in rows
        ]

        to_create, to_update = self._split_new_and_existing(
            address_dtos, user_label_pairs
        )

        created = (
            self.address_storage.create_bulk_addresses(to_create) if to_create else []
        )
        updated = (
            self.address_storage.update_bulk_addresses(to_update) if to_update else []
        )

        return f"{len(created)} addresses created, {len(updated)} addresses updated"

    def _split_new_and_existing(
        self,
        address_dtos: List[CreateAddressDTO],
        user_label_pairs: List[tuple],
    ) -> tuple[List[CreateAddressDTO], List[CreateAddressDTO]]:

        existing_addresses = self.address_storage.get_existing_addresses(
            user_label_pairs=user_label_pairs
        )

        existing_lookup = {
            (addr.user_id, addr.label): addr.id for addr in existing_addresses
        }

        to_create = []
        to_update = []

        for dto in address_dtos:
            key = (dto.user_id, dto.label)
            if key in existing_lookup:
                dto.id = existing_lookup[key]
                to_update.append(dto)
            else:
                to_create.append(dto)

        return to_create, to_update

    @staticmethod
    def _validate_rows_and_get_user_and_label(
        rows: list[dict[Any, str | Any]],
    ) -> list[Any]:
        user_label_pairs = []

        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                ["user_id", "label", "full_address", "pincode", "city"],
                f"address row {index}",
            )

            user_id = row["user_id"].strip()
            label = row["label"].strip()

            row["user_id"] = user_id
            row["label"] = label

            user_label_pairs.append((user_id, label))

        return user_label_pairs

    @staticmethod
    def _validate_duplicate_addresses(user_label_pairs: List[tuple]):
        seen = set()
        duplicates = []

        for user_id, label in user_label_pairs:
            if (user_id, label) in seen:
                duplicates.append((user_id, label))
            seen.add((user_id, label))

        if duplicates:
            raise DuplicateAddresses(addresses=duplicates)
