from datetime import time

import pytest

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.restaurant import BaseGetScoredRestaurantsTestCase
from restaurants.tests.factories.storage_factories import (
    DeliveryZoneFactory,
    RestaurantFactory,
    RestaurantReviewFactory,
    RestaurantTimingFactory,
)


@pytest.mark.django_db
class TestGetScoredRestaurantsApi(BaseGetScoredRestaurantsTestCase):
    def test_get_scored_restaurants_successfully(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        UserFactory(id=user_id)
        restaurant = RestaurantFactory(
            id=restaurant_id,
            name="Restaurant 1",
            cuisine_type="INDIAN",
            is_deleted=False,
        )
        DeliveryZoneFactory(
            restaurant=restaurant,
            pin_code="500001",
        )
        RestaurantTimingFactory(
            id=1,
            restaurant=restaurant,
            day_of_week=1,
            open_time=time(0, 0),
            close_time=time(23, 59),
        )
        RestaurantReviewFactory(
            id=1,
            restaurant=restaurant,
            customer_id=user_id,
            rating=5,
            review_text="Great food",
        )

        variables = {
            "params": {
                "pincode": "500001",
                "limit": 10,
                "offset": 0,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_scored_restaurants_empty_list(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        variables = {
            "params": {
                "pincode": "500001",
                "limit": 10,
                "offset": 0,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_invalid_limit_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        variables = {
            "params": {
                "pincode": "500001",
                "limit": -1,
                "offset": 0,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_invalid_offset_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        variables = {
            "params": {
                "pincode": "500001",
                "limit": 10,
                "offset": -1,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
