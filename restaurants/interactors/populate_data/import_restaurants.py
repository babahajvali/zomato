from typing import List

from restaurants.interactors.dtos import CreateRestaurantDTO
from restaurants.interactors.restaurant.restaurant_interactor import RestaurantInteractor
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportRestaurants:
    def __init__(self, restaurant_storage: RestaurantStorageInterface):
        self.restaurant_storage = restaurant_storage

    def import_restaurants(self, file_path="./sample_data/restaurants.csv"):
        rows = list(read_csv(file_path=file_path))

        self._validate_rows(rows=rows)

        restaurants_dto = self._build_restaurant_dtos(rows=rows)

        interactor = RestaurantInteractor(restaurant_storage=self.restaurant_storage)

        return interactor.create_or_update_restaurants(
            restaurant_dtos=restaurants_dto
        )

    @staticmethod
    def _validate_rows(rows):
        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                ["id", "name", "owner_id", "cuisine_type", "address", "pin_code"],
                f"restaurant row {index}",
            )
            row["id"] = row["id"].strip()
            row["name"] = row["name"].strip()
            row["owner_id"] = row["owner_id"].strip()
            row["description"] = (row.get("description") or "").strip()
            if hasattr(row["cuisine_type"], "strip"):
                row["cuisine_type"] = row["cuisine_type"].strip()
            row["address"] = row["address"].strip()
            row["pin_code"] = row["pin_code"].strip()
            row["is_veg_only"] = row.get("is_veg_only", "").strip()
            row["is_deleted"] = row.get("is_deleted", "").strip()

    @staticmethod
    def _build_restaurant_dtos(rows) -> List[CreateRestaurantDTO]:
        return [
            CreateRestaurantDTO(
                id=row["id"],
                name=row["name"],
                owner_id=row["owner_id"],
                description=row["description"],
                cuisine_type=row["cuisine_type"],
                address=row["address"],
                pin_code=row["pin_code"],
                is_veg_only=row["is_veg_only"].lower() == "true",
                is_deleted=row["is_deleted"].lower() == "true",
            )
            for row in rows
        ]
