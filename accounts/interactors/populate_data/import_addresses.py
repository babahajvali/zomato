from accounts.interactors.address.address_interactor import AddressInteractor
from accounts.interactors.dtos import (
    CreateAddressDTO,
)
from accounts.interactors.storage_interface.address_storage_interface import (
    AddressStorageInterface,
)
from accounts.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportAddresses:
    def __init__(
        self,
        address_storage: AddressStorageInterface,
        user_storage: UserStorageInterface,
    ):
        self.address_storage = address_storage
        self.user_storage = user_storage

    def import_addresses(self, file_path="./sample_data/addresses.csv"):
        rows = list(read_csv(file_path=file_path))

        self._validate_rows(rows)

        address_dtos = [
            CreateAddressDTO(
                user_id=row["user_id"],
                label=row["label"],
                full_address=row["full_address"],
                city=row["city"],
                pincode=int(row["pin_code"]),
                is_default=row.get("is_default", "").strip().lower() == "true",
            )
            for row in rows
        ]

        interactor = AddressInteractor(
            address_storage=self.address_storage,
            user_storage=self.user_storage,
        )

        return interactor.create_or_update_bulk_addresses(
            create_address_dtos=address_dtos
        )

    @staticmethod
    def _validate_rows(rows: list) -> None:
        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                ["user_id", "label", "full_address", "pin_code", "city"],
                f"address row {index}",
            )

            row["user_id"] = row["user_id"].strip()
            row["label"] = row["label"].strip()
            row["full_address"] = row["full_address"].strip()
            row["city"] = row["city"].strip()
            row["pin_code"] = int(row["pin_code"])
