from unittest.mock import create_autospec

from restaurants.interactors.restaurant.get_owner_restaurants_interactor import (
    GetOwnerRestaurantsInteractor,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.tests.factories.interactor_factories import RestaurantDTOFactory


class TestGetOwnerRestaurantsInteractor:
    def setup_method(self):
        self.restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.interactor = GetOwnerRestaurantsInteractor(
            restaurant_storage=self.restaurant_storage
        )

    def test_get_owner_restaurants_with_valid_data_success(self):
        restaurant = RestaurantDTOFactory(
            id="restaurant-1",
            name="Test Restaurant",
            description="Nice place",
            cuisine_type="Indian",
            address="Hyderabad",
            pin_code="500001",
            is_veg_only=True,
            is_deleted=False,
        )

        self.restaurant_storage.get_owner_restaurants.return_value = [restaurant]

        result = self.interactor.get_owner_restaurants(owner_id="owner-1")

        assert len(result) == 1

        dto = result[0]
        assert dto.id == "restaurant-1"
        assert dto.name == "Test Restaurant"
        assert dto.description == "Nice place"
        assert dto.cuisine_type == "Indian"
        assert dto.address == "Hyderabad"
        assert dto.pin_code == "500001"
        assert dto.is_veg_only is True
        assert dto.is_deleted is False

        self.restaurant_storage.get_owner_restaurants.assert_called_once_with(
            owner_id="owner-1"
        )

    def test_get_owner_restaurants_with_empty_result_success(self):
        self.restaurant_storage.get_owner_restaurants.return_value = []

        result = self.interactor.get_owner_restaurants(owner_id="owner-1")

        assert result == []
        self.restaurant_storage.get_owner_restaurants.assert_called_once_with(
            owner_id="owner-1"
        )

    def test_get_owner_restaurants_with_multiple_restaurants_success(self):
        r1 = RestaurantDTOFactory(id="r1")
        r2 = RestaurantDTOFactory(id="r2")

        self.restaurant_storage.get_owner_restaurants.return_value = [r1, r2]

        result = self.interactor.get_owner_restaurants(owner_id="owner-1")

        assert len(result) == 2
