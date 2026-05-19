from contextlib import contextmanager
from unittest.mock import patch

import pytest
from django.core.cache import cache

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
    def setup_method(self):
        cache.clear()

    @patch("orders.interactors.order.update_order_interactor.redis_lock", no_op_lock)
    def test_update_order_status_with_valid_data_success(self, snapshot):
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

    def test_update_order_status_with_order_not_found_raises_error(self, snapshot):
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

    def test_update_order_status_with_user_not_restaurant_owner_raises_error(self, snapshot):
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

    def test_update_order_status_with_invalid_transition_raises_error(self, snapshot):
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
    def test_update_order_status_with_confirmed_to_preparing_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        OrderFactory(
            id="orders-1",
            customer_id="customer-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.CONFIRMED.value,  # Start from CONFIRMED
        )

        variables = {
            "params": {
                "orderId": "orders-1",
                "status": OrderStatus.PREPARING.value,  # Transition to PREPARING
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch("orders.interactors.order.update_order_interactor.redis_lock", no_op_lock)
    def test_update_order_status_with_preparing_to_out_for_delivery_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        OrderFactory(
            id="orders-1",
            customer_id="customer-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.PREPARING.value,  # Start from PREPARING
        )

        variables = {
            "params": {
                "orderId": "orders-1",
                "status": OrderStatus.OUT_OF_DELIVERY.value,  # Transition to OUT_OF_DELIVERY
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch("orders.interactors.order.update_order_interactor.redis_lock", no_op_lock)
    def test_update_order_status_with_out_for_delivery_to_delivered_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        OrderFactory(
            id="orders-1",
            customer_id="customer-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.OUT_OF_DELIVERY.value,  # Start from OUT_OF_DELIVERY
        )

        variables = {
            "params": {
                "orderId": "orders-1",
                "status": OrderStatus.DELIVERED.value,  # Transition to DELIVERED
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_update_order_status_with_cancelled_order_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        OrderFactory(
            id="orders-1",
            customer_id="customer-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.CANCELLED.value,  # Start from CANCELLED
        )

        variables = {
            "params": {
                "orderId": "orders-1",
                "status": OrderStatus.PREPARING.value,  # Try to transition from CANCELLED
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
