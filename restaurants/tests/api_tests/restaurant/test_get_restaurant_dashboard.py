import pytest

from accounts.tests.factories.storage_factories import UserFactory
from orders.constants.enums import OrderStatus
from orders.tests.factories import OrderFactory
from restaurants.tests.api_tests.restaurant import BaseGetRestaurantDashboardTestCase
from restaurants.tests.factories.storage_factories import (
    RestaurantFactory,
    MenuItemFactory,
    RestaurantReviewFactory,
)


@pytest.mark.django_db
class TestGetRestaurantDashboard(BaseGetRestaurantDashboardTestCase):
    def test_get_restaurant_dashboard_with_valid_data_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        order_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        item_id = "49bb508e-c6d1-4882-95fd-1991d103f7dg"
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        MenuItemFactory(restaurant_id=restaurant_id, id=item_id)
        OrderFactory(id=order_id, restaurant_id=restaurant_id)
        OrderFactory(restaurant_id=restaurant_id, status=OrderStatus.DELIVERED.value)
        RestaurantReviewFactory(restaurant_id=restaurant_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "dateFrom": "2026-04-20",
                "dateTo": "2026-04-27",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_restaurant_dashboard_with_restaurant_not_found_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        UserFactory(id=user_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "dateFrom": "2026-04-20",
                "dateTo": "2026-04-27",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_restaurant_dashboard_with_user_not_restaurant_owner_raises_error(
        self, snapshot
    ):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        order_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        item_id = "49bb508e-c6d1-4882-95fd-1991d103f7dg"
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id="Baba Hajvali")
        MenuItemFactory(restaurant_id=restaurant_id, id=item_id)
        OrderFactory(id=order_id, restaurant_id=restaurant_id)
        OrderFactory(restaurant_id=restaurant_id, status=OrderStatus.DELIVERED.value)
        RestaurantReviewFactory(restaurant_id=restaurant_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "dateFrom": "2026-04-20",
                "dateTo": "2026-04-27",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_restaurant_dashboard_with_invalid_date_range_raises_error(
        self, snapshot
    ):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        order_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        item_id = "49bb508e-c6d1-4882-95fd-1991d103f7dg"
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        MenuItemFactory(restaurant_id=restaurant_id, id=item_id)
        OrderFactory(id=order_id, restaurant_id=restaurant_id)
        OrderFactory(restaurant_id=restaurant_id, status=OrderStatus.DELIVERED.value)
        RestaurantReviewFactory(restaurant_id=restaurant_id)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "dateFrom": "2026-04-27",
                "dateTo": "2026-04-20",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
