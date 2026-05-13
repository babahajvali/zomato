from unittest.mock import create_autospec, patch

import pytest

from accounts.exception.custom_exceptions import (
    DuplicateEmails,
)
from accounts.interactors.populate_data.import_users import ImportUsers
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.tests.factories.interactor_factories import CreateUserDTOFactory


READ_CSV = "accounts.interactors.populate_data.import_users.read_csv"
VALIDATE_ROW = "accounts.interactors.populate_data.import_users.validate_row"


ALICE_ROW = {
    "id": "user-1",
    "name": "Alice",
    "email": " Alice@Example.com ",
    "phone_number": "9999999999",
    "role": "OWNER",
}

BOB_ROW_DUPLICATE = {
    "id": "user-2",
    "name": "Bob",
    "email": "alice@example.com",
    "phone_number": "8888888888",
    "role": "CUSTOMER",
}


class TestImportUsers:
    def setup_method(self):
        self.user_storage = create_autospec(UserStorageInterface)
        self.interactor = ImportUsers(
            user_storage=self.user_storage,
        )

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_users_success(self, mock_read_csv, mock_validate_row):
        # Arrange
        mock_read_csv.return_value = [ALICE_ROW]
        self.user_storage.get_existing_emails.return_value = []

        expected_dto = CreateUserDTOFactory(
            id="user-1",
            name="Alice",
            email="alice@example.com",
            phone_number="9999999999",
            role="OWNER",
        )

        # Act
        self.interactor.import_users(file_path="users.csv")

        # Assert
        mock_validate_row.assert_called_once_with(
            ALICE_ROW,
            ["id", "email", "name", "role"],
            "user row 1",
        )
        self.user_storage.get_existing_emails.assert_called_once_with(
            ["alice@example.com"]
        )
        self.user_storage.create_bulk_users.assert_called_once_with([expected_dto])

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_users_duplicate_emails(self, mock_read_csv, mock_validate_row):
        # Arrange
        mock_read_csv.return_value = [ALICE_ROW, BOB_ROW_DUPLICATE]

        # Act & Assert
        with pytest.raises(DuplicateEmails) as exc:
            self.interactor.import_users(file_path="users.csv")

        assert exc.value.emails == ["alice@example.com"]
        self.user_storage.get_existing_emails.assert_not_called()
        self.user_storage.create_bulk_users.assert_not_called()
