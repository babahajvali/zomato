from contextlib import contextmanager
from unittest.mock import patch

import pytest

from accounts.tests.factories.storage_factories import UserFactory
from orders.constants.enums import OrderStatus
from orders.tests.api_tests.order import BaseUpdateOrderStatusTestCase
from orders.tests.factories.storage_factories import OrderFactory
from restaurants.tests.factories.storage_factories import RestaurantFactory


@contextmanager
def no_op_lock(*args, **kwargs):
    yield


@pytest.mark.django_db
class TestUpdateOrderStatusApi(BaseUpdateOrderStatusTestCase):
    @patch("orders.interactors.order.update_order_interactor.redis_lock", no_op_lock)
    def test_update_order_status_successfully(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        OrderFactory(
            id="orders-1",
            customer_id="customer-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
        )

        variables = {
            "params": {
                "orderId": "orders-1",
                "status": OrderStatus.CONFIRMED.value,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_order_not_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        variables = {
            "params": {
                "orderId": "invalid-orders",
                "status": OrderStatus.CONFIRMED.value,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_user_is_not_restaurant_owner(self, snapshot):
        owner_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7ce"
        UserFactory(id=owner_id)
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id, owner_id=owner_id)
        OrderFactory(
            id="orders-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
        )

        variables = {
            "params": {
                "orderId": "orders-1",
                "status": OrderStatus.CONFIRMED.value,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_invalid_order_status_transition(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        OrderFactory(
            id="orders-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
        )

        variables = {
            "params": {
                "orderId": "orders-1",
                "status": OrderStatus.DELIVERED.value,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch("orders.interactors.order.update_order_interactor.redis_lock", no_op_lock)
    def test_update_status_confirmed_to_preparing(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        OrderFactory(
            id="orders-1",
            customer_id="customer-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.CONFIRMED.value,
        )

        variables = {
            "params": {
                "orderId": "orders-1",
                "status": OrderStatus.PREPARING.value,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch("orders.interactors.order.update_order_interactor.redis_lock", no_op_lock)
    def test_update_status_preparing_to_out_of_delivery(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        OrderFactory(
            id="orders-1",
            customer_id="customer-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.PREPARING.value,
        )

        variables = {
            "params": {
                "orderId": "orders-1",
                "status": OrderStatus.OUT_OF_DELIVERY.value,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch("orders.interactors.order.update_order_interactor.redis_lock", no_op_lock)
    def test_update_status_out_of_delivery_to_delivered(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        OrderFactory(
            id="orders-1",
            customer_id="customer-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.OUT_OF_DELIVERY.value,
        )

        variables = {
            "params": {
                "orderId": "orders-1",
                "status": OrderStatus.DELIVERED.value,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_update_status_on_cancelled_order(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        OrderFactory(
            id="orders-1",
            customer_id="customer-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.CANCELLED.value,
        )

        variables = {
            "params": {
                "orderId": "orders-1",
                "status": OrderStatus.PREPARING.value,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
