from typing import List, Any

from account.exception.custom_exceptions import AlreadyExistsAddress, \
    DuplicateAddresses
from account.interactors.dtos import CreateAddressDTO
from account.interactors.storage_interface.address_storage_interface import \
    AddressStorageInterface
from utils.read_csv_util import read_csv, validate_row


class ImportAddresses:

    def __init__(self, address_storage: AddressStorageInterface):
        self.address_storage = address_storage

    def import_addresses(self, file_path="./sample_data/addresses.csv"):
        rows = read_csv(file_path=file_path)

        email_label_pairs = self._validate_rows_and_get_email_and_label(rows)

        self._check_duplicate_addresses(email_label_pairs)
        self._check_existing_addresses(email_label_pairs)

        address_dtos = [
            CreateAddressDTO(
                email=row['email'],
                label=row['label'],
                full_address=row['full_address'],
                city=row['city'],
                pincode=row['pin_code'],
                is_default=False
            )
            for row in rows
        ]

        created_addresses = self.address_storage.create_bulk_addresses(
            address_dtos)

        return f"{len(created_addresses)} addresses imported"

    @staticmethod
    def _validate_rows_and_get_email_and_label(rows: list[dict[Any, str | Any]]) -> list[Any]:
        email_label_pairs = []
        for index, row in enumerate(rows, start=1):
            validate_row(row, ['email', 'label', 'full_address'],
                         f"address row {index}")

            email = row['email'].strip().lower()
            label = row['label'].strip()

            row['email'] = email
            row['label'] = label

            email_label_pairs.append((email, label))
        return email_label_pairs

    def _check_existing_addresses(self, email_label_pairs: List[tuple]):
        emails = [pair[0] for pair in email_label_pairs]
        labels = [pair[1] for pair in email_label_pairs]

        existing_addresses = self.address_storage.get_existing_addresses(
            emails, labels)

        if existing_addresses:
            raise AlreadyExistsAddress(addresses=existing_addresses)

    @staticmethod
    def _check_duplicate_addresses(email_label_pairs: List[tuple]):
        seen = set()
        duplicates = []
        for email, label in email_label_pairs:
            if (email, label) in seen:
                duplicates.append((email, label))
            seen.add((email, label))

        if duplicates:
            raise DuplicateAddresses(addresses=duplicates)
