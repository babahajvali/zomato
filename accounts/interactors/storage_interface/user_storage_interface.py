from abc import ABC, abstractmethod
from typing import List

from accounts.interactors.dtos import (
    CreateUserDTO,
    UserDTO,
    UserCreateDTO,
    UpdateUserDTO,
)


class UserStorageInterface(ABC):
    @abstractmethod
    def create_bulk_users(self, create_user_dtos: List[CreateUserDTO]):
        pass

    @abstractmethod
    def get_existing_emails(self, emails: List[str]) -> List[UserDTO]:
        pass

    @abstractmethod
    def check_user_exists(self, user_id: str) -> bool:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> UserDTO:
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> UserDTO | None:
        pass

    @abstractmethod
    def create_user(self, create_user_dto: UserCreateDTO) -> UserDTO:
        pass

    @abstractmethod
    def update_user(self, update_user_dto: UpdateUserDTO) -> UserDTO:
        pass

    @abstractmethod
    def update_bulk_users(self, bulk_update_user_dtos: List[UpdateUserDTO]):
        pass
