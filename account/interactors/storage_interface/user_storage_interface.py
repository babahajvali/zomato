from abc import ABC, abstractmethod
from typing import List

from account.interactors.dtos import CreateUserDTO


class UserStorageInterface(ABC):

    @abstractmethod
    def create_bulk_users(self, create_users_dto: List[CreateUserDTO]):
        pass

    @abstractmethod
    def get_existing_emails(self, emails: List[str]) -> List[str]:
        pass

    @abstractmethod
    def check_user_exists(self, user_id: str) -> bool:
        pass
