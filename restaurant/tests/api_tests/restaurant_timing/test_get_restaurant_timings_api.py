import pytest

from account.tests.factories.storage_factories import UserFactory
from restaurant.tests.api_tests.restaurant_timing import \
    BaseGetRestaurantTimingsTestCase
from restaurant.tests.factories.storage_factories import RestaurantFactory, \
    RestaurantTimingFactory

@pytest.mark.django_db
class TestGetRestaurantTimings(BaseGetRestaurantTimingsTestCase):

    def test_get_restaurant_timings_success(self, snapshot):
        restaurant_id = "test-restaurant-id"

        RestaurantFactory(id=restaurant_id)
        RestaurantTimingFactory.create_batch(
            3,
            restaurant_id=restaurant_id
        )

        variables = {
            "params": {
                "restaurantId": restaurant_id
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )

    def test_restaurant_not_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        UserFactory(id=user_id)
        restaurant_id = "test-restaurant-id"

        variables = {
            "params": {
                "restaurantId": restaurant_id
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )