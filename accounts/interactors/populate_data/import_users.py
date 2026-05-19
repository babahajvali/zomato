from typing import Any

from accounts.constants.enums import Role
from accounts.interactors.dtos import CreateUserDTO
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from accounts.interactors.user.user_interactor import UserInteractor
from utils.read_csv_util import read_csv, validate_row


class ImportUsers:
    def __init__(self, user_storage: UserStorageInterface):
        self.user_storage = user_storage

    def import_users(self, file_path="./sample_data/users.csv"):
        rows = list(read_csv(file_path=file_path))

        self._validate_rows(rows=rows)

        user_dtos = [
            CreateUserDTO(
                id=row["id"],
                name=row["name"],
                email=row["email"],
                phone_number=row["phone_number"],
                role=Role(row["role"]),
            )
            for row in rows
        ]

        interactor = UserInteractor(user_storage=self.user_storage)

        return interactor.create_or_update_users(user_dtos=user_dtos)

    @staticmethod
    def _validate_rows(rows: list[dict[Any, str | Any]]):

        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                ["id", "email", "name", "role", "phone_number"],
                f"user row {index}",
            )
            row["id"] = row["id"].strip()
            row["name"] = row["name"].strip()
            row["email"] = row["email"].strip().lower()
            row["phone_number"] = row["phone_number"].strip()
            row["role"] = row["role"].strip()
