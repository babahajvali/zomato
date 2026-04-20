from unittest.mock import patch

import pytest

from account.tests.factories.storage_factories import UserFactory
from restaurant.tests.api_tests.restaurant import BaseCreateMenuItemsTestCase
from restaurant.tests.factories.storage_factories import RestaurantFactory
import factory.random

factory.random.reseed_random(123)


@pytest.mark.django_db
class TestCreateMenuItemsApi(BaseCreateMenuItemsTestCase):

    @patch("uuid.uuid4")
    def test_create_enu_items_successfully(self, mock_uuid, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        mock_uuid.return_value = "49bb508e-c6d1-4882-95fd-1991d103f7fe"

        variables = {
            "params": {
                "menuItems": [
                    {
                        "restaurantId": restaurant_id,
                        "name": "Chicken Biryani",
                        "description": "Test",
                        "price": 250.0,
                        "category": "MAIN_COURSE",
                        "isVeg": False,
                        "isAvailable": True,
                        "preparationTimeInMinutes": 30,
                        "tags": ["biryani", "spicy"]
                    }
                ]
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_restaurant_not_found(self, snapshot):
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        UserFactory(id=user_id)


        variables = {
            "params": {
                "menuItems": [
                    {
                        "restaurantId": restaurant_id,
                        "name": "Chicken Biryani",
                        "description": "Test",
                        "price": 250.0,
                        "category": "MAIN_COURSE",
                        "isVeg": False,
                        "isAvailable": True,
                        "preparationTimeInMinutes": 30,
                        "tags": ["biryani", "spicy"]
                    }
                ]
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_user_is_not_restaurant_owner(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id, owner_id="49bb508e-c6d1-4882-95fd-1991d103f7gg")

        variables = {
            "params": {
                "menuItems": [
                    {
                        "restaurantId": restaurant_id,
                        "name": "Chicken Biryani",
                        "description": "Test",
                        "price": 250.0,
                        "category": "MAIN_COURSE",
                        "isVeg": False,
                        "isAvailable": True,
                        "preparationTimeInMinutes": 30,
                        "tags": ["biryani", "spicy"]
                    }
                ]
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_invalid_categories_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id, owner_id=user_id)

        variables = {
            "params": {
                "menuItems": [
                    {
                        "restaurantId": restaurant_id,
                        "name": "Chicken Biryani",
                        "description": "Test",
                        "price": 250.0,
                        "category": "BABA",
                        "isVeg": False,
                        "isAvailable": True,
                        "preparationTimeInMinutes": 30,
                        "tags": ["biryani", "spicy"]
                    }
                ]
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )