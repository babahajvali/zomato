import pytest
from unittest.mock import create_autospec

from accounts.exception.custom_exceptions import UserNotFound
from accounts.interactors.address.get_user_addresses_interactor import (
    AddressesInteractor,
)
from accounts.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.tests.factories.interactor_factories import AddressDTOFactory


class TestGetUserAddressesInteractor:
    def setup_method(self):
        self.mock_address_storage = create_autospec(AddressStorageInterface)
        self.mock_user_storage = create_autospec(UserStorageInterface)
        self.interactor = AddressesInteractor(
            address_storage=self.mock_address_storage,
            user_storage=self.mock_user_storage,
        )

    def test_get_user_addresses_success(self):
        # Arrange
        user_id = "test-user-id"
        expected_addresses = [
            AddressDTOFactory(user_id=user_id),
            AddressDTOFactory(user_id=user_id),
        ]

        self.mock_user_storage.check_user_exists.return_value = True
        self.mock_address_storage.get_user_addresses.return_value = expected_addresses

        # Act
        result = self.interactor.get_user_addresses(user_id=user_id)

        # Assert
        assert result == expected_addresses
        self.mock_user_storage.check_user_exists.assert_called_once_with(
            user_id=user_id
        )
        self.mock_address_storage.get_user_addresses.assert_called_once_with(
            user_id=user_id
        )

    def test_get_user_addresses_user_not_found(self):
        # Arrange
        user_id = "non-existent-user"

        self.mock_user_storage.check_user_exists.return_value = False

        # Act & Assert
        with pytest.raises(UserNotFound) as exc_info:
            self.interactor.get_user_addresses(user_id=user_id)

        assert exc_info.value.user_id == user_id
        self.mock_user_storage.check_user_exists.assert_called_once_with(
            user_id=user_id
        )
        self.mock_address_storage.get_user_addresses.assert_not_called()

    def test_get_address_success(self):
        # Arrange
        address_id = 1
        expected_address = AddressDTOFactory(address_id=address_id)

        self.mock_address_storage.get_address_by_id.return_value = expected_address

        # Act
        result = self.interactor.get_address(address_id=address_id)

        # Assert
        assert result == expected_address
        self.mock_address_storage.get_address_by_id.assert_called_once_with(
            address_id=address_id
        )

    def test_get_address_not_found(self):
        # Arrange
        address_id = 999

        self.mock_address_storage.get_address_by_id.return_value = None

        # Act
        result = self.interactor.get_address(address_id=address_id)

        # Assert
        assert result is None
        self.mock_address_storage.get_address_by_id.assert_called_once_with(
            address_id=address_id
        )
