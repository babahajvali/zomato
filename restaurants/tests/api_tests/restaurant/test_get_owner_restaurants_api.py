import pytest

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.restaurant import BaseGetOwnerRestaurantsTestCase
from restaurants.tests.factories.storage_factories import RestaurantFactory
import factory.random

factory.random.reseed_random(123)


@pytest.mark.django_db
class TestGetOwnerRestaurantsApi(BaseGetOwnerRestaurantsTestCase):
    def test_get_owner_restaurants_successfully(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        RestaurantFactory(
            id="restaurant-1",
            owner_id=user_id,
            name="Restaurant 1",
            cuisine_type="INDIAN",
            is_deleted=False,
        )
        RestaurantFactory(
            id="restaurant-2",
            owner_id=user_id,
            name="Restaurant 2",
            cuisine_type="CHINESE",
            is_deleted=False,
        )

        self.execute_schema(
            query=self.QUERY,
            variables={},
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_owner_restaurants_empty_list(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        self.execute_schema(
            query=self.QUERY,
            variables={},
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_owner_restaurants_filters_deleted(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        RestaurantFactory(
            id="restaurant-1",
            owner_id=user_id,
            name="Active Restaurant",
            is_deleted=False,
        )
        RestaurantFactory(
            id="restaurant-2",
            owner_id=user_id,
            name="Deleted Restaurant",
            is_deleted=True,
        )

        self.execute_schema(
            query=self.QUERY,
            variables={},
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_owner_restaurants_ordered_by_created_at_desc(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        RestaurantFactory(
            id="restaurant-1",
            owner_id=user_id,
            name="Older Restaurant",
            is_deleted=False,
        )
        RestaurantFactory(
            id="restaurant-2",
            owner_id=user_id,
            name="Newer Restaurant",
            is_deleted=False,
        )

        self.execute_schema(
            query=self.QUERY,
            variables={},
            snapshot=snapshot,
            user_id=user_id,
        )
