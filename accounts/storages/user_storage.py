from typing import List
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.interactors.dtos import CreateUserDTO, UserDTO
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

    def create_bulk_users(self, create_user_dtos: List[CreateUserDTO]):
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

        return created_users

    def get_existing_emails(self, emails: List[str]) -> List[str]:

        return list(
            User.objects.filter(email__in=emails).values_list("email", flat=True)
        )

    def check_user_exists(self, user_id: str) -> bool:
        return User.objects.filter(id=user_id).exists()

    def get_user_by_email(self, email: str) -> UserDTO | None:

        user_obj = User.objects.filter(email=email).first()

        if user_obj is None:
            return None

        return self._convert_to_user_dto(user_obj=user_obj)
