import pytest

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.restaurant import BaseBrowseRestaurantsTestCase
from restaurants.tests.factories.storage_factories import RestaurantFactory
import factory.random

factory.random.reseed_random(123)


@pytest.mark.django_db
class TestBrowseRestaurantsAPI(BaseBrowseRestaurantsTestCase):
    def test_browse_restaurants_with_valid_data_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7d5"

        RestaurantFactory(
            id=restaurant_id,
            name="Restaurant 1",
            description="Test restaurant",
            address="Test Address",
            pin_code="500001",
            is_deleted=False,
        )

        variables = {
            "params": {
                "limit": 3,
                "offset": 0,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_browse_restaurants_with_invalid_cuisine_type_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        UserFactory(id=user_id)
        cuisine_type = "invalid"
        variables = {
            "params": {
                "limit": 3,
                "offset": 0,
                "cuisineType": cuisine_type,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_browse_restaurants_with_invalid_min_rating_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        UserFactory(id=user_id)
        min_rating = -10

        variables = {
            "params": {
                "limit": 3,
                "offset": 0,
                "minRating": min_rating,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
