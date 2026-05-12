from unittest.mock import create_autospec

import pytest

from accounts.exception.custom_exceptions import (
    EmailAlreadyExists,
    EmptyUserNameFound,
    NothingToUpdateUserProperties,
    UserNotFound,
)
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.interactors.user.user_interactor import UserInteractor
from accounts.tests.factories.interactor_factories import (
    UpdateUserDTOFactory,
    UserCreateDTOFactory,
    UserDTOFactory,
)


class TestUserInteractor:
    def setup_method(self):
        self.user_storage = create_autospec(UserStorageInterface)
        self.interactor = UserInteractor(user_storage=self.user_storage)

    def test_create_user_success(self):
        create_user_dto = UserCreateDTOFactory(email="sample@gmail.com")
        expected_user_dto = UserDTOFactory(email="sample@gmail.com")
        self.user_storage.get_user_by_email.return_value = None
        self.user_storage.create_user.return_value = expected_user_dto

        result = self.interactor.create_user(create_user_dto=create_user_dto)

        assert result == expected_user_dto
        self.user_storage.get_user_by_email.assert_called_once_with(
            email="sample@gmail.com"
        )
        self.user_storage.create_user.assert_called_once_with(
            create_user_dto=create_user_dto
        )

    def test_create_user_with_existing_email_raises_exception(self):
        create_user_dto = UserCreateDTOFactory(email="sample@gmail.com")
        self.user_storage.get_user_by_email.return_value = UserDTOFactory(
            email="sample@gmail.com"
        )

        with pytest.raises(EmailAlreadyExists) as exc:
            self.interactor.create_user(create_user_dto=create_user_dto)

        assert exc.value.emails == ["sample@gmail.com"]
        self.user_storage.create_user.assert_not_called()

    def test_create_user_with_empty_name_raises_exception(self):
        create_user_dto = UserCreateDTOFactory(name="   ")

        with pytest.raises(EmptyUserNameFound) as exc:
            self.interactor.create_user(create_user_dto=create_user_dto)

        assert exc.value.name == "   "
        self.user_storage.get_user_by_email.assert_not_called()
        self.user_storage.create_user.assert_not_called()

    def test_update_user_success(self):
        update_user_dto = UpdateUserDTOFactory(
            user_id="user-1", name="Updated Name", phone_number="9999999999"
        )
        expected_user_dto = UserDTOFactory(id="user-1", name="Updated Name")
        self.user_storage.check_user_exists.return_value = True
        self.user_storage.update_user.return_value = expected_user_dto

        result = self.interactor.update_user(update_user_dto=update_user_dto)

        assert result == expected_user_dto
        self.user_storage.check_user_exists.assert_called_once_with(user_id="user-1")
        self.user_storage.update_user.assert_called_once_with(
            update_user_dto=update_user_dto
        )

    def test_update_user_with_phone_number_only_success(self):
        update_user_dto = UpdateUserDTOFactory(
            user_id="user-1", name=None, phone_number="9999999999"
        )
        expected_user_dto = UserDTOFactory(id="user-1", phone_number="9999999999")
        self.user_storage.check_user_exists.return_value = True
        self.user_storage.update_user.return_value = expected_user_dto

        result = self.interactor.update_user(update_user_dto=update_user_dto)

        assert result == expected_user_dto
        self.user_storage.update_user.assert_called_once_with(
            update_user_dto=update_user_dto
        )

    def test_update_user_not_found_raises_exception(self):
        update_user_dto = UpdateUserDTOFactory(user_id="missing-user")
        self.user_storage.check_user_exists.return_value = False

        with pytest.raises(UserNotFound) as exc:
            self.interactor.update_user(update_user_dto=update_user_dto)

        assert exc.value.user_id == "missing-user"
        self.user_storage.update_user.assert_not_called()

    def test_update_user_with_empty_name_raises_exception(self):
        update_user_dto = UpdateUserDTOFactory(user_id="user-1", name="")
        self.user_storage.check_user_exists.return_value = True

        with pytest.raises(EmptyUserNameFound) as exc:
            self.interactor.update_user(update_user_dto=update_user_dto)

        assert exc.value.name == ""
        self.user_storage.update_user.assert_not_called()

    def test_update_user_with_no_properties_raises_exception(self):
        update_user_dto = UpdateUserDTOFactory(
            user_id="user-1", name=None, phone_number=None
        )
        self.user_storage.check_user_exists.return_value = True

        with pytest.raises(NothingToUpdateUserProperties) as exc:
            self.interactor.update_user(update_user_dto=update_user_dto)

        assert exc.value.user_id == "user-1"
        self.user_storage.update_user.assert_not_called()
