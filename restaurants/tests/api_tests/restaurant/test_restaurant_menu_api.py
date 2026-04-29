import pytest

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.restaurant import BaseRestaurantMenuTestCase
from restaurants.tests.factories.storage_factories import (
    RestaurantFactory,
    MenuItemFactory,
)
import factory.random

factory.random.reseed_random(123)


@pytest.mark.django_db
class TestRestaurantMenuAPI(BaseRestaurantMenuTestCase):
    def test_get_restaurant_menu_successful(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        restaurant_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)

        MenuItemFactory(
            restaurant_id=restaurant_id,
            id="49bb508e-c6d1-4882-95fd-1991d103f7d5",
            name="Item 1",
            description="Test item",
            tags=["New_Item", "Best_Seller"],
        )

        variables = {
            "params": {
                "restaurantId": restaurant_id,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_restaurant_not_found(self, snapshot):
        restaurant_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"

        UserFactory(id=user_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
