from unittest.mock import patch

import pytest
from django.core.cache import cache

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.restaurant import BaseCreateMenuItemsTestCase
from restaurants.tests.factories.storage_factories import RestaurantFactory
import factory.random

factory.random.reseed_random(123)


@pytest.mark.django_db
class TestCreateMenuItemsApi(BaseCreateMenuItemsTestCase):
    def setup_method(self):
        cache.clear()

    @patch("uuid.uuid4")
    def test_create_menu_items_with_valid_data_success(self, mock_uuid, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        mock_uuid.return_value = "49bb508e-c6d1-4882-95fd-1991d103f7fe"

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "menuItems": [
                    {
                        "name": "Chicken Biryani",
                        "description": "Test",
                        "price": 250.0,
                        "category": "MAIN_COURSE",
                        "isVeg": False,
                        "isAvailable": True,
                        "preparationTimeInMinutes": 30,
                        "tags": ["biryani", "spicy"],
                    }
                ],
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_create_menu_items_with_restaurant_not_found_raises_error(self, snapshot):
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        UserFactory(id=user_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "menuItems": [
                    {
                        "name": "Chicken Biryani",
                        "description": "Test",
                        "price": 250.0,
                        "category": "MAIN_COURSE",
                        "isVeg": False,
                        "isAvailable": True,
                        "preparationTimeInMinutes": 30,
                        "tags": ["biryani", "spicy"],
                    }
                ],
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_create_menu_items_with_user_not_restaurant_owner_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(
            id=restaurant_id, owner_id="49bb508e-c6d1-4882-95fd-1991d103f7gg"
        )

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "menuItems": [
                    {
                        "name": "Chicken Biryani",
                        "description": "Test",
                        "price": 250.0,
                        "category": "MAIN_COURSE",
                        "isVeg": False,
                        "isAvailable": True,
                        "preparationTimeInMinutes": 30,
                        "tags": ["biryani", "spicy"],
                    }
                ],
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_create_menu_items_with_invalid_categories_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id, owner_id=user_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "menuItems": [
                    {
                        "name": "Chicken Biryani",
                        "description": "Test",
                        "price": 250.0,
                        "category": "BABA",
                        "isVeg": False,
                        "isAvailable": True,
                        "preparationTimeInMinutes": 30,
                        "tags": ["biryani", "spicy"],
                    }
                ],
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
