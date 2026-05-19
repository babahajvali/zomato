from unittest.mock import create_autospec

import pytest

from accounts.exception.custom_exceptions import DuplicateAddresses, InvalidUsersFound
from accounts.interactors.address.address_interactor import AddressInteractor
from accounts.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.tests.factories.interactor_factories import (
    UserDTOFactory,
    AddressDTOFactory,
)
from accounts.tests.interactors.address.test_address_interactor import (
    _create_address_dto,
    LABEL_HOME,
    PINCODE,
    USER_ID,
    ADDRESS_ID,
    LABEL_WORK,
    SECOND_PINCODE,
    SECOND_ADDRESS_ID,
)


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


class TestCreateOrUpdateBulkAddresses:
    @pytest.mark.django_db
    def test_create_or_update_bulk_addresses_with_single_address_create_success(
        self, address_interactor, address_storage, user_storage
    ):
        # Arrange
        address_dto = _create_address_dto(label=LABEL_HOME, pincode=PINCODE)
        user_storage.get_users_by_user_ids.return_value = [UserDTOFactory(id=USER_ID)]
        address_storage.get_existing_addresses.return_value = []
        address_storage.create_bulk_addresses.return_value = [
            AddressDTOFactory(address_id=ADDRESS_ID)
        ]

        # Act
        result = address_interactor.create_or_update_bulk_addresses(
            create_address_dtos=[address_dto]
        )

        # Assert
        assert result == "1 created and 0 updated address!!!"
        address_storage.create_bulk_addresses.assert_called_once_with(
            address_dtos=[address_dto]
        )
        address_storage.update_bulk_addresses.assert_not_called()

    @pytest.mark.django_db
    def test_create_or_update_bulk_addresses_with_multiple_addresses_create_success(
        self, address_interactor, address_storage, user_storage
    ):
        # Arrange
        address_dtos = [
            _create_address_dto(label=LABEL_HOME, pincode=PINCODE),
            _create_address_dto(label=LABEL_WORK, pincode=SECOND_PINCODE),
        ]
        user_storage.get_users_by_user_ids.return_value = [UserDTOFactory(id=USER_ID)]
        address_storage.get_existing_addresses.return_value = []
        address_storage.create_bulk_addresses.return_value = [
            AddressDTOFactory(address_id=ADDRESS_ID),
            AddressDTOFactory(address_id=SECOND_ADDRESS_ID),
        ]

        # Act
        result = address_interactor.create_or_update_bulk_addresses(
            create_address_dtos=address_dtos
        )

        # Assert
        assert result == "2 created and 0 updated address!!!"
        address_storage.create_bulk_addresses.assert_called_once_with(
            address_dtos=address_dtos
        )
        address_storage.update_bulk_addresses.assert_not_called()

    @pytest.mark.django_db
    def test_create_or_update_bulk_addresses_with_single_address_update_success(
        self, address_interactor, address_storage, user_storage
    ):
        # Arrange
        address_dto = _create_address_dto(label=LABEL_HOME, pincode=PINCODE)
        existing_address = AddressDTOFactory(
            address_id=ADDRESS_ID,
            user_id=USER_ID,
            label=LABEL_HOME,
            pincode=PINCODE,
        )
        user_storage.get_users_by_user_ids.return_value = [UserDTOFactory(id=USER_ID)]
        address_storage.get_existing_addresses.return_value = [existing_address]
        address_storage.update_bulk_addresses.return_value = [existing_address]

        # Act
        result = address_interactor.create_or_update_bulk_addresses(
            create_address_dtos=[address_dto]
        )

        # Assert
        assert result == "0 created and 1 updated address!!!"
        address_storage.create_bulk_addresses.assert_not_called()
        address_storage.update_bulk_addresses.assert_called_once()

    @pytest.mark.django_db
    def test_create_or_update_bulk_addresses_with_multiple_addresses_update_success(
        self, address_interactor, address_storage, user_storage
    ):
        # Arrange
        address_dtos = [
            _create_address_dto(label=LABEL_HOME, pincode=PINCODE),
            _create_address_dto(label=LABEL_WORK, pincode=SECOND_PINCODE),
        ]
        existing_addresses = [
            AddressDTOFactory(
                address_id=ADDRESS_ID,
                user_id=USER_ID,
                label=LABEL_HOME,
                pincode=PINCODE,
            ),
            AddressDTOFactory(
                address_id=SECOND_ADDRESS_ID,
                user_id=USER_ID,
                label=LABEL_WORK,
                pincode=SECOND_PINCODE,
            ),
        ]
        user_storage.get_users_by_user_ids.return_value = [UserDTOFactory(id=USER_ID)]
        address_storage.get_existing_addresses.return_value = existing_addresses
        address_storage.update_bulk_addresses.return_value = existing_addresses

        # Act
        result = address_interactor.create_or_update_bulk_addresses(
            create_address_dtos=address_dtos
        )

        # Assert
        assert result == "0 created and 2 updated address!!!"
        address_storage.create_bulk_addresses.assert_not_called()
        address_storage.update_bulk_addresses.assert_called_once()

    @pytest.mark.django_db
    def test_create_or_update_bulk_addresses_with_duplicate_addresses_raises_error(
        self, address_interactor, address_storage, user_storage
    ):
        # Arrange
        address_dtos = [
            _create_address_dto(label=LABEL_HOME, pincode=PINCODE),
            _create_address_dto(label=LABEL_HOME, pincode=PINCODE),
        ]
        user_storage.get_users_by_user_ids.return_value = [UserDTOFactory(id=USER_ID)]

        # Act / Assert
        with pytest.raises(DuplicateAddresses):
            address_interactor.create_or_update_bulk_addresses(
                create_address_dtos=address_dtos
            )

        address_storage.get_existing_addresses.assert_not_called()

    @pytest.mark.django_db
    def test_create_or_update_bulk_addresses_with_invalid_user_raises_error(
        self, address_interactor, address_storage, user_storage
    ):
        # Arrange
        address_dto = _create_address_dto(label=LABEL_HOME, pincode=PINCODE)
        user_storage.get_users_by_user_ids.return_value = []

        # Act / Assert
        with pytest.raises(InvalidUsersFound) as exc:
            address_interactor.create_or_update_bulk_addresses(
                create_address_dtos=[address_dto]
            )

        assert exc.value.user_ids == [USER_ID]
        address_storage.get_existing_addresses.assert_not_called()

    @pytest.mark.django_db
    def test_create_or_update_bulk_addresses_with_mixed_create_and_update_success(
        self, address_interactor, address_storage, user_storage
    ):
        # Arrange
        address_dtos = [
            _create_address_dto(label=LABEL_HOME, pincode=PINCODE),
            _create_address_dto(label=LABEL_WORK, pincode=SECOND_PINCODE),
        ]
        existing_address = AddressDTOFactory(
            address_id=ADDRESS_ID,
            user_id=USER_ID,
            label=LABEL_HOME,
            pincode=PINCODE,
        )
        user_storage.get_users_by_user_ids.return_value = [UserDTOFactory(id=USER_ID)]
        address_storage.get_existing_addresses.return_value = [existing_address]
        address_storage.create_bulk_addresses.return_value = [
            AddressDTOFactory(address_id=SECOND_ADDRESS_ID)
        ]
        address_storage.update_bulk_addresses.return_value = [existing_address]

        # Act
        result = address_interactor.create_or_update_bulk_addresses(
            create_address_dtos=address_dtos
        )

        # Assert
        assert result == "1 created and 1 updated address!!!"
        address_storage.create_bulk_addresses.assert_called_once()
        address_storage.update_bulk_addresses.assert_called_once()
