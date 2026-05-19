import pytest

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.restaurant import BaseGetOwnerRestaurantsTestCase
from restaurants.tests.factories.storage_factories import RestaurantFactory
@pytest.mark.django_db
class TestGetOwnerRestaurantsApi(BaseGetOwnerRestaurantsTestCase):
    def test_get_owner_restaurants_with_valid_data_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        RestaurantFactory(
            id="restaurant-1",
            owner_id=user_id,
            name="Restaurant 1",
            description="Restaurant 1 description",
            cuisine_type="INDIAN",
            address="Restaurant 1 address",
            pin_code="500000",
            is_deleted=False,
        )
        RestaurantFactory(
            id="restaurant-2",
            owner_id=user_id,
            name="Restaurant 2",
            description="Restaurant 2 description",
            cuisine_type="CHINESE",
            address="Restaurant 2 address",
            pin_code="500001",
            is_deleted=False,
        )

        self.execute_schema(
            query=self.QUERY,
            variables={},
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_owner_restaurants_with_empty_list_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        self.execute_schema(
            query=self.QUERY,
            variables={},
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_owner_restaurants_filters_deleted_with_valid_data_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        RestaurantFactory(
            id="restaurant-1",
            owner_id=user_id,
            name="Active Restaurant",
            description="Active restaurant description",
            address="Active restaurant address",
            pin_code="500002",
            is_deleted=False,
        )
        RestaurantFactory(
            id="restaurant-2",
            owner_id=user_id,
            name="Deleted Restaurant",
            description="Deleted restaurant description",
            address="Deleted restaurant address",
            pin_code="500003",
            is_deleted=True,
        )

        self.execute_schema(
            query=self.QUERY,
            variables={},
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_owner_restaurants_ordered_by_created_at_desc_with_valid_data_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        RestaurantFactory(
            id="restaurant-1",
            owner_id=user_id,
            name="Older Restaurant",
            description="Older restaurant description",
            address="Older restaurant address",
            pin_code="500004",
            is_deleted=False,
        )
        RestaurantFactory(
            id="restaurant-2",
            owner_id=user_id,
            name="Newer Restaurant",
            description="Newer restaurant description",
            address="Newer restaurant address",
            pin_code="500005",
            is_deleted=False,
        )

        self.execute_schema(
            query=self.QUERY,
            variables={},
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_owner_restaurants_with_unauthorized_owner_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        RestaurantFactory(
            id="restaurant-1",
            owner_id=user_id,
            name="Older Restaurant",
            description="Older restaurant description",
            address="Older restaurant address",
            pin_code="500004",
            is_deleted=False,
        )
        RestaurantFactory(
            id="restaurant-2",
            owner_id=user_id,
            name="Newer Restaurant",
            description="Newer restaurant description",
            address="Newer restaurant address",
            pin_code="500005",
            is_deleted=False,
        )

        self.execute_schema(
            query=self.QUERY,
            variables={},
            snapshot=snapshot,
            user_id=None,
        )
