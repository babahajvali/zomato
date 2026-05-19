from unittest.mock import create_autospec

import pytest

from accounts.exception.custom_exceptions import UserNotFound
from accounts.interactors.address.address_interactor import AddressInteractor
from accounts.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.tests.factories.interactor_factories import AddressDTOFactory
from accounts.tests.interactors.address.test_address_interactor import (
    ADDRESS_ID,
    USER_ID,
    INVALID_ADDRESS_ID,
    OTHER_USER_ID,
)
from utils.exceptions import AddressNotFound, AddressNotBelongsToUser


@pytest.fixture
def address_storage():
    return create_autospec(AddressStorageInterface)


@pytest.fixture
def user_storage():
    return create_autospec(UserStorageInterface)


@pytest.fixture
def address_interactor(address_storage, user_storage):
    return AddressInteractor(
        address_storage=address_storage,
        user_storage=user_storage,
    )


class TestGetAddress:
    def test_get_address_with_valid_address_success(
        self, address_interactor, address_storage, user_storage
    ):
        # Arrange
        expected_address = AddressDTOFactory(address_id=ADDRESS_ID, user_id=USER_ID)
        user_storage.is_user_exists.return_value = True
        address_storage.get_address_by_id.return_value = expected_address

        # Act
        result = address_interactor.get_address(
            address_id=ADDRESS_ID,
            user_id=USER_ID,
        )

        # Assert
        assert result == expected_address
        address_storage.get_address_by_id.assert_called_once_with(address_id=ADDRESS_ID)

    def test_get_address_with_invalid_address_raises_not_found(
        self, address_interactor, address_storage, user_storage
    ):
        # Arrange
        user_storage.is_user_exists.return_value = True
        address_storage.get_address_by_id.return_value = None

        # Act / Assert
        with pytest.raises(AddressNotFound) as exc:
            address_interactor.get_address(
                address_id=INVALID_ADDRESS_ID,
                user_id=USER_ID,
            )

        assert exc.value.address_id == INVALID_ADDRESS_ID

    def test_get_address_with_address_not_belonging_to_user_raises_error(
        self, address_interactor, address_storage, user_storage
    ):
        # Arrange
        other_user_address = AddressDTOFactory(
            address_id=ADDRESS_ID,
            user_id=OTHER_USER_ID,
        )
        user_storage.is_user_exists.return_value = True
        address_storage.get_address_by_id.return_value = other_user_address

        # Act / Assert
        with pytest.raises(AddressNotBelongsToUser) as exc:
            address_interactor.get_address(
                address_id=ADDRESS_ID,
                user_id=USER_ID,
            )

        assert exc.value.address_id == ADDRESS_ID
        assert exc.value.user_id == USER_ID

    def test_get_address_with_user_not_found_raises_error(
        self, address_interactor, address_storage, user_storage
    ):
        # Arrange
        user_storage.is_user_exists.return_value = False

        # Act / Assert
        with pytest.raises(UserNotFound) as exc:
            address_interactor.get_address(
                address_id=ADDRESS_ID,
                user_id=USER_ID,
            )

        assert exc.value.user_id == USER_ID
        address_storage.get_address_by_id.assert_not_called()
