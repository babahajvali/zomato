from typing import List
import json

from restaurant.interactors.dtos import CreateMenuItemDTO
from restaurant.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurant.exception.custom_exceptions import InvalidRestaurantIdsFound
from utils.read_csv_util import read_csv, validate_row


class ImportMenuItems:
    def __init__(self, restaurant_storage: RestaurantStorageInterface):
        self.restaurant_storage = restaurant_storage

    def import_menu_items(self, file_path="./sample_data/menu_items.csv"):
        rows = read_csv(file_path=file_path)

        restaurant_ids = []

        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                [
                    "restaurant",
                    "name",
                    "price",
                    "category",
                    "preparation_time_in_minutes",
                ],
                f"menu item row {index}",
            )

            restaurant_id = row["restaurant"].strip()
            name = row["name"].strip()

            row["restaurant"] = restaurant_id
            row["name"] = name

            restaurant_ids.append(restaurant_id)

        self._validate_restaurants_exist(list(set(restaurant_ids)))

        menu_items_dto = [
            CreateMenuItemDTO(
                name=row["name"],
                description=row.get("description"),
                price=row["price"],
                category=row["category"],
                is_veg=row.get("is_veg") == "True",
                is_available=row.get("is_available", "True") == "True",
                preparation_time_in_minutes=int(row["preparation_time_in_minutes"]),
                tags=json.loads(row["tags"]) if row.get("tags") else [],
            )
            for row in rows
        ]

        created_items = self.restaurant_storage.create_menu_items(
            menu_items_dto, restaurant_id=restaurant_ids[0]
        )

        return created_items

    def _validate_restaurants_exist(self, restaurant_ids: List[str]):
        existing_ids = self.restaurant_storage.get_restaurants_by_ids(restaurant_ids)

        existing_ids_set = set(existing_ids)
        missing_ids = [rid for rid in restaurant_ids if rid not in existing_ids_set]

        if missing_ids:
            raise InvalidRestaurantIdsFound(restaurant_ids=missing_ids)
