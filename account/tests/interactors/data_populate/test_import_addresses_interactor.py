from unittest.mock import MagicMock, create_autospec, patch

import pytest

from account.exception.custom_exceptions import (
    AlreadyExistsAddress,
    DuplicateAddresses,
)
from account.interactors.populate_data.import_addresses import ImportAddresses
from account.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from account.tests.factories import CreateAddressDTOFactory


class TestImportAddresses:
    def setup_method(self):
        self.address_storage = create_autospec(AddressStorageInterface)
        self.interactor = ImportAddresses(
            address_storage_interface=self.address_storage,
        )

    def test_import_addresses_success(self):
        rows = [
            {
                "email": " Alice@Example.com ",
                "label": " Home ",
                "full_address": "12 MG Road",
                "city": "Bangalore",
                "pin_code": "560001",
            }
        ]
        expected_dto = CreateAddressDTOFactory(
            email="alice@example.com",
            label="Home",
            full_address="12 MG Road",
            city="Bangalore",
            pincode="560001",
            is_default=False,
        )
        expected_addresses = ["created-address"]
        validate_row = MagicMock()

        self.address_storage.get_existing_addresses.return_value = []
        self.address_storage.create_bulk_addresses.return_value = expected_addresses

        with patch(
            "account.interactors.populate_data.import_addresses.read_csv",
            return_value=rows,
        ), patch(
            "account.interactors.populate_data.import_addresses.validate_row",
            validate_row,
        ):
            result = self.interactor.import_addresses(file_path="addresses.csv")

        assert result == expected_addresses
        validate_row.assert_called_once_with(
            rows[0],
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

    def test_import_addresses_duplicate_pairs(self):
        rows = [
            {
                "email": " Alice@Example.com ",
                "label": " Home ",
                "full_address": "12 MG Road",
                "city": "Bangalore",
                "pin_code": "560001",
            },
            {
                "email": "alice@example.com",
                "label": "Home",
                "full_address": "34 Residency Road",
                "city": "Bangalore",
                "pin_code": "560025",
            },
        ]

        with patch(
            "account.interactors.populate_data.import_addresses.read_csv",
            return_value=rows,
        ), patch(
            "account.interactors.populate_data.import_addresses.validate_row",
            MagicMock(),
        ):
            with pytest.raises(DuplicateAddresses) as exc:
                self.interactor.import_addresses(file_path="addresses.csv")

        assert exc.value.addresses == [("alice@example.com", "Home")]
        self.address_storage.get_existing_addresses.assert_not_called()
        self.address_storage.create_bulk_addresses.assert_not_called()

    def test_import_addresses_already_exist(self):
        rows = [
            {
                "email": " Alice@Example.com ",
                "label": " Home ",
                "full_address": "12 MG Road",
                "city": "Bangalore",
                "pin_code": "560001",
            }
        ]

        self.address_storage.get_existing_addresses.return_value = [
            ("alice@example.com", "Home")
        ]

        with patch(
            "account.interactors.populate_data.import_addresses.read_csv",
            return_value=rows,
        ), patch(
            "account.interactors.populate_data.import_addresses.validate_row",
            MagicMock(),
        ):
            with pytest.raises(AlreadyExistsAddress) as exc:
                self.interactor.import_addresses(file_path="addresses.csv")

        assert exc.value.addresses == [("alice@example.com", "Home")]

