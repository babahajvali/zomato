import pytest

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.restaurant_timing import (
    BaseCreateRestaurantTimingTestCase,
)
from restaurants.tests.factories.storage_factories import (
    RestaurantFactory,
)


@pytest.mark.django_db
class TestCreateRestaurantTimingAPI(BaseCreateRestaurantTimingTestCase):
    def test_create_restaurant_timing_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        restaurant_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "dayOfWeek": 1,
                "openTime": "10:00:00",
                "closeTime": "22:00:00",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_create_restaurant_timing_restaurant_not_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"

        UserFactory(id=user_id)

        variables = {
            "params": {
                "restaurantId": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                "dayOfWeek": 1,
                "openTime": "10:00:00",
                "closeTime": "22:00:00",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_create_restaurant_timing_user_not_owner(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        other_user_id = "99999999-9999-9999-9999-999999999999"
        restaurant_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

        UserFactory(id=user_id)
        UserFactory(id=other_user_id)
        RestaurantFactory(id=restaurant_id, owner_id=other_user_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "dayOfWeek": 2,
                "openTime": "10:00:00",
                "closeTime": "22:00:00",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_create_open_time_greater_than_close_time(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        restaurant_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "dayOfWeek": 3,
                "openTime": "23:00:00",
                "closeTime": "10:00:00",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_create_open_time_equal_to_close_time(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        restaurant_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "dayOfWeek": 4,
                "openTime": "10:00:00",
                "closeTime": "10:00:00",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_create_restaurant_timing_different_day(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        restaurant_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "dayOfWeek": 6,
                "openTime": "08:00:00",
                "closeTime": "20:00:00",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
