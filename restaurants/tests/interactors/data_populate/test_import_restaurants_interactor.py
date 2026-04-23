from unittest.mock import MagicMock, create_autospec, patch

import pytest

from restaurants.exception.custom_exceptions import (
    AlreadyExistsRestaurant,
    DuplicateRestaurants,
)
from restaurants.interactors.populate_data.import_restaurants import (
    ImportRestaurants,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.tests.factories.interactor_factories import CreateRestaurantDTOFactory


class TestImportRestaurants:
    def setup_method(self):
        self.restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.interactor = ImportRestaurants(
            restaurant_storage_interface=self.restaurant_storage,
        )

    def test_import_restaurants_success(self):
        rows = [
            {
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
        validate_row = MagicMock()

        self.restaurant_storage.get_existing_restaurants.return_value = []
        self.restaurant_storage.create_bulk_restaurants.return_value = expected_result

        with (
            patch(
                "restaurants.interactors.populate_data.import_restaurants.read_csv",
                return_value=rows,
            ),
            patch(
                "restaurants.interactors.populate_data.import_restaurants.validate_row",
                validate_row,
            ),
        ):
            result = self.interactor.import_restaurants(file_path="restaurants.csv")

        assert result == expected_result

    def test_import_restaurants_duplicate_names(self):
        rows = [
            {
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

        with (
            patch(
                "restaurants.interactors.populate_data.import_restaurants.read_csv",
                return_value=rows,
            ),
            patch(
                "restaurants.interactors.populate_data.import_restaurants.validate_row",
                MagicMock(),
            ),
        ):
            with pytest.raises(DuplicateRestaurants) as exc:
                self.interactor.import_restaurants(file_path="restaurants.csv")

        assert exc.value.names == ["Spice Hub"]
        self.restaurant_storage.get_existing_restaurants.assert_not_called()
        self.restaurant_storage.create_bulk_restaurants.assert_not_called()

    def test_import_restaurants_already_exists(self):
        rows = [
            {
                "name": " Spice Hub ",
                "owner_id": "00000000-0000-0000-0000-000000000001",
                "description": "Popular spot",
                "cuisine_type": "Indian",
                "address": "12 Main Road",
                "pin_code": "560001",
                "is_veg_only": "true",
                "is_deleted": "false",
            }
        ]

        self.restaurant_storage.get_existing_restaurants.return_value = ["Spice Hub"]

        with (
            patch(
                "restaurants.interactors.populate_data.import_restaurants.read_csv",
                return_value=rows,
            ),
            patch(
                "restaurants.interactors.populate_data.import_restaurants.validate_row",
                MagicMock(),
            ),
        ):
            with pytest.raises(AlreadyExistsRestaurant) as exc:
                self.interactor.import_restaurants(file_path="restaurants.csv")

        assert exc.value.names == ["Spice Hub"]
        self.restaurant_storage.create_bulk_restaurants.assert_not_called()
