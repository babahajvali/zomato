import pytest

from restaurants.tests.api_tests.review import BaseGetRestaurantReviewsTestCase
from restaurants.tests.factories.storage_factories import RestaurantFactory


@pytest.mark.django_db
class TestGetRestaurantReviewsApi(BaseGetRestaurantReviewsTestCase):
    def test_get_restaurant_reviews_successfully(self, snapshot):
        # Arrange
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        
        # Create existing reviews
        from restaurants.models import RestaurantReview
        RestaurantReview.objects.create(
            restaurant=restaurant,
            customer_id="user1",
            rating=5,
            review_text="Excellent food!"
        )
        RestaurantReview.objects.create(
            restaurant=restaurant,
            customer_id="user2",
            rating=3,
            review_text="Average service"
        )
        
        variables = {
            "params": {
                "restaurantId": restaurant_id
            }
        }
        
        # Act & Assert
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id="user1",  # Any user can access
        )

    def test_get_restaurant_reviews_empty(self, snapshot):
        # Arrange
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        
        variables = {
            "params": {
                "restaurantId": restaurant_id
            }
        }
        
        # Act & Assert
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id="user1",
        )

    def test_get_restaurant_reviews_not_found(self, snapshot):
        # Arrange
        restaurant_id = "non-existent-restaurant"
        
        variables = {
            "params": {
                "restaurantId": restaurant_id
            }
        }
        
        # Act & Assert
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id="user1",
        )

    def test_get_restaurant_reviews_unauthorized(self, snapshot):
        # Arrange
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        
        variables = {
            "params": {
                "restaurantId": restaurant_id
            }
        }
        
        # Act & Assert - No user authenticated
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=None,
        )
