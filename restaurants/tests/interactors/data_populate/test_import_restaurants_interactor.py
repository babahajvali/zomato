from unittest.mock import create_autospec, patch

import pytest

from restaurants.constants.enums import CuisineType
from restaurants.exception.custom_exceptions import DuplicateRestaurants
from restaurants.interactors.dtos import UpdateRestaurantDTO
from restaurants.interactors.populate_data.import_restaurants import (
    ImportRestaurants,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.tests.factories.interactor_factories import CreateRestaurantDTOFactory
from restaurants.tests.factories.interactor_factories import RestaurantDTOFactory


READ_CSV = "restaurants.interactors.populate_data.import_restaurants.read_csv"
VALIDATE_ROW = "restaurants.interactors.populate_data.import_restaurants.validate_row"


class TestImportRestaurants:
    def setup_method(self):
        self.restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.interactor = ImportRestaurants(
            restaurant_storage=self.restaurant_storage,
        )

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_restaurants_success(self, mock_read_csv, mock_validate_row):
        rows = [
            {
                "id": "restaurant-1",
                "name": " Spice Hub ",
                "owner_id": " 00000000-0000-0000-0000-000000000001 ",
                "description": "Popular spot",
                "cuisine_type": "Indian",
                "address": "12 Main Road",
                "pin_code": "560001",
                "is_veg_only": "true",
                "is_deleted": "false",
            }
        ]
        CreateRestaurantDTOFactory(
            id="restaurant-1",
            name="Spice Hub",
            owner_id="00000000-0000-0000-0000-000000000001",
            description="Popular spot",
            cuisine_type="Indian",
            address="12 Main Road",
            pin_code="560001",
            is_veg_only=True,
            is_deleted=False,
        )
        expected_result = ["created-restaurants"]
        mock_read_csv.return_value = rows

        self.restaurant_storage.get_existing_restaurant_dtos.return_value = []
        self.restaurant_storage.create_bulk_restaurants.return_value = expected_result
        self.restaurant_storage.update_bulk_restaurants.return_value = []

        result = self.interactor.import_restaurants(file_path="restaurants.csv")

        assert result == "1 restaurants created, 0 restaurants updated"

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_restaurants_duplicate_names(self, mock_read_csv, mock_validate_row):
        rows = [
            {
                "id": "restaurant-1",
                "name": " Spice Hub ",
                "owner_id": "00000000-0000-0000-0000-000000000001",
                "description": "Popular spot",
                "cuisine_type": "Indian",
                "address": "12 Main Road",
                "pin_code": "560001",
                "is_veg_only": "true",
                "is_deleted": "false",
            },
            {
                "id": "restaurant-2",
                "name": "Spice Hub",
                "owner_id": "00000000-0000-0000-0000-000000000002",
                "description": "Another branch",
                "cuisine_type": "Indian",
                "address": "14 Main Road",
                "pin_code": "560002",
                "is_veg_only": "false",
                "is_deleted": "false",
            },
        ]
        mock_read_csv.return_value = rows

        with pytest.raises(DuplicateRestaurants) as exc:
            self.interactor.import_restaurants(file_path="restaurants.csv")

        assert exc.value.names == ["Spice Hub"]
        self.restaurant_storage.get_existing_restaurant_dtos.assert_not_called()
        self.restaurant_storage.create_bulk_restaurants.assert_not_called()

    @patch(VALIDATE_ROW)
    @patch(READ_CSV)
    def test_import_restaurants_updates_existing(
        self, mock_read_csv, mock_validate_row
    ):
        rows = [
            {
                "id": "restaurant-1",
                "name": " Spice Hub ",
                "owner_id": "00000000-0000-0000-0000-000000000001",
                "description": "Popular spot",
                "cuisine_type": CuisineType.NORTH_INDIAN,
                "address": "12 Main Road",
                "pin_code": "560001",
                "is_veg_only": "true",
                "is_deleted": "false",
            }
        ]
        mock_read_csv.return_value = rows

        self.restaurant_storage.get_existing_restaurant_dtos.return_value = [
            RestaurantDTOFactory(id="existing-restaurant-id", name="Spice Hub")
        ]
        self.restaurant_storage.create_bulk_restaurants.return_value = []
        self.restaurant_storage.update_bulk_restaurants.return_value = ["updated"]

        result = self.interactor.import_restaurants(file_path="restaurants.csv")

        assert result == "0 restaurants created, 1 restaurants updated"
        self.restaurant_storage.create_bulk_restaurants.assert_not_called()
        self.restaurant_storage.update_bulk_restaurants.assert_called_once_with(
            [
                UpdateRestaurantDTO(
                    id="existing-restaurant-id",
                    name="Spice Hub",
                    owner_id="00000000-0000-0000-0000-000000000001",
                    description="Popular spot",
                    cuisine_type=CuisineType.NORTH_INDIAN,
                    address="12 Main Road",
                    pin_code="560001",
                    is_veg_only=True,
                    is_deleted=False,
                )
            ]
        )
