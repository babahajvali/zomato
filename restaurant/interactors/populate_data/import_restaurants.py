from typing import List

from restaurant.exception.custom_exceptions import AlreadyExistsRestaurant, DuplicateRestaurants, OwnerNotFound
from restaurant.interactors.dtos import CreateRestaurantDTO
from restaurant.interactors.storage_interface.restaurant_storage_interface import RestaurantStorageInterface
from utils.read_csv_util import read_csv, validate_row


class ImportRestaurants:

    def __init__(self, restaurant_storage_interface: RestaurantStorageInterface):
        self.restaurant_storage_interface = restaurant_storage_interface

    def import_restaurants(self, file_path="./sample_data/restaurants.csv"):
        rows = read_csv(file_path=file_path)

        names = []
        owner_emails = []
        for index, row in enumerate(rows, start=1):
            validate_row(row, ['name', 'owner_email'], f"restaurant row {index}")

            name = row['name'].strip()
            owner_email = row['owner_email'].strip().lower()
            
            row['name'] = name
            row['owner_email'] = owner_email

            names.append(name)
            owner_emails.append(owner_email)

        self._check_duplicate_names(names)
        self._check_existing_restaurants(names)

        restaurants_dto = [
            CreateRestaurantDTO(
                name=row['name'],
                owner_email=row['owner_email'],
                description=row['description'],
                cuisine_type=row['cuisine_type'],
                address=row['address'],
                pin_code=row['pin_code'],
                is_veg_only=row['is_veg_only'] == 'True',
                is_active=row['is_active'] == 'True'
            )
            for row in rows
        ]

        created_restaurants = self.restaurant_storage_interface.create_bulk_restaurants(
            restaurants_dto)

        return created_restaurants

    def _check_existing_restaurants(self, names: List[str]):
        existing_restaurants = self.restaurant_storage_interface.get_existing_restaurants(names)

        if existing_restaurants:
            raise AlreadyExistsRestaurant(names=existing_restaurants)

    @staticmethod
    def _check_duplicate_names(names: List[str]):
        seen = set()
        duplicates = []
        for name in names:
            if name in seen:
                duplicates.append(name)
            seen.add(name)
        
        if duplicates:
            raise DuplicateRestaurants(names=duplicates)
