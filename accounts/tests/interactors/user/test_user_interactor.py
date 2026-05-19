from unittest.mock import create_autospec

import pytest

from accounts.exception.custom_exceptions import (
    DuplicateEmails,
    EmailAlreadyExists,
    EmptyUserNameFound,
    NothingToUpdateUserProperties,
    UserNotFound,
)
from accounts.interactors.dtos import CreateUserDTO
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.interactors.user.user_interactor import UserInteractor
from accounts.tests.factories.interactor_factories import (
    UpdateUserDTOFactory,
    UserCreateDTOFactory,
    UserDTOFactory,
)


USER_ID = "user-1"
EXISTING_USER_ID = "existing-user"
SECOND_USER_ID = "user-2"
MISSING_USER_ID = "missing-user"
EMAIL = "sample@gmail.com"
SECOND_EMAIL = "second@gmail.com"
NAME = "Sample User"
UPDATED_NAME = "Updated Name"
PHONE_NUMBER = "9999999999"
SECOND_PHONE_NUMBER = "8888888888"


@pytest.fixture
def user_storage():
    return create_autospec(UserStorageInterface)


@pytest.fixture
def user_interactor(user_storage):
    return UserInteractor(user_storage=user_storage)


@pytest.mark.django_db
class TestCreateUser:
    def test_create_user_with_valid_data_success(self, user_interactor, user_storage):
        # Arrange
        create_user_dto = UserCreateDTOFactory(email=EMAIL)
        expected_user_dto = UserDTOFactory(email=EMAIL)
        user_storage.get_user_by_email.return_value = None
        user_storage.create_user.return_value = expected_user_dto

        # Act
        result = user_interactor.create_user(create_user_dto=create_user_dto)

        # Assert
        assert result == expected_user_dto
        user_storage.get_user_by_email.assert_called_once_with(email=EMAIL)
        user_storage.create_user.assert_called_once_with(
            create_user_dto=create_user_dto
        )

    def test_create_user_with_duplicate_email_raises_error(
        self, user_interactor, user_storage
    ):
        # Arrange
        create_user_dto = UserCreateDTOFactory(email=EMAIL)
        user_storage.get_user_by_email.return_value = UserDTOFactory(email=EMAIL)

        # Act / Assert
        with pytest.raises(EmailAlreadyExists) as exc:
            user_interactor.create_user(create_user_dto=create_user_dto)

        assert exc.value.emails == [EMAIL]
        user_storage.create_user.assert_not_called()

    def test_create_user_with_empty_name_raises_error(
        self, user_interactor, user_storage
    ):
        # Arrange
        empty_name = "   "
        create_user_dto = UserCreateDTOFactory(name=empty_name)

        # Act / Assert
        with pytest.raises(EmptyUserNameFound) as exc:
            user_interactor.create_user(create_user_dto=create_user_dto)

        assert exc.value.name == empty_name
        user_storage.get_user_by_email.assert_not_called()
        user_storage.create_user.assert_not_called()


@pytest.mark.django_db
class TestUpdateUser:
    def test_update_user_with_valid_data_success(self, user_interactor, user_storage):
        # Arrange
        update_user_dto = UpdateUserDTOFactory(
            user_id=USER_ID,
            name=UPDATED_NAME,
            phone_number=PHONE_NUMBER,
        )
        expected_user_dto = UserDTOFactory(id=USER_ID, name=UPDATED_NAME)
        user_storage.is_user_exists.return_value = True
        user_storage.update_user.return_value = expected_user_dto

        # Act
        result = user_interactor.update_user(update_user_dto=update_user_dto)

        # Assert
        assert result == expected_user_dto
        user_storage.is_user_exists.assert_called_once_with(user_id=USER_ID)
        user_storage.update_user.assert_called_once_with(
            update_user_dto=update_user_dto
        )

    def test_update_user_with_user_not_found_raises_error(
        self, user_interactor, user_storage
    ):
        # Arrange
        update_user_dto = UpdateUserDTOFactory(user_id=MISSING_USER_ID)
        user_storage.is_user_exists.return_value = False

        # Act / Assert
        with pytest.raises(UserNotFound) as exc:
            user_interactor.update_user(update_user_dto=update_user_dto)

        assert exc.value.user_id == MISSING_USER_ID
        user_storage.update_user.assert_not_called()

    def test_update_user_with_nothing_to_update_raises_error(
        self, user_interactor, user_storage
    ):
        # Arrange
        update_user_dto = UpdateUserDTOFactory(
            user_id=USER_ID,
            name=None,
            phone_number=None,
        )
        user_storage.is_user_exists.return_value = True

        # Act / Assert
        with pytest.raises(NothingToUpdateUserProperties) as exc:
            user_interactor.update_user(update_user_dto=update_user_dto)

        assert exc.value.user_id == USER_ID
        user_storage.update_user.assert_not_called()

    def test_update_user_with_empty_name_raises_error(
        self, user_interactor, user_storage
    ):
        # Arrange
        empty_name = ""
        update_user_dto = UpdateUserDTOFactory(user_id=USER_ID, name=empty_name)
        user_storage.is_user_exists.return_value = True

        # Act / Assert
        with pytest.raises(EmptyUserNameFound) as exc:
            user_interactor.update_user(update_user_dto=update_user_dto)

        assert exc.value.name == empty_name
        user_storage.update_user.assert_not_called()


