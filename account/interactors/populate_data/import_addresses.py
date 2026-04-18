from typing import List

from account.exception.custom_exceptions import AlreadyExistsAddress, \
    DuplicateAddresses, EmailNotFound
from account.interactors.dtos import CreateAddressDTO
from account.interactors.storage_interface.address_storage_interface import \
    AddressStorageInterface
from utils.read_csv_util import read_csv, validate_row


class ImportAddresses:

    def __init__(self, address_storage_interface: AddressStorageInterface):
        self.address_storage_interface = address_storage_interface

    def import_addresses(self, file_path="./sample_data/addresses.csv"):
        rows = read_csv(file_path=file_path)

        email_label_pairs = []
        for index, row in enumerate(rows, start=1):
            validate_row(row, ['email', 'label', 'full_address'],
                         f"address row {index}")

            email = row['email'].strip().lower()
            label = row['label'].strip()

            row['email'] = email
            row['label'] = label

            email_label_pairs.append((email, label))

        self._check_duplicate_addresses(email_label_pairs)
        self._check_existing_addresses(email_label_pairs)

        addresses_dto = [
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

        created_addresses = self.address_storage_interface.create_bulk_addresses(
            addresses_dto)

        return created_addresses

    def _check_existing_addresses(self, email_label_pairs: List[tuple]):
        emails = [pair[0] for pair in email_label_pairs]
        labels = [pair[1] for pair in email_label_pairs]

        existing_addresses = self.address_storage_interface.get_existing_addresses(
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
