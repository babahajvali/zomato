from django.test import TestCase

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.constants.enums import CuisineType
from restaurants.interactors.dtos import CreateRestaurantDTO
from restaurants.models import Restaurant
from restaurants.storages.restaurant_storage import RestaurantStorage
from restaurants.tests.factories.storage_factories import (
    MenuItemFactory,
    RestaurantFactory,
)


class TestRestaurantStorage(TestCase):
    def setUp(self):
        self.storage = RestaurantStorage()

    def test_create_bulk_restaurants_success(self):
        user = UserFactory(email="owner@example.com", role="OWNER")
        restaurants_dto = [
            CreateRestaurantDTO(
                id="restaurant-1",
                name="Spice Hub",
                owner_id=str(user.id),
                description="Popular spot",
                cuisine_type=CuisineType.NORTH_INDIAN,
                address="12 Main Road",
                pin_code="560001",
                is_veg_only=True,
                is_deleted=False,
            )
        ]

        result = self.storage.create_bulk_restaurants(restaurant_dtos=restaurants_dto)

        assert len(result) == 1
        assert Restaurant.objects.filter(name="Spice Hub").exists()

    def test_create_bulk_restaurants_with_owner_id(self):
        restaurants_dto = [
            CreateRestaurantDTO(
                id="restaurant-1",
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

        result = self.storage.create_bulk_restaurants(restaurant_dtos=restaurants_dto)

        assert len(result) == 1
        assert Restaurant.objects.filter(name="Spice Hub").exists()
        assert Restaurant.objects.filter(
            owner_id="00000000-0000-0000-0000-000000000001"
        ).exists()

    def test_get_existing_restaurants(self):
        RestaurantFactory(name="Spice Hub")
        RestaurantFactory(name="Cafe Nova")

        result = self.storage.get_existing_restaurants(
            names=["Spice Hub", "Other Name"],
        )

        assert result == ["Spice Hub"]

    def test_get_available_menu_items_by_restaurant(self):
        restaurant = RestaurantFactory()
        available_item = MenuItemFactory(
            restaurant=restaurant,
            name="Paneer Tikka",
            category="STARTER",
            is_available=True,
            tags=["spicy", "veg"],
        )
        MenuItemFactory(
            restaurant=restaurant,
            name="Hidden Item",
            is_available=False,
        )
        other_restaurant = RestaurantFactory()
        MenuItemFactory(
            restaurant=other_restaurant,
            name="Other Restaurant Item",
            is_available=True,
        )

        result = self.storage.get_available_menu_items_by_restaurant(
            restaurant_id=str(restaurant.id),
        )

        assert len(result) == 2

    def test_get_available_menu_items_by_restaurant_returns_sorted_items(self):
        restaurant = RestaurantFactory()
        MenuItemFactory(
            restaurant=restaurant,
            name="B Item",
            category="STARTER",
        )
        MenuItemFactory(
            restaurant=restaurant,
            name="A Item",
            category="STARTER",
        )

        result = self.storage.get_available_menu_items_by_restaurant(
            restaurant_id=str(restaurant.id),
        )

        assert [item.name for item in result] == ["A Item", "B Item"]
