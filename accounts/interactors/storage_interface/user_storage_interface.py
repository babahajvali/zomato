from abc import ABC, abstractmethod
from typing import List, Optional

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
    def get_users_by_emails(self, emails: List[str]) -> List[UserDTO]:
        pass

    @abstractmethod
    def is_user_exists(self, user_id: str) -> bool:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> UserDTO:
        pass

    @abstractmethod
    def get_user_password(self, email: str) -> str:
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> Optional[UserDTO]:
        pass

    @abstractmethod
    def create_user(self, create_user_dto: UserCreateDTO) -> UserDTO:
        pass

    @abstractmethod
    def update_user(self, update_user_dto: UpdateUserDTO) -> UserDTO:
        pass

    @abstractmethod
    def update_bulk_users(self, update_user_dtos: List[UpdateUserDTO]):
        pass

    @abstractmethod
    def get_users_by_user_ids(self, user_ids: List[str]) -> List[UserDTO]:
        pass
