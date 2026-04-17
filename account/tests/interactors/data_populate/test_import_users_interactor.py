from unittest.mock import MagicMock, create_autospec, patch

import pytest

from account.exception.custom_exceptions import (
    AlreadyExistsEmail,
    DuplicateUserEmails,
)
from account.interactors.populate_data.import_users import ImportUsers
from account.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from account.tests.factories import CreateUserDTOFactory


class TestImportUsers:
    def setup_method(self):
        self.user_storage = create_autospec(UserStorageInterface)
        self.interactor = ImportUsers(
            user_storage_interface=self.user_storage,
        )

    def test_import_users_success(self):
        rows = [
            {
                "name": "Alice",
                "email": " Alice@Example.com ",
                "phone_number": "9999999999",
                "role": "OWNER",
            }
        ]
        expected_dto = CreateUserDTOFactory(
            name="Alice",
            email="alice@example.com",
            phone_number="9999999999",
            role="OWNER",
        )
        expected_users = ["created-user"]
        validate_row = MagicMock()

        self.user_storage.get_existing_emails.return_value = []
        self.user_storage.create_bulk_users.return_value = expected_users

        with patch(
            "account.interactors.populate_data.import_users.read_csv",
            return_value=rows,
        ), patch(
            "account.interactors.populate_data.import_users.validate_row",
            validate_row,
        ):
            result = self.interactor.import_users(file_path="users.csv")

        assert result == expected_users
        validate_row.assert_called_once_with(
            rows[0],
            ["email", "name"],
            "user row 1",
        )
        self.user_storage.get_existing_emails.assert_called_once_with(
            ["alice@example.com"]
        )
        self.user_storage.create_bulk_users.assert_called_once_with([expected_dto])

    def test_import_users_duplicate_emails(self):
        rows = [
            {
                "name": "Alice",
                "email": " Alice@Example.com ",
                "phone_number": "9999999999",
                "role": "OWNER",
            },
            {
                "name": "Bob",
                "email": "alice@example.com",
                "phone_number": "8888888888",
                "role": "CUSTOMER",
            },
        ]

        with patch(
            "account.interactors.populate_data.import_users.read_csv",
            return_value=rows,
        ), patch(
            "account.interactors.populate_data.import_users.validate_row",
            MagicMock(),
        ):
            with pytest.raises(DuplicateUserEmails) as exc:
                self.interactor.import_users(file_path="users.csv")

        assert exc.value.emails == ["alice@example.com"]
        self.user_storage.get_existing_emails.assert_not_called()
        self.user_storage.create_bulk_users.assert_not_called()

    def test_import_users_existing_email(self):
        rows = [
            {
                "name": "Alice",
                "email": " Alice@Example.com ",
                "phone_number": "9999999999",
                "role": "OWNER",
            }
        ]

        self.user_storage.get_existing_emails.return_value = ["alice@example.com"]

        with patch(
            "account.interactors.populate_data.import_users.read_csv",
            return_value=rows,
        ), patch(
            "account.interactors.populate_data.import_users.validate_row",
            MagicMock(),
        ):
            with pytest.raises(AlreadyExistsEmail) as exc:
                self.interactor.import_users(file_path="users.csv")

        assert exc.value.emails == ["alice@example.com"]
        self.user_storage.create_bulk_users.assert_not_called()
