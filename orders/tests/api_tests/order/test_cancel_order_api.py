from datetime import datetime, timedelta
from contextlib import contextmanager
from unittest.mock import patch

import pytest
from django.core.cache import cache

from accounts.tests.factories.storage_factories import UserFactory
from orders.constants.enums import OrderStatus
from orders.tests.api_tests.order import BaseCancelOrderTestCase
from orders.tests.factories.storage_factories import OrderFactory
from restaurants.models import Restaurant


@contextmanager
def no_op_lock(*args, **kwargs):
    yield


@pytest.mark.django_db
class TestCancelOrderApi(BaseCancelOrderTestCase):
    def setup_method(self):
        cache.clear()

    @patch("orders.interactors.order.order_interactor.redis_lock", no_op_lock)
    def test_cancel_order_with_valid_data_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        Restaurant.objects.create(
            id=restaurant_id,
            owner_id=user_id,
            name="Test Restaurant",
            cuisine_type="INDIAN",
            address="Test Address",
            pin_code="500001",
        )

        created_at = datetime.now() - timedelta(minutes=2)
        OrderFactory(
            id="orders-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
            created_at=created_at,
        )

        variables = {
            "params": {
                "orderId": "orders-1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch("orders.interactors.order.order_interactor.redis_lock", no_op_lock)
    def test_cancel_order_with_not_found_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        variables = {
            "params": {
                "orderId": "invalid-orders",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch("orders.interactors.order.order_interactor.redis_lock", no_op_lock)
    def test_cancel_order_with_not_belongs_to_user_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        other_user_id = "49bb508e-c6d1-4882-95fd-1991d103f7ce"
        UserFactory(id=user_id)
        UserFactory(id=other_user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        Restaurant.objects.create(
            id=restaurant_id,
            owner_id=other_user_id,
            name="Test Restaurant",
            cuisine_type="INDIAN",
            address="Test Address",
            pin_code="500001",
        )

        created_at = datetime.now() - timedelta(minutes=2)
        OrderFactory(
            id="orders-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
            created_at=created_at,
        )

        variables = {
            "params": {
                "orderId": "orders-1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=other_user_id,
        )

    @patch("orders.interactors.order.order_interactor.redis_lock", no_op_lock)
    def test_cancel_order_with_time_exceeded_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        Restaurant.objects.create(
            id=restaurant_id,
            owner_id=user_id,
            name="Test Restaurant",
            cuisine_type="INDIAN",
            address="Test Address",
            pin_code="500001",
        )

        created_at = datetime.now() - timedelta(minutes=10)
        OrderFactory(
            id="orders-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
            created_at=created_at,
        )

        variables = {
            "params": {
                "orderId": "orders-1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch("orders.interactors.order.order_interactor.redis_lock", no_op_lock)
    def test_cancel_order_with_already_cancelled_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        Restaurant.objects.create(
            id=restaurant_id,
            owner_id=user_id,
            name="Test Restaurant",
            cuisine_type="INDIAN",
            address="Test Address",
            pin_code="500001",
        )

        created_at = datetime.now() - timedelta(minutes=2)
        OrderFactory(
            id="orders-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.CANCELLED.value,
            created_at=created_at,
        )

        variables = {
            "params": {
                "orderId": "orders-1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch("orders.interactors.order.order_interactor.redis_lock", no_op_lock)
    def test_cancel_order_with_not_cancellable_delivered_status_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        Restaurant.objects.create(
            id=restaurant_id,
            owner_id=user_id,
            name="Test Restaurant",
            cuisine_type="INDIAN",
            address="Test Address",
            pin_code="500001",
        )

        created_at = datetime.now() - timedelta(minutes=2)
        OrderFactory(
            id="orders-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.DELIVERED.value,
            created_at=created_at,
        )

        variables = {
            "params": {
                "orderId": "orders-1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
