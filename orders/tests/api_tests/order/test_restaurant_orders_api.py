import pytest

from accounts.tests.factories.storage_factories import UserFactory
from orders.constants.enums import OrderStatus
from orders.tests.api_tests.order import BaseRestaurantOrdersTestCase
from orders.tests.factories import OrderFactory
from restaurants.tests.factories.storage_factories import RestaurantFactory


@pytest.mark.django_db
class TestRestaurantOrdersApi(BaseRestaurantOrdersTestCase):
    def test_restaurant_orders_successfully(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        other_restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7d0"
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        RestaurantFactory(id=other_restaurant_id, owner_id=user_id)
        OrderFactory(
            id="orders-1",
            customer_id="customer-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
        )
        OrderFactory(
            id="orders-2",
            customer_id="customer-2",
            restaurant_id=restaurant_id,
            status=OrderStatus.CONFIRMED.value,
        )
        OrderFactory(
            id="orders-3",
            customer_id="customer-3",
            restaurant_id=other_restaurant_id,
            status=OrderStatus.PLACED.value,
        )

        variables = {"params": {"restaurantId": restaurant_id, "limit": 3, "offset": 0}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_user_is_not_restaurant_owner(self, snapshot):
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

    def test_restaurant_orders_empty(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)

        variables = {"params": {"restaurantId": restaurant_id, "limit": 5, "offset": 0}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_order_pagination(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        UserFactory(id=user_id)
        RestaurantFactory(id=restaurant_id, owner_id=user_id)

        # Create 5 orders for pagination testing
        for i in range(1, 6):
            OrderFactory(
                id=f"orders-{i}",
                customer_id=f"customer-{i}",
                restaurant_id=restaurant_id,
                status=OrderStatus.PLACED.value,
            )

        variables = {"params": {"restaurantId": restaurant_id, "limit": 2, "offset": 1}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
