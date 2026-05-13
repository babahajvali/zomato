from typing import List, Any

from accounts.exception.custom_exceptions import (
    AddressAlreadyExists,
    DuplicateAddresses,
)
from accounts.interactors.dtos import CreateAddressDTO
from accounts.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportAddresses:
    def __init__(self, address_storage: AddressStorageInterface):
        self.address_storage = address_storage

    def import_addresses(self, file_path="./sample_data/addresses.csv"):
        # TODO: Clear separation of the csv handling, data cleaning and core logic should be seggregated.
        rows = read_csv(file_path=file_path)

        user_label_pairs = self._validate_rows_and_get_user_and_label(rows)

        self._validate_duplicate_addresses(user_label_pairs)
        self._validate_existing_addresses(user_label_pairs)

        # TODO: Instead of writing logic in the import interactors, I guess we can write a create interactor and compose it in this import interactor.
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

        created_addresses = self.address_storage.create_bulk_addresses(address_dtos)

        return f"{len(created_addresses)} addresses imported"

    @staticmethod
    def _validate_rows_and_get_user_and_label(
        rows: list[dict[Any, str | Any]],
    ) -> list[Any]:
        user_label_pairs = []

        for index, row in enumerate(rows, start=1):
            # TODO: As per the db schema, pincode and city are not optional.

            validate_row(
                row, ["user_id", "label", "full_address"], f"address row {index}"
            )

            user_id = row["user_id"].strip()
            label = row["label"].strip()

            row["user_id"] = user_id
            row["label"] = label

            user_label_pairs.append((user_id, label)) # TODO: Why are we using tuples instead of DTOs? here?

        return user_label_pairs

    def _validate_existing_addresses(self, user_label_pairs: List[tuple]):
        # TODO: This logic seems wrong or in appropriate in this context so plz do provide clarification

        existing_addresses = self.address_storage.get_existing_addresses(
            user_label_pairs=user_label_pairs
        )

        if existing_addresses:
            raise AddressAlreadyExists(addresses=existing_addresses)

    @staticmethod
    def _validate_duplicate_addresses(user_label_pairs: List[tuple]):
        # TODO: Wouldn't duplicate means adding the same address again instead of the label
        
        seen = set()
        duplicates = []

        for user_id, label in user_label_pairs:
            if (user_id, label) in seen:
                duplicates.append((user_id, label))
            seen.add((user_id, label))

        if duplicates:
            raise DuplicateAddresses(addresses=duplicates)
