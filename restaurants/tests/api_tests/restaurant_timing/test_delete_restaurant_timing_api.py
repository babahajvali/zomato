import pytest
from django.core.cache import cache

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.restaurant_timing import (
    BaseDeleteRestaurantTimingTestCase,
)
from restaurants.tests.factories.storage_factories import (
    RestaurantFactory,
    RestaurantTimingFactory,
)


@pytest.mark.django_db
class TestDeleteRestaurantTiming(BaseDeleteRestaurantTimingTestCase):
    def setup_method(self):
        cache.clear()

    def test_delete_restaurant_timing_success(self, snapshot):
        user_id = "user-id-123"
        restaurant_id = "restaurants-id-123"

        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)

        timing = RestaurantTimingFactory(id=0, restaurant_id=restaurant_id)

        variables = {"params": {"timingId": timing.id}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_restaurant_timing_not_found(self, snapshot):
        user_id = "user-id-123"
        restaurant_id = "restaurants-id-123"
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        id = 2

        variables = {"params": {"timingId": id}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_user_is_not_restaurant_owner(self, snapshot):
        user_id = "user-id-123"
        restaurant_id = "restaurants-id-123"
        RestaurantFactory(id=restaurant_id)

        timing = RestaurantTimingFactory(restaurant_id=restaurant_id)

        variables = {"params": {"timingId": timing.id}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
