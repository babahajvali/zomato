from typing import List, Any

from accounts.exception.custom_exceptions import DuplicateEmails
from accounts.interactors.dtos import CreateUserDTO, UpdateUserDTO
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportUsers:
    def __init__(self, user_storage: UserStorageInterface):
        self.user_storage = user_storage

    def import_users(self, file_path="./sample_data/users.csv"):
        rows = list(read_csv(file_path=file_path))

        emails = self._validate_rows(rows=rows)

        self._validate_duplicate_emails(emails=emails)

        user_dtos = [
            CreateUserDTO(
                id=row["id"],
                name=row["name"],
                email=row["email"],
                phone_number=row["phone_number"],
                role=row["role"],
            )
            for row in rows
        ]

        to_create, to_update = self._split_new_and_existing(
            user_dtos=user_dtos,
            emails=emails,
        )

        created = self.user_storage.create_bulk_users(to_create) if to_create else []
        updated = self.user_storage.update_bulk_users(to_update) if to_update else []

        return f"{len(created)} users created, {len(updated)} users updated"

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

    @staticmethod
    def _validate_rows(rows: list[dict[Any, str | Any]]) -> List[str]:
        emails = []

        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                ["id", "email", "name", "role", "phone_number"],
                f"user row {index}",
            )

            user_id = row["id"].strip()
            email = row["email"].strip().lower()

            row["id"] = user_id
            row["email"] = email

            emails.append(email)

        return emails
