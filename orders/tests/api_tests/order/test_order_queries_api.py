from datetime import datetime, timezone

import pytest

from accounts.tests.factories.storage_factories import UserFactory
from orders.constants.enums import OrderStatus
from orders.tests.api_tests.order import (
    BaseGetOrderTestCase,
)
from orders.tests.factories.storage_factories import (
    OrderFactory,
    OrderItemFactory,
    PromoCodeFactory,
)
from restaurants.tests.factories.storage_factories import RestaurantFactory


@pytest.mark.django_db
class TestGetOrderApi(BaseGetOrderTestCase):
    def test_get_order_with_valid_data_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id)
        promo_code = PromoCodeFactory(id=1)
        order = OrderFactory(
            id="orders-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            promo_code=promo_code,
            status=OrderStatus.PLACED.value,
        )
        order.created_at = datetime(2026, 4, 27, 5, 14, 41, 4573, tzinfo=timezone.utc)
        order.save(update_fields=["created_at"])
        OrderItemFactory(
            order_id="orders-1",
            item_id="item-1",
            quantity=2,
            item_price=200.0,
        )

        variables = {"params": {"orderId": "orders-1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_order_with_not_found_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        variables = {"params": {"orderId": "invalid-orders"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
