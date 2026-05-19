from decimal import Decimal
import json
from typing import List

from restaurants.constants.enums import Category
from restaurants.interactors.dtos import CreateMenuItemDTO
from restaurants.interactors.restaurant.menu_item_interactor import MenuItemInteractor
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportMenuItems:
    def __init__(self, restaurant_storage: RestaurantStorageInterface):
        self.restaurant_storage = restaurant_storage

    def import_menu_items(self, file_path="./sample_data/menu_items.csv"):
        rows = list(read_csv(file_path=file_path))

        self._validate_rows(rows=rows)

        menu_items_dto = self._build_menu_item_dtos(rows=rows)

        interactor = MenuItemInteractor(restaurant_storage=self.restaurant_storage)

        return interactor.import_menu_items(create_item_dtos=menu_items_dto)

    @staticmethod
    def _validate_rows(rows):
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
            row["description"] = (row.get("description") or "").strip()
            row["price"] = Decimal(row["price"])
            row["category"] = row["category"].strip()
            row["is_veg"] = row.get("is_veg", "").strip()
            row["is_available"] = row.get("is_available", "True").strip()
            row["preparation_time_in_minutes"] = int(
                row["preparation_time_in_minutes"]
            )

    @staticmethod
    def _build_menu_item_dtos(rows) -> List[CreateMenuItemDTO]:
        return [
            CreateMenuItemDTO(
                id=row["id"],
                restaurant_id=row["restaurant"],
                name=row["name"],
                description=row["description"],
                price=row["price"],
                category=Category[row["category"]],
                is_veg=(row["is_veg"].lower() == "true"),
                is_available=(row["is_available"].lower() == "true"),
                preparation_time_in_minutes=row["preparation_time_in_minutes"],
                tags=json.loads(row["tags"]) if row.get("tags") else [],
            )
            for row in rows
        ]
