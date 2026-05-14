from decimal import Decimal
from typing import List
import json

from restaurants.constants.enums import Category
from restaurants.interactors.dtos import CreateMenuItemDTO
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.exception.custom_exceptions import InvalidRestaurantIds
from utils.read_csv_util import read_csv, validate_row


class ImportMenuItems:
    def __init__(self, restaurant_storage: RestaurantStorageInterface):
        self.restaurant_storage = restaurant_storage

    def import_menu_items(self, file_path="./sample_data/menu_items.csv"):
        rows = list(read_csv(file_path=file_path))

        restaurant_ids = self._parse_and_normalize_rows(rows=rows)

        self._validate_restaurants_exist(list(set(restaurant_ids)))

        menu_items_dto = self._build_menu_item_dtos(rows=rows)

        created_items = self.restaurant_storage.create_menu_items(
            menu_items_dto, restaurant_id=restaurant_ids[0]
        )

        return created_items

    def _validate_restaurants_exist(self, restaurant_ids: List[str]):
        existing_ids = self.restaurant_storage.get_restaurants_by_ids(restaurant_ids)

        existing_ids_set = set(existing_ids)
        missing_ids = [rid for rid in restaurant_ids if rid not in existing_ids_set]

        if missing_ids:
            raise InvalidRestaurantIds(restaurant_ids=missing_ids)

    @staticmethod
    def _parse_and_normalize_rows(rows) -> List[str]:
        restaurant_ids = []
        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                [
                    "id",
                    "restaurant",
                    "name",
                    "price",
                    "category",
                    "preparation_time_in_minutes",
                ],
                f"menu item row {index}",
            )
            row["id"] = row["id"].strip()
            row["restaurant"] = row["restaurant"].strip()
            row["name"] = row["name"].strip()
            restaurant_ids.append(row["restaurant"])

        return restaurant_ids

    @staticmethod
    def _build_menu_item_dtos(rows) -> List[CreateMenuItemDTO]:
        return [
            CreateMenuItemDTO(
                id=row["id"],
                restaurant_id=row["restaurant"],
                name=row["name"],
                description=row.get("description"),
                price=Decimal(row["price"]),
                category=Category[row["category"]],
                is_veg=(row.get("is_veg", "").strip().lower() == "true"),
                is_available=(
                    row.get("is_available", "True").strip().lower() == "true"
                ),
                preparation_time_in_minutes=int(row["preparation_time_in_minutes"]),
                tags=json.loads(row["tags"]) if row.get("tags") else [],
            )
            for row in rows
        ]
