import pytest
from django.core.cache import cache

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.review import BaseCreateReviewTestCase
from restaurants.tests.factories.storage_factories import (
    RestaurantFactory,
    RestaurantReviewFactory,
)


@pytest.mark.django_db
class TestCreateReviewApi(BaseCreateReviewTestCase):
    def setup_method(self):
        cache.clear()

    def test_create_review_with_valid_data_success(self, snapshot):
        # Arrange
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "rating": 4,
                "review": "Great food and excellent service!",
            }
        }

        # Act & Assert
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_create_review_with_restaurant_not_found_raises_error(self, snapshot):
        # Arrange
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "non-existent-restaurant"

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "rating": 4,
                "review": "Great food and excellent service!",
            }
        }

        # Act & Assert
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_create_review_with_invalid_rating_low_raises_error(self, snapshot):
        # Arrange
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "rating": 0,
                "review": "Poor experience",
            }
        }

        # Act & Assert
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_create_review_with_invalid_rating_high_raises_error(self, snapshot):
        # Arrange
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "rating": 6,
                "review": "Amazing experience",
            }
        }

        # Act & Assert
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_create_review_with_user_already_reviewed_success(self, snapshot):
        # Arrange
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)

        RestaurantReviewFactory(restaurant=restaurant)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "rating": 4,
                "review": "New review attempt",
            }
        }

        # Act & Assert
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
