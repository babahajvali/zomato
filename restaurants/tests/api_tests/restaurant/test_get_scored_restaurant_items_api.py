import pytest

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.restaurant import BaseGetScoredRestaurantItemsTestCase
from restaurants.tests.factories.storage_factories import (
    MenuItemFactory,
    RestaurantFactory,
    RestaurantReviewFactory,
)


@pytest.mark.django_db
class TestGetScoredRestaurantItemsApi(BaseGetScoredRestaurantItemsTestCase):
    def test_get_scored_restaurant_items_with_valid_data_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        UserFactory(id=user_id)
        restaurant = RestaurantFactory(id=restaurant_id, name="Restaurant 1")
        MenuItemFactory(
            id="49bb508e-c6d1-4882-95fd-1991d103f7de",
            restaurant=restaurant,
            name="Paneer Tikka",
            price=200.0,
            is_available=True,
        )
        RestaurantReviewFactory(
            id=1,
            restaurant=restaurant,
            customer_id=user_id,
            rating=5,
            review_text="Great food",
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

    def test_get_scored_restaurant_items_with_empty_list_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, name="Restaurant 1")

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

    def test_get_scored_restaurant_items_with_restaurant_not_found_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        variables = {
            "params": {
                "restaurantId": "49bb508e-c6d1-4882-95fd-1991d103f7df",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
