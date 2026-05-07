import pytest

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.review import BaseCreateReviewTestCase
from restaurants.tests.factories.storage_factories import (
    RestaurantFactory,
    RestaurantReviewFactory,
)


@pytest.mark.django_db
class TestCreateReviewApi(BaseCreateReviewTestCase):
    def test_create_review_successfully(self, snapshot):
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

    def test_create_review_restaurant_not_found(self, snapshot):
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

    def test_create_review_invalid_rating_low(self, snapshot):
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

    def test_create_review_invalid_rating_high(self, snapshot):
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

    def test_create_review_user_already_reviewed(self, snapshot):
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
