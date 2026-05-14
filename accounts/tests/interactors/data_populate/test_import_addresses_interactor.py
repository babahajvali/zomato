from unittest.mock import create_autospec, patch

import pytest

from accounts.exception.custom_exceptions import DuplicateAddresses
from accounts.interactors.dtos import (
    AddressLookupDTO,
    CreateAddressDTO,
    UpdateAddressDTO,
)
from accounts.interactors.populate_data.import_addresses import ImportAddresses
from accounts.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.tests.factories.interactor_factories import AddressDTOFactory


READ_CSV = "accounts.interactors.populate_data.import_addresses.read_csv"
VALIDATE_ROW = "accounts.interactors.populate_data.import_addresses.validate_row"


ALICE_ROW = {
    "user_id": " user-1 ",
    "label": " Home ",
    "full_address": "12 MG Road",
    "city": "Bangalore",
    "pin_code": "560001",
    "is_default": "False",
}

ALICE_ROW_2 = {
    "user_id": "user-1",
    "label": "Home",
    "full_address": "34 Residency Road",
    "city": "Bangalore",
    "pin_code": "560025",
}


class TestImportAddresses:
    def setup_method(self):
        self.address_storage = create_autospec(AddressStorageInterface)
        user_storage = create_autospec(UserStorageInterface)
        self.interactor = ImportAddresses(
            address_storage=self.address_storage, user_storage=user_storage
        )

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_addresses_success(self, mock_read_csv, mock_validate_row):
        # Arrange
        mock_read_csv.return_value = [ALICE_ROW]
        self.address_storage.get_existing_addresses.return_value = []
        self.address_storage.create_bulk_addresses.return_value = ["created-address"]
        self.address_storage.update_bulk_addresses.return_value = []

        expected_dto = CreateAddressDTO(
            user_id="user-1",
            label="Home",
            full_address="12 MG Road",
            city="Bangalore",
            pincode=560001,
            is_default=False,
        )

        # Act
        result = self.interactor.import_addresses(file_path="addresses.csv")

        # Assert
        assert result == "1 addresses created, 0 addresses updated"
        mock_validate_row.assert_called_once_with(
            ALICE_ROW,
            ["user_id", "label", "full_address", "pin_code", "city"],
            "address row 1",
        )
        self.address_storage.get_existing_addresses.assert_called_once_with(
            pairs=[
                AddressLookupDTO(
                    user_id="user-1",
                    label="Home",
                    pincode=560001,
                )
            ],
        )
        self.address_storage.create_bulk_addresses.assert_called_once_with(
            [expected_dto]
        )

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_addresses_duplicate_pairs(self, mock_read_csv, mock_validate_row):
        # Arrange
        mock_read_csv.return_value = [
            ALICE_ROW,
            {
                **ALICE_ROW_2,
                "pin_code": "560001",
            },
        ]

        # Act & Assert
        with pytest.raises(DuplicateAddresses):
            self.interactor.import_addresses(file_path="addresses.csv")

        self.address_storage.get_existing_addresses.assert_not_called()
        self.address_storage.create_bulk_addresses.assert_not_called()

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_addresses_updates_existing(self, mock_read_csv, mock_validate_row):
        # Arrange
        mock_read_csv.return_value = [ALICE_ROW]
        self.address_storage.get_existing_addresses.return_value = [
            AddressDTOFactory(
                address_id=1,
                user_id="user-1",
                label="Home",
                pincode=560001,
            )
        ]
        self.address_storage.create_bulk_addresses.return_value = []
        self.address_storage.update_bulk_addresses.return_value = ["updated-address"]

        # Act
        result = self.interactor.import_addresses(file_path="addresses.csv")

        # Assert
        assert result == "0 addresses created, 1 addresses updated"
        self.address_storage.update_bulk_addresses.assert_called_once_with(
            address_dtos=[
                UpdateAddressDTO(
                    id=1,
                    user_id="user-1",
                    label="Home",
                    full_address="12 MG Road",
                    city="Bangalore",
                    pincode=560001,
                    is_default=False,
                )
            ]
        )
