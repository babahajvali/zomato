import pytest

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.restaurant import BaseDeleteMenuItemTestCase
from restaurants.tests.factories.storage_factories import (
    RestaurantFactory,
    MenuItemFactory,
)
import factory.random

factory.random.reseed_random(123)


@pytest.mark.django_db
class TestDeleteMenuItemApi(BaseDeleteMenuItemTestCase):
    def test_delete_menu_item_successfully(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        menu_item_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"

        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)

        MenuItemFactory(
            id=menu_item_id,
            restaurant_id=restaurant_id,
        )

        variables = {
            "params": {
                "menuItemId": menu_item_id,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_menu_item_not_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"

        UserFactory(id=user_id)

        variables = {
            "params": {
                "menuItemId": "49bb508e-c6d1-4882-95fd-1991d103f7aa",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_user_is_not_restaurant_owner(self, snapshot):
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
        )

        variables = {
            "params": {
                "menuItemId": menu_item_id,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
