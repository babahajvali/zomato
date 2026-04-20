from typing import List
from account.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from account.interactors.dtos import CreateUserDTO
from account.models.user import User
from utils.uuid_util import generate_uuid


class UserStorage(UserStorageInterface):

    def create_bulk_users(self, create_users_dto: List[CreateUserDTO]):
        users = [User(
            id=generate_uuid(),
            name=dto.name,
            email=dto.email,
            phone_number=dto.phone_number,
            role=dto.role
        ) for dto in create_users_dto]

        created_users = User.objects.bulk_create(users)

        return created_users

    def get_existing_emails(self, emails: List[str]) -> List[str]:

        return list(User.objects.filter(email__in=emails).
                    values_list('email', flat=True))

    def check_user_exists(self, user_id: str) -> bool:
        return User.objects.filter(id=user_id).exists()
