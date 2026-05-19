import pytest
from django.core.cache import cache

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.restaurant_timing import (
    BaseGetRestaurantTimingsTestCase,
)
from restaurants.tests.factories.storage_factories import (
    RestaurantFactory,
    RestaurantTimingFactory,
)


@pytest.mark.django_db
class TestGetRestaurantTimings(BaseGetRestaurantTimingsTestCase):
    def setup_method(self):
        cache.clear()

    def test_get_restaurant_timings_with_valid_data_success(self, snapshot):
        restaurant_id = "test-restaurants-id"

        RestaurantFactory(id=restaurant_id)
        RestaurantTimingFactory(id=2, restaurant_id=restaurant_id, day_of_week=3)
        RestaurantTimingFactory(id=3, restaurant_id=restaurant_id, day_of_week=4)
        RestaurantTimingFactory(id=4, restaurant_id=restaurant_id, day_of_week=5)

        variables = {"params": {"restaurantId": restaurant_id}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )

    def test_get_restaurant_timings_with_restaurant_not_found_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        UserFactory(id=user_id)
        restaurant_id = "test-restaurants-id"

        variables = {"params": {"restaurantId": restaurant_id}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
