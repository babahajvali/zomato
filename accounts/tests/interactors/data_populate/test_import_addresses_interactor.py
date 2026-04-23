from unittest.mock import create_autospec, patch

import pytest

from accounts.exception.custom_exceptions import (
    AlreadyExistsAddress,
    DuplicateAddresses,
)
from accounts.interactors.populate_data.import_addresses import ImportAddresses
from accounts.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from accounts.tests.factories.interactor_factories import CreateAddressDTOFactory


READ_CSV = "accounts.interactors.populate_data.import_addresses.read_csv"
VALIDATE_ROW = "accounts.interactors.populate_data.import_addresses.validate_row"


ALICE_ROW = {
    "email": " Alice@Example.com ",
    "label": " Home ",
    "full_address": "12 MG Road",
    "city": "Bangalore",
    "pin_code": "560001",
}

ALICE_ROW_2 = {
    "email": "alice@example.com",
    "label": "Home",
    "full_address": "34 Residency Road",
    "city": "Bangalore",
    "pin_code": "560025",
}


class TestImportAddresses:
    def setup_method(self):
        self.address_storage = create_autospec(AddressStorageInterface)
        self.interactor = ImportAddresses(
            address_storage=self.address_storage,
        )

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_addresses_success(self, mock_read_csv, mock_validate_row):
        # Arrange
        mock_read_csv.return_value = [ALICE_ROW]
        self.address_storage.get_existing_addresses.return_value = []

        expected_dto = CreateAddressDTOFactory(
            email="alice@example.com",
            label="Home",
            full_address="12 MG Road",
            city="Bangalore",
            pincode="560001",
            is_default=False,
        )

        # Act
        self.interactor.import_addresses(file_path="addresses.csv")

        # Assert
        mock_validate_row.assert_called_once_with(
            ALICE_ROW,
            ["email", "label", "full_address"],
            "address row 1",
        )
        self.address_storage.get_existing_addresses.assert_called_once_with(
            ["alice@example.com"],
            ["Home"],
        )
        self.address_storage.create_bulk_addresses.assert_called_once_with(
            [expected_dto]
        )

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_addresses_duplicate_pairs(self, mock_read_csv, mock_validate_row):
        # Arrange
        mock_read_csv.return_value = [ALICE_ROW, ALICE_ROW_2]

        # Act & Assert
        with pytest.raises(DuplicateAddresses):
            self.interactor.import_addresses(file_path="addresses.csv")

        self.address_storage.get_existing_addresses.assert_not_called()
        self.address_storage.create_bulk_addresses.assert_not_called()

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_addresses_already_exist(self, mock_read_csv, mock_validate_row):
        # Arrange
        mock_read_csv.return_value = [ALICE_ROW]
        self.address_storage.get_existing_addresses.return_value = [
            ("alice@example.com", "Home")
        ]

        # Act & Assert
        with pytest.raises(AlreadyExistsAddress) as exc:
            self.interactor.import_addresses(file_path="addresses.csv")

        assert exc.value.addresses == [("alice@example.com", "Home")]
        self.address_storage.create_bulk_addresses.assert_not_called()
