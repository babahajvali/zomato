from accounts.exception.custom_exceptions import UserNotFound
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)


class UserMixin:
    @staticmethod
    def validate_user_exists(user_id: str, user_storage: UserStorageInterface):
        is_user_exists = user_storage.is_user_exists(user_id=user_id)

        if not is_user_exists:
            raise UserNotFound(user_id=user_id)
