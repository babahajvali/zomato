from typing import List

from restaurants.exception.custom_exceptions import DuplicateRestaurants
from restaurants.interactors.dtos import CreateRestaurantDTO, UpdateRestaurantDTO
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportRestaurants:
    def __init__(self, restaurant_storage: RestaurantStorageInterface):
        self.restaurant_storage = restaurant_storage

    def import_restaurants(self, file_path="./sample_data/restaurants.csv"):
        rows = read_csv(file_path=file_path)

        names = self._parse_and_normalize_rows(rows=rows)

        self._validate_duplicate_names(names)

        restaurants_dto = self._build_restaurant_dtos(rows=rows)

        to_create, to_update = self._split_new_and_existing(
            restaurant_dtos=restaurants_dto,
            names=names,
        )

        created = (
            self.restaurant_storage.create_bulk_restaurants(to_create)
            if to_create
            else []
        )
        updated = (
            self.restaurant_storage.update_bulk_restaurants(to_update)
            if to_update
            else []
        )

        return f"{len(created)} restaurants created, {len(updated)} restaurants updated"

    def _split_new_and_existing(
        self,
        restaurant_dtos: List[CreateRestaurantDTO],
        names: List[str],
    ) -> tuple[List[CreateRestaurantDTO], List[UpdateRestaurantDTO]]:
        existing_restaurants = self.restaurant_storage.get_existing_restaurant_dtos(
            names
        )

        existing_lookup = {
            restaurant.name: restaurant.id for restaurant in existing_restaurants
        }

        to_create = []
        to_update = []

        for dto in restaurant_dtos:
            if dto.name in existing_lookup:
                to_update.append(
                    self._build_update_restaurant_dto(
                        restaurant_dto=dto,
                        restaurant_id=existing_lookup[dto.name],
                    )
                )
            else:
                to_create.append(dto)

        return to_create, to_update

    @staticmethod
    def _build_update_restaurant_dto(
        restaurant_dto: CreateRestaurantDTO,
        restaurant_id: str,
    ) -> UpdateRestaurantDTO:
        return UpdateRestaurantDTO(
            id=restaurant_id,
            name=restaurant_dto.name,
            owner_id=restaurant_dto.owner_id,
            description=restaurant_dto.description,
            cuisine_type=restaurant_dto.cuisine_type,
            address=restaurant_dto.address,
            pin_code=restaurant_dto.pin_code,
            is_veg_only=restaurant_dto.is_veg_only,
            is_deleted=restaurant_dto.is_deleted,
        )

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
                description=row.get("description") or "",
                cuisine_type=row["cuisine_type"],
                address=row["address"],
                pin_code=row["pin_code"],
                is_veg_only=row["is_veg_only"].strip().lower() == "true",
                is_deleted=row["is_deleted"].strip().lower() == "true",
            )
            for row in rows
        ]
