from unittest.mock import create_autospec, patch

import pytest

from accounts.exception.custom_exceptions import DuplicateAddresses, InvalidUsersFound
from accounts.interactors.populate_data.import_addresses import ImportAddresses
from accounts.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.tests.factories.interactor_factories import (
    AddressDTOFactory,
    UserDTOFactory,
)


READ_CSV = "accounts.interactors.populate_data.import_addresses.read_csv"
VALIDATE_ROW = "accounts.interactors.populate_data.import_addresses.validate_row"

USER_ID = "user-1"
ADDRESS_ID = 1
SECOND_ADDRESS_ID = 2
LABEL_HOME = "Home"
LABEL_WORK = "Work"
FULL_ADDRESS = "12 MG Road"
SECOND_FULL_ADDRESS = "34 Residency Road"
CITY = "Bangalore"
PINCODE = "560001"
SECOND_PINCODE = "560025"
FILE_PATH = "addresses.csv"
REQUIRED_FIELDS = ["user_id", "label", "full_address", "pin_code", "city"]


@pytest.fixture
def address_storage():
    return create_autospec(AddressStorageInterface)


@pytest.fixture
def user_storage():
    return create_autospec(UserStorageInterface)


@pytest.fixture
def import_addresses(address_storage, user_storage):
    return ImportAddresses(address_storage=address_storage, user_storage=user_storage)


@pytest.mark.django_db
class TestImportAddresses:
    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_addresses_with_single_address_success(
        self,
        mock_read_csv,
        mock_validate_row,
        import_addresses,
        address_storage,
        user_storage,
    ):
        # Arrange
        row = _address_row(label=f" {LABEL_HOME} ")
        mock_read_csv.return_value = [row]
        user_storage.get_users_by_user_ids.return_value = [UserDTOFactory(id=USER_ID)]
        address_storage.get_existing_addresses.return_value = []
        address_storage.create_bulk_addresses.return_value = [
            AddressDTOFactory(address_id=ADDRESS_ID)
        ]

        # Act
        result = import_addresses.import_addresses(file_path=FILE_PATH)

        # Assert
        assert result == "1 created and 0 updated address!!!"
        mock_validate_row.assert_called_once_with(row, REQUIRED_FIELDS, "address row 1")
        address_storage.create_bulk_addresses.assert_called_once()

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_addresses_with_multiple_addresses_success(
        self,
        mock_read_csv,
        mock_validate_row,
        import_addresses,
        address_storage,
        user_storage,
    ):
        # Arrange
        rows = [
            _address_row(label=LABEL_HOME, pincode=PINCODE),
            _address_row(
                label=LABEL_WORK,
                full_address=SECOND_FULL_ADDRESS,
                pincode=SECOND_PINCODE,
            ),
        ]
        mock_read_csv.return_value = rows
        user_storage.get_users_by_user_ids.return_value = [UserDTOFactory(id=USER_ID)]
        address_storage.get_existing_addresses.return_value = []
        address_storage.create_bulk_addresses.return_value = [
            AddressDTOFactory(address_id=ADDRESS_ID),
            AddressDTOFactory(address_id=SECOND_ADDRESS_ID),
        ]

        # Act
        result = import_addresses.import_addresses(file_path=FILE_PATH)

        # Assert
        assert result == "2 created and 0 updated address!!!"
        assert mock_validate_row.call_count == 2
        address_storage.create_bulk_addresses.assert_called_once()

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_addresses_with_duplicate_addresses_raises_error(
        self,
        mock_read_csv,
        mock_validate_row,
        import_addresses,
        address_storage,
        user_storage,
    ):
        # Arrange
        mock_read_csv.return_value = [
            _address_row(label=LABEL_HOME, pincode=PINCODE),
            _address_row(label=LABEL_HOME, pincode=PINCODE),
        ]
        user_storage.get_users_by_user_ids.return_value = [UserDTOFactory(id=USER_ID)]

        # Act / Assert
        with pytest.raises(DuplicateAddresses):
            import_addresses.import_addresses(file_path=FILE_PATH)

        address_storage.get_existing_addresses.assert_not_called()

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_addresses_with_invalid_user_raises_error(
        self,
        mock_read_csv,
        mock_validate_row,
        import_addresses,
        address_storage,
        user_storage,
    ):
        # Arrange
        mock_read_csv.return_value = [_address_row(label=LABEL_HOME, pincode=PINCODE)]
        user_storage.get_users_by_user_ids.return_value = []

        # Act / Assert
        with pytest.raises(InvalidUsersFound) as exc:
            import_addresses.import_addresses(file_path=FILE_PATH)

        assert exc.value.user_ids == [USER_ID]
        address_storage.get_existing_addresses.assert_not_called()

    @patch(READ_CSV)
    def test_import_addresses_with_missing_required_field_raises_error(
        self, mock_read_csv, import_addresses, address_storage
    ):
        # Arrange
        missing_field = "pin_code"
        row = _address_row(label=LABEL_HOME, pincode=PINCODE)
        row.pop(missing_field)
        mock_read_csv.return_value = [row]

        # Act / Assert
        with pytest.raises(ValueError) as exc:
            import_addresses.import_addresses(file_path=FILE_PATH)

        assert f"Missing field '{missing_field}'" in str(exc.value)
        address_storage.get_existing_addresses.assert_not_called()


def _address_row(
    label: str,
    pincode: str = PINCODE,
    full_address: str = FULL_ADDRESS,
) -> dict[str, str]:
    return {
        "user_id": USER_ID,
        "label": label,
        "full_address": full_address,
        "city": CITY,
        "pin_code": pincode,
        "is_default": "False",
    }
