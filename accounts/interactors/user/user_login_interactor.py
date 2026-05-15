from accounts.exception.custom_exceptions import EmailNotFound, InvalidCredentials
from accounts.interactors.dtos import UserDTO
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)


class UserLoginInteractor:
    def __init__(self, user_storage: UserStorageInterface):
        self.user_storage = user_storage

    def user_login(self, email: str, password: str) -> UserDTO:
        user_dto = self._validate_email(email=email)
        actual_password = self.user_storage.get_user_password(email=email)
        self._validate_credentials(
            actual_password=actual_password, password=password, email=email
        )

        return user_dto

    def _validate_email(self, email: str) -> UserDTO:

        user_dto = self.user_storage.get_user_by_email(email=email)

        if user_dto is None:
            raise EmailNotFound(email=email)

        return user_dto

    @staticmethod
    def _validate_credentials(actual_password: str, password: str, email: str):

        if actual_password != password:
            raise InvalidCredentials(email=email)
