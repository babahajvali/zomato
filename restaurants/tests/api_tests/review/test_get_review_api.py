import pytest
from django.core.cache import cache

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.review import BaseGetUserRestaurantReviewTestCase
from restaurants.tests.factories.storage_factories import (
    RestaurantFactory,
    RestaurantReviewFactory,
)


@pytest.mark.django_db
class TestGetUserRestaurantReviewApi(BaseGetUserRestaurantReviewTestCase):
    def setup_method(self):
        cache.clear()

    def test_get_user_restaurant_review_with_valid_data_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        other_user_id = "49bb508e-c6d1-4882-95fd-1991d103f7ce"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        UserFactory(id=user_id)
        UserFactory(id=other_user_id)
        RestaurantReviewFactory(
            id=1,
            restaurant=restaurant,
            customer_id=user_id,
            rating=4,
            review_text="Great food",
        )
        RestaurantReviewFactory(
            id=2,
            restaurant=restaurant,
            customer_id=other_user_id,
            rating=2,
            review_text="Not for me",
        )

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "userId": user_id,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_user_restaurant_review_with_missing_data_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id)
        UserFactory(id=user_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "userId": user_id,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
