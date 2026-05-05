from datetime import datetime, timezone

import pytest

from accounts.tests.factories.storage_factories import UserFactory
from orders.constants.enums import OrderStatus
from orders.tests.api_tests.order import BaseTodayRestaurantScheduledOrdersTestCase
from orders.tests.factories import OrderFactory, OrderItemFactory
from restaurants.tests.factories.storage_factories import RestaurantFactory


@pytest.mark.django_db
class TestTodayRestaurantScheduledOrdersApi(BaseTodayRestaurantScheduledOrdersTestCase):
    def test_today_restaurant_scheduled_orders_successfully(self, snapshot):
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
            status=OrderStatus.SCHEDULED.value,
            scheduled_for=datetime(2026, 5, 5, 18, 0, tzinfo=timezone.utc),
        )
        included_order.created_at = datetime.now(timezone.utc).replace(microsecond=0)
        included_order.save(update_fields=["created_at"])

        other_restaurant_order = OrderFactory(
            id="orders-2",
            customer_id="customer-2",
            restaurant_id=other_restaurant_id,
            status=OrderStatus.SCHEDULED.value,
            scheduled_for=datetime(2026, 5, 5, 19, 0, tzinfo=timezone.utc),
        )
        other_restaurant_order.created_at = included_order.created_at
        other_restaurant_order.save(update_fields=["created_at"])

        non_scheduled_order = OrderFactory(
            id="orders-3",
            customer_id="customer-3",
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
        )
        non_scheduled_order.created_at = included_order.created_at
        non_scheduled_order.save(update_fields=["created_at"])

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

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"restaurantId": restaurant_id, "limit": 5, "offset": 0}},
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_today_restaurant_scheduled_orders_user_is_not_restaurant_owner(
        self, snapshot
    ):
        owner_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7ce"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        UserFactory(id=owner_id)
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=owner_id)

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"restaurantId": restaurant_id, "limit": 5, "offset": 0}},
            snapshot=snapshot,
            user_id=user_id,
        )
