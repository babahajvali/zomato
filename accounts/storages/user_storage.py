from typing import List

from django.db import transaction

from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.interactors.dtos import (
    CreateUserDTO,
    UserDTO,
    UserCreateDTO,
    UpdateUserDTO,
)
from accounts.models.user import User


class UserStorage(UserStorageInterface):
    @staticmethod
    def _convert_to_user_dto(user_obj: User) -> UserDTO:
        return UserDTO(
            id=user_obj.id,
            email=user_obj.email,
            name=user_obj.name,
            phone_number=user_obj.phone_number,
            role=user_obj.role,
        )

    @transaction.atomic
    def create_bulk_users(self, create_user_dtos: List[CreateUserDTO]) -> List[UserDTO]:
        users = [
            User(
                id=dto.id,
                name=dto.name,
                email=dto.email,
                phone_number=dto.phone_number,
                role=dto.role,
            )
            for dto in create_user_dtos
        ]

        created_users = User.objects.bulk_create(users)

        return [
            self._convert_to_user_dto(user_obj=user_obj) for user_obj in created_users
        ]

    def get_users_by_emails(self, emails: List[str]) -> List[UserDTO]:

        user_objs = User.objects.filter(email__in=emails)

        return [self._convert_to_user_dto(user_obj=user_obj) for user_obj in user_objs]

    def is_user_exists(self, user_id: str) -> bool:
        return User.objects.filter(id=user_id).exists()

    def get_user_by_email(self, email: str) -> UserDTO | None:

        user_obj = User.objects.filter(email=email).first()

        if user_obj is None:
            return None

        return self._convert_to_user_dto(user_obj=user_obj)

    def get_user_password(self, email: str) -> str:
        return User.objects.filter(email=email).first().password

    def get_user(self, user_id: str) -> UserDTO | None:

        user_obj = User.objects.filter(id=user_id).first()

        if user_obj is None:
            return None
        return self._convert_to_user_dto(user_obj=user_obj)

    def create_user(self, create_user_dto: UserCreateDTO) -> UserDTO:
        user_obj = User.objects.create(
            name=create_user_dto.name,
            email=create_user_dto.email,
            phone_number=create_user_dto.phone_number,
            role=create_user_dto.role.value,
            password=create_user_dto.password,
        )

        return self._convert_to_user_dto(user_obj=user_obj)

    def update_user(self, update_user_dto: UpdateUserDTO) -> UserDTO:

        user_properties = {}

        if update_user_dto.name:
            user_properties["name"] = update_user_dto.name

        if update_user_dto.phone_number:
            user_properties["phone_number"] = update_user_dto.phone_number

        User.objects.filter(id=update_user_dto.user_id).update(**user_properties)

        return self.get_user(user_id=update_user_dto.user_id)

    def update_bulk_users(self, update_user_dtos: List[UpdateUserDTO]):

        users = []
        for update_user_dto in update_user_dtos:
            user = User(
                id=update_user_dto.user_id,
                name=update_user_dto.name,
                phone_number=update_user_dto.phone_number,
            )

            users.append(user)

        User.objects.bulk_update(users, ["name", "phone_number"])

        return [self._convert_to_user_dto(user_obj=user_obj) for user_obj in users]

    def get_users_by_user_ids(self, user_ids: List[str]) -> List[UserDTO]:
        user_objs = User.objects.filter(id__in=user_ids)

        return [self._convert_to_user_dto(user_obj=user_obj) for user_obj in user_objs]
