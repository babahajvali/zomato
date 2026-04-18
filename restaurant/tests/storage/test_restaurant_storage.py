from django.test import TestCase

from account.tests.factories.storage_factories import UserFactory
from restaurant.enums import CuisineType
from restaurant.interactors.dtos import CreateRestaurantDTO
from restaurant.exception.custom_exceptions import OwnerNotFound
from restaurant.models import Restaurant
from restaurant.storages.restaurant_storage import RestaurantStorage
from restaurant.tests.factories.storage_factories import RestaurantFactory


class TestRestaurantStorage(TestCase):
    def setUp(self):
        self.storage = RestaurantStorage()

    def test_create_bulk_restaurants_success(self):
        UserFactory(email="owner@example.com", role="OWNER")
        restaurants_dto = [
            CreateRestaurantDTO(
                name="Spice Hub",
                owner_email="owner@example.com",
                description="Popular spot",
                cuisine_type=CuisineType.NORTH_INDIAN,
                address="12 Main Road",
                pin_code="560001",
                is_veg_only=True,
                is_active=True,
            )
        ]

        result = self.storage.create_bulk_restaurants(restaurants_dto=restaurants_dto)

        assert len(result) == 1
        assert Restaurant.objects.filter(name="Spice Hub").exists()

    def test_create_bulk_restaurants_owner_not_found(self):
        UserFactory(email="owner@example.com", role="CUSTOMER")
        restaurants_dto = [
            CreateRestaurantDTO(
                name="Spice Hub",
                owner_email="owner@example.com",
                description="Popular spot",
                cuisine_type=CuisineType.NORTH_INDIAN,
                address="12 Main Road",
                pin_code="560001",
                is_veg_only=True,
                is_active=True,
            )
        ]

        with self.assertRaises(OwnerNotFound) as exc:
            self.storage.create_bulk_restaurants(restaurants_dto=restaurants_dto)

        assert exc.exception.email == "owner@example.com"

    def test_get_existing_restaurants(self):
        RestaurantFactory(name="Spice Hub")
        RestaurantFactory(name="Cafe Nova")

        result = self.storage.get_existing_restaurants(
            names=["Spice Hub", "Other Name"],
        )

        assert result == ["Spice Hub"]
