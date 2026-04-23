from datetime import datetime, timedelta

import pytest

from account.tests.factories.storage_factories import UserFactory
from order.constants.enums import OrderStatus
from order.tests.api_tests.order import BaseCancelOrderTestCase
from order.tests.factories.storage_factories import OrderFactory
from restaurant.models import Restaurant


@pytest.mark.django_db
class TestCancelOrderApi(BaseCancelOrderTestCase):
    def test_cancel_order_successfully(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        Restaurant.objects.create(id=restaurant_id, owner_id=user_id, name="Test Restaurant", cuisine_type="INDIAN", address="Test Address", pin_code="500001")
        
        # Create order placed within cancellation window
        created_at = datetime.now() - timedelta(minutes=2)
        OrderFactory(
            id="order-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
            created_at=created_at,
        )

        variables = {
            "params": {
                "orderId": "order-1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_cancel_order_not_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        variables = {
            "params": {
                "orderId": "invalid-order",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_cancel_order_not_belongs_to_user(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        other_user_id = "49bb508e-c6d1-4882-95fd-1991d103f7ce"
        UserFactory(id=user_id)
        UserFactory(id=other_user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        Restaurant.objects.create(id=restaurant_id, owner_id=other_user_id, name="Test Restaurant", cuisine_type="INDIAN", address="Test Address", pin_code="500001")
        
        created_at = datetime.now() - timedelta(minutes=2)
        OrderFactory(
            id="order-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
            created_at=created_at,
        )

        variables = {
            "params": {
                "orderId": "order-1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=other_user_id,
        )

    def test_cancel_order_time_exceeded(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        Restaurant.objects.create(id=restaurant_id, owner_id=user_id, name="Test Restaurant", cuisine_type="INDIAN", address="Test Address", pin_code="500001")
        
        # Create order placed outside cancellation window (more than 5 minutes ago)
        created_at = datetime.now() - timedelta(minutes=10)
        OrderFactory(
            id="order-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
            created_at=created_at,
        )

        variables = {
            "params": {
                "orderId": "order-1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_cancel_order_already_cancelled(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        Restaurant.objects.create(id=restaurant_id, owner_id=user_id, name="Test Restaurant", cuisine_type="INDIAN", address="Test Address", pin_code="500001")
        
        created_at = datetime.now() - timedelta(minutes=2)
        OrderFactory(
            id="order-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.CANCELLED.value,
            created_at=created_at,
        )

        variables = {
            "params": {
                "orderId": "order-1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
