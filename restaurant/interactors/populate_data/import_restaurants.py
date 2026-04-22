from typing import List

from restaurant.exception.custom_exceptions import (
    AlreadyExistsRestaurant,
    DuplicateRestaurants,
)
from restaurant.interactors.dtos import CreateRestaurantDTO
from utils.read_csv_util import read_csv, validate_row


class ImportRestaurants:
    def __init__(self, restaurant_storage_interface):
        self.restaurant_storage_interface = restaurant_storage_interface

    def import_restaurants(self, file_path="./sample_data/restaurants.csv"):
        rows = read_csv(file_path=file_path)

        names = []
        owner_ids = []

        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                ["name", "owner_id", "cuisine_type", "address", "pin_code"],
                f"restaurant row {index}",
            )

            name = row["name"].strip()
            owner_id = row["owner_id"].strip()

            row["name"] = name
            row["owner_id"] = owner_id

            names.append(name)
            owner_ids.append(owner_id)

        self._validate_duplicate_names(names)
        self._validate_existing_restaurants(names)

        restaurants_dto = [
            CreateRestaurantDTO(
                name=row["name"],
                owner_id=row["owner_id"],
                description=row.get("description"),
                cuisine_type=row["cuisine_type"],
                address=row["address"],
                pin_code=row["pin_code"],
                is_veg_only=row["is_veg_only"].strip().lower() == "true",
                is_deleted=row["is_deleted"].strip().lower() != "true",
            )
            for row in rows
        ]

        return self.restaurant_storage_interface.create_bulk_restaurants(
            restaurants_dto
        )

    def _validate_existing_restaurants(self, names: List[str]):
        existing_restaurants = (
            self.restaurant_storage_interface.get_existing_restaurants(names)
        )

        if existing_restaurants:
            raise AlreadyExistsRestaurant(names=existing_restaurants)

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
