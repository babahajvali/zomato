from unittest.mock import create_autospec, patch

import pytest

from accounts.exception.custom_exceptions import DuplicateEmails
from accounts.interactors.populate_data.import_users import ImportUsers
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.tests.factories.interactor_factories import UserDTOFactory


READ_CSV = "accounts.interactors.populate_data.import_users.read_csv"
VALIDATE_ROW = "accounts.interactors.populate_data.import_users.validate_row"

USER_ID = "user-1"
SECOND_USER_ID = "user-2"
EXISTING_USER_ID = "existing-user"
EMAIL = "alice@example.com"
SECOND_EMAIL = "bob@example.com"
NAME = "Alice"
SECOND_NAME = "Bob"
PHONE_NUMBER = "9999999999"
SECOND_PHONE_NUMBER = "8888888888"
ROLE = "CUSTOMER"
FILE_PATH = "users.csv"
REQUIRED_FIELDS = ["id", "email", "name", "role", "phone_number"]


@pytest.fixture
def user_storage():
    return create_autospec(UserStorageInterface)


@pytest.fixture
def import_users(user_storage):
    return ImportUsers(user_storage=user_storage)


@pytest.mark.django_db
class TestImportUsers:
    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_users_with_single_user_success(
        self, mock_read_csv, mock_validate_row, import_users, user_storage
    ):
        # Arrange
        row = _user_row(user_id=USER_ID, email=f" {EMAIL.upper()} ")
        mock_read_csv.return_value = [row]
        user_storage.get_users_by_emails.return_value = []
        user_storage.create_bulk_users.return_value = [UserDTOFactory(id=USER_ID)]

        # Act
        result = import_users.import_users(file_path=FILE_PATH)

        # Assert
        assert result == "1 users created and 0 users updated!!!"
        mock_validate_row.assert_called_once_with(row, REQUIRED_FIELDS, "user row 1")
        user_storage.get_users_by_emails.assert_called_once_with(emails=[EMAIL])
        user_storage.create_bulk_users.assert_called_once()

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_users_with_multiple_users_success(
        self, mock_read_csv, mock_validate_row, import_users, user_storage
    ):
        # Arrange
        rows = [
            _user_row(user_id=USER_ID, email=EMAIL),
            _user_row(user_id=SECOND_USER_ID, email=SECOND_EMAIL, name=SECOND_NAME),
        ]
        mock_read_csv.return_value = rows
        user_storage.get_users_by_emails.return_value = []
        user_storage.create_bulk_users.return_value = [
            UserDTOFactory(id=USER_ID),
            UserDTOFactory(id=SECOND_USER_ID),
        ]

        # Act
        result = import_users.import_users(file_path=FILE_PATH)

        # Assert
        assert result == "2 users created and 0 users updated!!!"
        assert mock_validate_row.call_count == 2
        user_storage.create_bulk_users.assert_called_once()

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_users_with_duplicate_emails_raises_error(
        self, mock_read_csv, mock_validate_row, import_users, user_storage
    ):
        # Arrange
        mock_read_csv.return_value = [
            _user_row(user_id=USER_ID, email=EMAIL),
            _user_row(user_id=SECOND_USER_ID, email=EMAIL, name=SECOND_NAME),
        ]

        # Act / Assert
        with pytest.raises(DuplicateEmails) as exc:
            import_users.import_users(file_path=FILE_PATH)

        assert exc.value.emails == [EMAIL]
        user_storage.get_users_by_emails.assert_not_called()

    @patch(READ_CSV)
    def test_import_users_with_missing_required_field_raises_error(
        self, mock_read_csv, import_users, user_storage
    ):
        # Arrange
        missing_field = "email"
        row = _user_row(user_id=USER_ID, email=EMAIL)
        row.pop(missing_field)
        mock_read_csv.return_value = [row]

        # Act / Assert
        with pytest.raises(ValueError) as exc:
            import_users.import_users(file_path=FILE_PATH)

        assert f"Missing field '{missing_field}'" in str(exc.value)
        user_storage.get_users_by_emails.assert_not_called()

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_users_with_mixed_create_and_update_success(
        self, mock_read_csv, mock_validate_row, import_users, user_storage
    ):
        # Arrange
        rows = [
            _user_row(user_id=USER_ID, email=EMAIL),
            _user_row(user_id=SECOND_USER_ID, email=SECOND_EMAIL, name=SECOND_NAME),
        ]
        mock_read_csv.return_value = rows
        existing_user = UserDTOFactory(id=EXISTING_USER_ID, email=EMAIL)
        user_storage.get_users_by_emails.return_value = [existing_user]
        user_storage.create_bulk_users.return_value = [
            UserDTOFactory(id=SECOND_USER_ID)
        ]
        user_storage.update_bulk_users.return_value = [existing_user]

        # Act
        result = import_users.import_users(file_path=FILE_PATH)

        # Assert
        assert result == "1 users created and 1 users updated!!!"
        user_storage.create_bulk_users.assert_called_once()
        user_storage.update_bulk_users.assert_called_once()


def _user_row(user_id: str, email: str, name: str = NAME) -> dict[str, str]:
    return {
        "id": user_id,
        "name": name,
        "email": email,
        "phone_number": PHONE_NUMBER,
        "role": ROLE,
    }
