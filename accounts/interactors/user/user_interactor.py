from typing import List

from django.db import transaction

from accounts.exception.custom_exceptions import (
    EmailAlreadyExists,
    EmptyUserNameFound,
    NothingToUpdateUserProperties,
    DuplicateEmails,
)
from accounts.interactors.dtos import (
    UserCreateDTO,
    UserDTO,
    UpdateUserDTO,
    CreateUserDTO,
)
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.mixin.user_mixin import UserMixin


class UserInteractor(UserMixin):
    def __init__(self, user_storage: UserStorageInterface):
        self.user_storage = user_storage

    def create_user(self, create_user_dto: UserCreateDTO) -> UserDTO:

        self._validate_name_not_null(name=create_user_dto.name)
        self._validate_email(email=create_user_dto.email)

        return self.user_storage.create_user(create_user_dto=create_user_dto)

    def update_user(self, update_user_dto: UpdateUserDTO) -> UserDTO:
        self.validate_user_exists(
            user_id=update_user_dto.user_id, user_storage=self.user_storage
        )
        self._validate_update_properties(update_user_dto=update_user_dto)

        return self.user_storage.update_user(update_user_dto=update_user_dto)

    @transaction.atomic
    def create_or_update_users(self, user_dtos: List[CreateUserDTO]) -> str:
        emails = [user.email for user in user_dtos]

        self._validate_duplicate_emails(emails=emails)

        to_create, to_update = self._split_new_and_existing(
            user_dtos=user_dtos, emails=emails
        )

        created_users = []
        updated_users = []

        if to_create:
            created_users = self.user_storage.create_bulk_users(
                create_user_dtos=to_create
            )

        if to_update:
            updated_users = self.user_storage.update_bulk_users(
                update_user_dtos=to_update
            )

        return f"{len(created_users)} users created and {len(updated_users)} users updated!!!"

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

    @staticmethod
    def _validate_duplicate_emails(emails: List[str]):
        seen = set()
        duplicates = []

        for email in emails:
            if email in seen:
                duplicates.append(email)
            seen.add(email)

        if duplicates:
            raise DuplicateEmails(emails=duplicates)

    def _split_new_and_existing(
        self,
        user_dtos: List[CreateUserDTO],
        emails: List[str],
    ) -> tuple[List[CreateUserDTO], List[UpdateUserDTO]]:

        existing_users = self.user_storage.get_users_by_emails(emails=emails)

        existing_lookup = {user.email: user.id for user in existing_users}

        to_create = []
        to_update = []

        for dto in user_dtos:
            if dto.email in existing_lookup:
                user_id = existing_lookup[dto.email]
                update_dto = self._build_update_user_dto(
                    user_dto=dto,
                    user_id=user_id,
                )
                to_update.append(update_dto)
            else:
                to_create.append(dto)

        return to_create, to_update

    @staticmethod
    def _build_update_user_dto(
        user_dto: CreateUserDTO,
        user_id: str,
    ) -> UpdateUserDTO:
        return UpdateUserDTO(
            user_id=user_id,
            name=user_dto.name,
            phone_number=user_dto.phone_number,
        )
