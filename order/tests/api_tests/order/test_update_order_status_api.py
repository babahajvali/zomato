from contextlib import contextmanager
from unittest.mock import patch

import pytest

from account.tests.factories.storage_factories import UserFactory
from order.constants.enums import OrderStatus
from order.tests.api_tests.order import BaseUpdateOrderStatusTestCase
from order.tests.factories.storage_factories import OrderFactory
from restaurant.tests.factories.storage_factories import RestaurantFactory


@contextmanager
def no_op_lock(*args, **kwargs):
    yield


@pytest.mark.django_db
class TestUpdateOrderStatusApi(BaseUpdateOrderStatusTestCase):
    @patch("order.interactors.order.update_order_interactor.redis_lock", no_op_lock)
    def test_update_order_status_successfully(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id, owner_id=user_id)
        OrderFactory(
            id="order-1",
            customer_id="customer-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
        )

        variables = {
            "params": {
                "orderId": "order-1",
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
                "orderId": "invalid-order",
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
            id="order-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
        )

        variables = {
            "params": {
                "orderId": "order-1",
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
            id="order-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
        )

        variables = {
            "params": {
                "orderId": "order-1",
                "status": OrderStatus.DELIVERED.value,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
