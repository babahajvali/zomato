from typing import List, Any

from account.exception.custom_exceptions import AlreadyExistsEmail, DuplicateUserEmails
from account.interactors.dtos import CreateUserDTO
from account.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportUsers:
    def __init__(self, user_storage: UserStorageInterface):
        self.user_storage = user_storage

    def import_users(self, file_path="./sample_data/users.csv"):
        rows = read_csv(file_path=file_path)

        emails = self._validate_rows(rows=rows)
        self._validate_duplicate_emails(emails)
        self._validate_existing_emails(emails)

        user_dtos = [
            CreateUserDTO(
                name=row["name"],
                email=row["email"],
                phone_number=row["phone_number"],
                role=row["role"],
            )
            for row in rows
        ]

        created_users = self.user_storage.create_bulk_users(user_dtos)

        return f"imported {len(created_users)} users"

    def _validate_existing_emails(self, emails: List[str]):
        existing_emails = self.user_storage.get_existing_emails(emails)

        if existing_emails:
            raise AlreadyExistsEmail(emails=existing_emails)

    @staticmethod
    def _validate_duplicate_emails(emails: List[str]):
        seen = set()
        duplicates = []
        for email in emails:
            if email in seen:
                duplicates.append(email)
            seen.add(email)

        if duplicates:
            raise DuplicateUserEmails(emails=duplicates)

    @staticmethod
    def _validate_rows(rows: list[dict[Any, str | Any]]) -> List[str]:
        emails = []
        for index, row in enumerate(rows, start=1):
            validate_row(row, ["email", "name"], f"user row {index}")

            email = row["email"].strip().lower()
            row["email"] = email

            emails.append(email)

        return emails
