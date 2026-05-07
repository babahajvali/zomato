from abc import ABC, abstractmethod
from typing import List

from accounts.interactors.dtos import CreateUserDTO, UserDTO


class UserStorageInterface(ABC):
    @abstractmethod
    def create_bulk_users(self, create_user_dtos: List[CreateUserDTO]):
        pass

    @abstractmethod
    def get_existing_emails(self, emails: List[str]) -> List[str]:
        pass

    @abstractmethod
    def check_user_exists(self, user_id: str) -> bool:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> UserDTO:
        pass