@pytest.mark.django_db
class TestCreateOrUpdateUsers:
    def test_create_or_update_users_with_single_user_create_success(
        self, user_interactor, user_storage
    ):
        # Arrange
        user_dto = _create_user_dto(user_id=USER_ID, email=EMAIL)
        user_storage.get_users_by_emails.return_value = []
        user_storage.create_bulk_users.return_value = [UserDTOFactory(id=USER_ID)]

        # Act
        result = user_interactor.create_or_update_users(user_dtos=[user_dto])

        # Assert
        assert result == "1 users created and 0 users updated!!!"
        user_storage.create_bulk_users.assert_called_once_with(
            create_user_dtos=[user_dto]
        )
        user_storage.update_bulk_users.assert_not_called()

    def test_create_or_update_users_with_multiple_users_create_success(
        self, user_interactor, user_storage
    ):
        # Arrange
        user_dtos = [
            _create_user_dto(user_id=USER_ID, email=EMAIL),
            _create_user_dto(user_id=SECOND_USER_ID, email=SECOND_EMAIL),
        ]
        user_storage.get_users_by_emails.return_value = []
        user_storage.create_bulk_users.return_value = [
            UserDTOFactory(id=USER_ID),
            UserDTOFactory(id=SECOND_USER_ID),
        ]

        # Act
        result = user_interactor.create_or_update_users(user_dtos=user_dtos)

        # Assert
        assert result == "2 users created and 0 users updated!!!"
        user_storage.create_bulk_users.assert_called_once_with(
            create_user_dtos=user_dtos
        )
        user_storage.update_bulk_users.assert_not_called()

    def test_create_or_update_users_with_single_user_update_success(
        self, user_interactor, user_storage
    ):
        # Arrange
        user_dto = _create_user_dto(user_id=USER_ID, email=EMAIL)
        existing_user = UserDTOFactory(id=EXISTING_USER_ID, email=EMAIL)
        user_storage.get_users_by_emails.return_value = [existing_user]
        user_storage.update_bulk_users.return_value = [existing_user]

        # Act
        result = user_interactor.create_or_update_users(user_dtos=[user_dto])

        # Assert
        assert result == "0 users created and 1 users updated!!!"
        user_storage.create_bulk_users.assert_not_called()
        user_storage.update_bulk_users.assert_called_once()

    def test_create_or_update_users_with_multiple_users_update_success(
        self, user_interactor, user_storage
    ):
        # Arrange
        user_dtos = [
            _create_user_dto(user_id=USER_ID, email=EMAIL),
            _create_user_dto(user_id=SECOND_USER_ID, email=SECOND_EMAIL),
        ]
        existing_users = [
            UserDTOFactory(id=USER_ID, email=EMAIL),
            UserDTOFactory(id=SECOND_USER_ID, email=SECOND_EMAIL),
        ]
        user_storage.get_users_by_emails.return_value = existing_users
        user_storage.update_bulk_users.return_value = existing_users

        # Act
        result = user_interactor.create_or_update_users(user_dtos=user_dtos)

        # Assert
        assert result == "0 users created and 2 users updated!!!"
        user_storage.create_bulk_users.assert_not_called()
        user_storage.update_bulk_users.assert_called_once()

    def test_create_or_update_users_with_duplicate_emails_raises_error(
        self, user_interactor, user_storage
    ):
        # Arrange
        user_dtos = [
            _create_user_dto(user_id=USER_ID, email=EMAIL),
            _create_user_dto(user_id=SECOND_USER_ID, email=EMAIL),
        ]

        # Act / Assert
        with pytest.raises(DuplicateEmails) as exc:
            user_interactor.create_or_update_users(user_dtos=user_dtos)

        assert exc.value.emails == [EMAIL]
        user_storage.get_users_by_emails.assert_not_called()

    def test_create_or_update_users_with_mixed_create_and_update_success(
        self, user_interactor, user_storage
    ):
        # Arrange
        user_dtos = [
            _create_user_dto(user_id=USER_ID, email=EMAIL),
            _create_user_dto(user_id=SECOND_USER_ID, email=SECOND_EMAIL),
        ]
        existing_user = UserDTOFactory(id=EXISTING_USER_ID, email=EMAIL)
        user_storage.get_users_by_emails.return_value = [existing_user]
        user_storage.create_bulk_users.return_value = [
            UserDTOFactory(id=SECOND_USER_ID)
        ]
        user_storage.update_bulk_users.return_value = [existing_user]

        # Act
        result = user_interactor.create_or_update_users(user_dtos=user_dtos)

        # Assert
        assert result == "1 users created and 1 users updated!!!"
        user_storage.create_bulk_users.assert_called_once()
        user_storage.update_bulk_users.assert_called_once()


def _create_user_dto(user_id: str, email: str) -> CreateUserDTO:
    return CreateUserDTO(
        id=user_id,
        name=NAME,
        email=email,
        phone_number=PHONE_NUMBER,
        role="CUSTOMER",
    )
