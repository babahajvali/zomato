from datetime import datetime, timezone, timedelta

import pytest

from accounts.tests.factories.storage_factories import UserFactory
from orders.constants.enums import OrderStatus
from orders.tests.api_tests.order import BaseTodayRestaurantOrdersTestCase
from orders.tests.factories import OrderFactory, OrderItemFactory
from restaurants.tests.factories.storage_factories import RestaurantFactory


@pytest.mark.django_db
class TestTodayRestaurantOrdersApi(BaseTodayRestaurantOrdersTestCase):
    def test_today_restaurant_orders_with_valid_data_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        other_restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7d0"
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        RestaurantFactory(id=other_restaurant_id, owner_id=user_id)

        included_order = OrderFactory(
            id="orders-1",
            customer_id="customer-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
        )
        included_order.created_at = datetime.now(timezone.utc).replace(
            microsecond=0
        ) - timedelta(minutes=2)
        included_order.save(update_fields=["created_at"])

        recent_order = OrderFactory(
            id="orders-2",
            customer_id="customer-2",
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
        )
        recent_order.created_at = datetime.now(timezone.utc).replace(microsecond=0)
        recent_order.save(update_fields=["created_at"])

        other_restaurant_order = OrderFactory(
            id="orders-3",
            customer_id="customer-3",
            restaurant_id=other_restaurant_id,
            status=OrderStatus.PLACED.value,
        )
        other_restaurant_order.created_at = included_order.created_at
        other_restaurant_order.save(update_fields=["created_at"])

        OrderItemFactory(
            order_id="orders-1",
            item_id="item-1",
            quantity=2,
            item_price=200.0,
        )
        OrderItemFactory(
            order_id="orders-1",
            item_id="item-2",
            quantity=1,
            item_price=150.0,
        )
        OrderItemFactory(
            order_id="orders-2",
            item_id="item-3",
            quantity=1,
            item_price=100.0,
        )

        variables = {"params": {"restaurantId": restaurant_id, "limit": 5, "offset": 0}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_today_restaurant_orders_with_user_is_not_restaurant_owner_raises_error(self, snapshot):
        owner_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7ce"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        UserFactory(id=owner_id)
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=owner_id)

        variables = {"params": {"restaurantId": restaurant_id, "limit": 5, "offset": 0}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
