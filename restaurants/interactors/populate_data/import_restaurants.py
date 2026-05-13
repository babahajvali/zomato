from typing import List

from restaurants.exception.custom_exceptions import (
    RestaurantAlreadyExists,
    DuplicateRestaurants,
)
from restaurants.interactors.dtos import CreateRestaurantDTO
from utils.read_csv_util import read_csv, validate_row


class ImportRestaurants:
    def __init__(self, restaurant_storage_interface):
        self.restaurant_storage_interface = restaurant_storage_interface

    def import_restaurants(self, file_path="./sample_data/restaurants.csv"):
        rows = read_csv(file_path=file_path)

        names = self._parse_and_normalize_rows(rows=rows)

        self._validate_duplicate_names(names)
        self._validate_existing_restaurants(names)

        restaurants_dto = self._build_restaurant_dtos(rows=rows)

        return self.restaurant_storage_interface.create_bulk_restaurants(
            restaurants_dto
        )

    def _validate_existing_restaurants(self, names: List[str]):
        existing_restaurants = (
            self.restaurant_storage_interface.get_existing_restaurants(names)
        )

        if existing_restaurants:
            raise RestaurantAlreadyExists(names=existing_restaurants)

    @staticmethod
    def _validate_duplicate_names(names: List[str]):
        seen = set()
        duplicates = []
        for name in names:
            if name in seen:
                duplicates.append(name)
            seen.add(name)

        if duplicates:
            raise DuplicateRestaurants(names=duplicates)

    @staticmethod
    def _parse_and_normalize_rows(rows) -> List[str]:
        names = []
        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                ["id", "name", "owner_id", "cuisine_type", "address", "pin_code"],
                f"restaurant row {index}",
            )
            row["id"] = row["id"].strip()
            row["name"] = row["name"].strip()
            row["owner_id"] = row["owner_id"].strip()
            names.append(row["name"])
        return names

    @staticmethod
    def _build_restaurant_dtos(rows) -> List[CreateRestaurantDTO]:
        return [
            CreateRestaurantDTO(
                id=row["id"],
                name=row["name"],
                owner_id=row["owner_id"],
                # TODO: description is NOT NULL in the model — row.get() can return None and writes will blow up at DB layer.
                description=row.get("description"),
                cuisine_type=row["cuisine_type"],
                address=row["address"],
                pin_code=row["pin_code"],
                is_veg_only=row["is_veg_only"].strip().lower() == "true",
                is_deleted=row["is_deleted"].strip().lower() == "true",
            )
            for row in rows
        ]
