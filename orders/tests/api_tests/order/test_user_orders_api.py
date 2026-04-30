import pytest

from accounts.tests.factories.storage_factories import UserFactory
from orders.constants.enums import OrderStatus
from orders.tests.api_tests.order import BaseUserOrdersTestCase
from orders.tests.factories import OrderFactory
from restaurants.tests.factories.storage_factories import RestaurantFactory


@pytest.mark.django_db
class TestUserOrdersApi(BaseUserOrdersTestCase):
    def test_user_orders_successfully(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        other_user_id = "49bb508e-c6d1-4882-95fd-1991d103f7ce"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        UserFactory(id=user_id)
        UserFactory(id=other_user_id)
        RestaurantFactory(id=restaurant_id)
        OrderFactory(
            id="orders-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
        )
        OrderFactory(
            id="orders-2",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.CONFIRMED.value,
        )
        OrderFactory(
            id="orders-3",
            customer_id=other_user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
        )

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"limit": 5, "offset": 0}},
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_user_orders_empty(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"limit": 5, "offset": 0}},
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_user_orders_pagination(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id)
        
        # Create 5 orders for pagination testing
        for i in range(1, 6):
            OrderFactory(
                id=f"orders-{i}",
                customer_id=user_id,
                restaurant_id=restaurant_id,
                status=OrderStatus.PLACED.value,
            )

        # Test first page with limit=2, offset=0
        variables = {"params": {"limit": 2, "offset": 0}}
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
