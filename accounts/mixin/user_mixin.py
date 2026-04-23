from accounts.exception.custom_exceptions import UserNotFound
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)


class UserMixin:
    def __init__(self, user_storage: UserStorageInterface):
        self.user_storage = user_storage

    def validate_user_exists(self, user_id: str):
        is_user_exists = self.user_storage.check_user_exists(user_id=user_id)

        if not is_user_exists:
            raise UserNotFound(user_id=user_id)
