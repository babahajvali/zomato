from datetime import datetime, timedelta

import pytest

from orders.constants.enums import OrderStatus
from orders.tests.api_tests.order import BaseAutoCancelOrderTestCase
from orders.tests.factories.storage_factories import OrderFactory
from restaurants.models import Restaurant


@pytest.mark.django_db
class TestAutoCancelOrderApi(BaseAutoCancelOrderTestCase):
    def test_auto_cancel_order_successfully(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        Restaurant.objects.create(
            id=restaurant_id,
            owner_id=user_id,
            name="Test Restaurant",
            cuisine_type="INDIAN",
            address="Test Address",
            pin_code="500001",
        )

        # Create orders in PLACED status (can be auto-cancelled)
        created_at = datetime.now() - timedelta(minutes=2)
        OrderFactory(
            id="orders-1",
            customer_id="customer-1",
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
            user_id="system-user",
        )

    def test_auto_cancel_order_not_found(self, snapshot):
        variables = {
            "params": {
                "orderId": "invalid-orders",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id="system-user",
        )

    def test_auto_cancel_order_already_delivered(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
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
            customer_id="customer-1",
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
            user_id="system-user",
        )

    def test_auto_cancel_order_already_cancelled(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
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
            customer_id="customer-1",
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
            user_id="system-user",
        )

    def test_auto_cancel_order_confirmed_status(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
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
            customer_id="customer-1",
            restaurant_id=restaurant_id,
            status=OrderStatus.CONFIRMED.value,
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
            user_id="system-user",
        )
