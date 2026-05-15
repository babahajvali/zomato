import pytest
from unittest.mock import Mock

from accounts.exception.custom_exceptions import EmailNotFound, InvalidCredentials
from accounts.interactors.user.user_login_interactor import UserLoginInteractor
from accounts.tests.factories.interactor_factories import UserDTOFactory


class TestUserLoginInteractor:
    def test_user_login_success(self):
        # Arrange
        user_storage = Mock()

        user_dto = UserDTOFactory(id=1, email="test@gmail.com")

        user_storage.get_user_by_email.return_value = user_dto
        user_storage.get_user_password.return_value = "password123"

        interactor = UserLoginInteractor(user_storage=user_storage)

        # Act
        response = interactor.user_login(email="test@gmail.com", password="password123")

        # Assert
        assert response == user_dto
        user_storage.get_user_by_email.assert_called_once_with(email="test@gmail.com")

    def test_user_login_with_invalid_email_raises_exception(self):
        # Arrange
        user_storage = Mock()

        user_storage.get_user_by_email.return_value = None

        interactor = UserLoginInteractor(user_storage=user_storage)

        # Act & Assert
        with pytest.raises(EmailNotFound):
            interactor.user_login(email="invalid@gmail.com", password="password123")

        user_storage.get_user_by_email.assert_called_once_with(
            email="invalid@gmail.com"
        )

    def test_user_login_with_invalid_password_raises_exception(self):
        # Arrange
        user_storage = Mock()

        user_dto = UserDTOFactory(
            id=1,
            email="test@gmail.com",
        )

        user_storage.get_user_by_email.return_value = user_dto

        interactor = UserLoginInteractor(user_storage=user_storage)

        # Act & Assert
        with pytest.raises(InvalidCredentials):
            interactor.user_login(email="test@gmail.com", password="wrong_password")

        user_storage.get_user_by_email.assert_called_once_with(email="test@gmail.com")
