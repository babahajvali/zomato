from datetime import datetime, timezone

import pytest
from django.core.cache import cache

from accounts.tests.factories.storage_factories import UserFactory
from orders.constants.enums import OrderStatus
from orders.tests.api_tests.order import BaseUserScheduledOrdersTestCase
from orders.tests.factories import OrderFactory, OrderItemFactory
from restaurants.tests.factories.storage_factories import RestaurantFactory


@pytest.mark.django_db
class TestUserScheduledOrdersApi(BaseUserScheduledOrdersTestCase):
    def setup_method(self):
        cache.clear()

    def test_user_scheduled_orders_with_valid_data_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        other_user_id = "49bb508e-c6d1-4882-95fd-1991d103f7ce"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        UserFactory(id=user_id)
        UserFactory(id=other_user_id)
        RestaurantFactory(id=restaurant_id)

        first_order = OrderFactory(
            id="orders-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.SCHEDULED.value,
            scheduled_for=datetime(2026, 5, 5, 18, 0, tzinfo=timezone.utc),
        )
        first_order.created_at = datetime(2026, 5, 5, 10, 0, tzinfo=timezone.utc)
        first_order.save(update_fields=["created_at"])

        second_order = OrderFactory(
            id="orders-2",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.SCHEDULED.value,
            scheduled_for=datetime(2026, 5, 5, 19, 0, tzinfo=timezone.utc),
        )
        second_order.created_at = datetime(2026, 5, 5, 11, 0, tzinfo=timezone.utc)
        second_order.save(update_fields=["created_at"])

        OrderItemFactory(
            order_id="orders-1",
            item_id="item-1",
            quantity=2,
            item_price=200.0,
        )
        OrderItemFactory(
            order_id="orders-2",
            item_id="item-2",
            quantity=1,
            item_price=150.0,
        )

        OrderFactory(
            id="orders-3",
            customer_id=other_user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.SCHEDULED.value,
            scheduled_for=datetime(2026, 5, 5, 20, 0, tzinfo=timezone.utc),
        )

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"limit": 5, "offset": 0}},
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_user_scheduled_orders_with_empty_result_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"limit": 5, "offset": 0}},
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_user_scheduled_orders_with_pagination_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id)

        for i in range(1, 6):
            order = OrderFactory(
                id=f"orders-{i}",
                customer_id=user_id,
                restaurant_id=restaurant_id,
                status=OrderStatus.SCHEDULED.value,
                scheduled_for=datetime(2026, 5, 5, 12 + i, 0, tzinfo=timezone.utc),
            )
            order.created_at = datetime(2026, 5, 5, i, 0, tzinfo=timezone.utc)
            order.save(update_fields=["created_at"])
            OrderItemFactory(
                order_id=f"orders-{i}",
                item_id=f"item-{i}",
                quantity=1,
                item_price=100.0 + i,
            )

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"limit": 2, "offset": 1}},
            snapshot=snapshot,
            user_id=user_id,
        )
