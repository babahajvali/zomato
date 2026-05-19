import pytest
from django.core.cache import cache

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.restaurant import BaseUpdateMenuItemTestCase
from restaurants.tests.factories.storage_factories import (
    RestaurantFactory,
    MenuItemFactory,
)
import factory.random

factory.random.reseed_random(123)


@pytest.mark.django_db
class TestUpdateMenuItemApi(BaseUpdateMenuItemTestCase):
    def setup_method(self):
        cache.clear()

    def test_update_menu_item_with_valid_data_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        menu_item_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"

        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)

        MenuItemFactory(
            id=menu_item_id,
            restaurant_id=restaurant_id,
            name="Old Name",
            description="Test item",
            is_available=True,
            price=100,
        )

        variables = {
            "params": {
                "menuItemId": menu_item_id,
                "isAvailable": False,
                "name": "Updated Name",
                "preparationTimeInMinutes": 15,
                "price": 200,
                "tags": ["updated", "spicy"],
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_update_menu_item_with_menu_item_not_found_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        UserFactory(id=user_id)

        variables = {
            "params": {
                "menuItemId": "49bb508e-c6d1-4882-95fd-1991d103f7aa",
                "isAvailable": False,
                "name": "Updated Name",
                "preparationTimeInMinutes": 15,
                "price": 200,
                "tags": ["updated"],
                "description": "Test item",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_update_menu_item_with_user_not_restaurant_owner_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        other_user_id = "49bb508e-c6d1-4882-95fd-1991d103f7aa"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        menu_item_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"

        UserFactory(id=user_id)
        UserFactory(id=other_user_id)

        RestaurantFactory(id=restaurant_id, owner_id=other_user_id)

        MenuItemFactory(
            id=menu_item_id,
            restaurant_id=restaurant_id,
            name="Old Name",
            is_available=True,
            price=100,
        )

        variables = {
            "params": {
                "menuItemId": menu_item_id,
                "isAvailable": False,
                "name": "Updated Name",
                "preparationTimeInMinutes": 15,
                "price": 200,
                "tags": ["updated"],
                "description": "Test item",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
