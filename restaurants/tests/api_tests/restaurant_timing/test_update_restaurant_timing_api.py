import pytest

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.restaurant_timing import BaseUpdateRestaurantTiming
from restaurants.tests.factories.storage_factories import (
    RestaurantFactory,
    RestaurantTimingFactory,
)


@pytest.mark.django_db
class TestUpdateRestaurantTimingAPI(BaseUpdateRestaurantTiming):
    def test_update_restaurant_timing_successfully(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        timing_id = 1
        restaurant_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

        UserFactory(id=user_id)
        restaurant = RestaurantFactory(id=restaurant_id, owner_id=user_id)
        RestaurantTimingFactory(
            id=timing_id,
            restaurant=restaurant,
            day_of_week=1,
            open_time="10:00:00",
            close_time="22:00:00",
        )

        variables = {
            "params": {
                "id": timing_id,
                "openTime": "11:00:00",
                "closeTime": "23:00:00",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_update_restaurant_timing_not_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        timing_id = 999

        UserFactory(id=user_id)

        variables = {
            "params": {
                "id": timing_id,
                "openTime": "11:00:00",
                "closeTime": "23:00:00",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_update_restaurant_timing_user_not_owner(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        other_user_id = "99999999-9999-9999-9999-999999999999"
        timing_id = 1
        restaurant_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

        UserFactory(id=user_id)
        UserFactory(id=other_user_id)
        restaurant = RestaurantFactory(
            id=restaurant_id,
            owner_id=other_user_id,
        )
        RestaurantTimingFactory(
            id=timing_id,
            restaurant=restaurant,
            day_of_week=1,
            open_time="10:00:00",
            close_time="22:00:00",
        )

        variables = {
            "params": {
                "id": timing_id,
                "openTime": "11:00:00",
                "closeTime": "23:00:00",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_update_open_time_greater_than_close_time(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        timing_id = 1
        restaurant_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

        UserFactory(id=user_id)
        restaurant = RestaurantFactory(id=restaurant_id, owner_id=user_id)
        RestaurantTimingFactory(
            id=timing_id,
            restaurant=restaurant,
            day_of_week=1,
            open_time="10:00:00",
            close_time="22:00:00",
        )

        variables = {
            "params": {
                "id": timing_id,
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

    def test_update_only_open_time(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        timing_id = 1
        restaurant_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

        UserFactory(id=user_id)
        restaurant = RestaurantFactory(id=restaurant_id, owner_id=user_id)
        RestaurantTimingFactory(
            id=timing_id,
            restaurant=restaurant,
            day_of_week=1,
            open_time="10:00:00",
            close_time="22:00:00",
        )

        variables = {
            "params": {
                "id": timing_id,
                "openTime": "11:00:00",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_update_only_close_time(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        timing_id = 1
        restaurant_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

        UserFactory(id=user_id)
        restaurant = RestaurantFactory(id=restaurant_id, owner_id=user_id)
        RestaurantTimingFactory(
            id=timing_id,
            restaurant=restaurant,
            day_of_week=1,
            open_time="10:00:00",
            close_time="22:00:00",
        )

        variables = {
            "params": {
                "id": timing_id,
                "closeTime": "23:00:00",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_update_open_time_equal_to_existing_close_time(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        timing_id = 1
        restaurant_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

        UserFactory(id=user_id)
        restaurant = RestaurantFactory(id=restaurant_id, owner_id=user_id)
        RestaurantTimingFactory(
            id=timing_id,
            restaurant=restaurant,
            day_of_week=1,
            open_time="10:00:00",
            close_time="22:00:00",
        )

        variables = {
            "params": {
                "id": timing_id,
                "openTime": "22:00:00",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_update_close_time_equal_to_existing_open_time(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        timing_id = 1
        restaurant_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

        UserFactory(id=user_id)
        restaurant = RestaurantFactory(id=restaurant_id, owner_id=user_id)
        RestaurantTimingFactory(
            id=timing_id,
            restaurant=restaurant,
            day_of_week=1,
            open_time="10:00:00",
            close_time="22:00:00",
        )

        variables = {
            "params": {
                "id": timing_id,
                "closeTime": "10:00:00",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
