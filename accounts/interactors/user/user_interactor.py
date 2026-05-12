from accounts.exception.custom_exceptions import (
    EmailAlreadyExists,
    EmptyUserNameFound,
    NothingToUpdateUserProperties,
)
from accounts.interactors.dtos import UserCreateDTO, UserDTO, UpdateUserDTO
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.mixin.user_mixin import UserMixin


class UserInteractor(UserMixin):
    def __init__(self, user_storage: UserStorageInterface):
        super().__init__(user_storage=user_storage)
        self.user_storage = user_storage

    def create_user(self, create_user_dto: UserCreateDTO) -> UserDTO:

        self._validate_name_not_null(name=create_user_dto.name)
        self._validate_email(email=create_user_dto.email)

        return self.user_storage.create_user(create_user_dto=create_user_dto)

    def update_user(self, update_user_dto: UpdateUserDTO) -> UserDTO:
        self.validate_user_exists(user_id=update_user_dto.user_id)
        self._validate_update_properties(update_user_dto=update_user_dto)

        return self.user_storage.update_user(update_user_dto=update_user_dto)

    def _validate_email(self, email: str):
        user_dto = self.user_storage.get_user_by_email(email=email)

        if user_dto:
            raise EmailAlreadyExists(emails=[email])

    @staticmethod
    def _validate_name_not_null(name: str):
        if name is None or name == "" or name.strip() == "":
            raise EmptyUserNameFound(name=name)

    def _validate_update_properties(self, update_user_dto: UpdateUserDTO):
        if update_user_dto.name is not None:
            self._validate_name_not_null(name=update_user_dto.name)

        if update_user_dto.name is None and update_user_dto.phone_number is None:
            raise NothingToUpdateUserProperties(user_id=update_user_dto.user_id)
