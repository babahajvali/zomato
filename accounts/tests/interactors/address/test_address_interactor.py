from unittest.mock import create_autospec

import pytest

from accounts.exception.custom_exceptions import (
    UserNotFound,
)
from accounts.interactors.address.address_interactor import AddressInteractor
from accounts.interactors.dtos import CreateAddressDTO
from accounts.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.tests.factories.interactor_factories import (
    AddressDTOFactory,
)

USER_ID = "user-1"
OTHER_USER_ID = "user-2"
ADDRESS_ID = 1
SECOND_ADDRESS_ID = 2
INVALID_ADDRESS_ID = 999
LABEL_HOME = "Home"
LABEL_WORK = "Work"
PINCODE = 560001
SECOND_PINCODE = 560002
FULL_ADDRESS = "12 MG Road"
SECOND_FULL_ADDRESS = "34 Residency Road"
CITY = "Bangalore"


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


class TestGetUserAddresses:
    def test_get_user_addresses_with_single_address_success(
        self, address_interactor, address_storage, user_storage
    ):
        # Arrange
        expected_addresses = [AddressDTOFactory(user_id=USER_ID)]
        user_storage.is_user_exists.return_value = True
        address_storage.get_user_addresses.return_value = expected_addresses

        # Act
        result = address_interactor.get_user_addresses(user_id=USER_ID)

        # Assert
        assert result == expected_addresses
        address_storage.get_user_addresses.assert_called_once_with(user_id=USER_ID)

    def test_get_user_addresses_with_multiple_addresses_success(
        self, address_interactor, address_storage, user_storage
    ):
        # Arrange
        expected_addresses = [
            AddressDTOFactory(address_id=ADDRESS_ID, user_id=USER_ID),
            AddressDTOFactory(address_id=SECOND_ADDRESS_ID, user_id=USER_ID),
        ]
        user_storage.is_user_exists.return_value = True
        address_storage.get_user_addresses.return_value = expected_addresses

        # Act
        result = address_interactor.get_user_addresses(user_id=USER_ID)

        # Assert
        assert result == expected_addresses
        address_storage.get_user_addresses.assert_called_once_with(user_id=USER_ID)

    def test_get_user_addresses_with_user_not_found_raises_error(
        self, address_interactor, address_storage, user_storage
    ):
        # Arrange
        user_storage.is_user_exists.return_value = False

        # Act / Assert
        with pytest.raises(UserNotFound) as exc:
            address_interactor.get_user_addresses(user_id=USER_ID)

        assert exc.value.user_id == USER_ID
        address_storage.get_user_addresses.assert_not_called()


def _create_address_dto(label: str, pincode: int) -> CreateAddressDTO:
    return CreateAddressDTO(
        user_id=USER_ID,
        label=label,
        full_address=FULL_ADDRESS,
        city=CITY,
        pincode=pincode,
        is_default=False,
    )
