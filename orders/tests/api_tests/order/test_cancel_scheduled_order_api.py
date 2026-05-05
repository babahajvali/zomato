from contextlib import contextmanager
from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from accounts.tests.factories.storage_factories import UserFactory
from orders.constants.enums import OrderStatus
from orders.tests.api_tests.order import BaseCancelScheduledOrderTestCase
from orders.tests.factories.storage_factories import OrderFactory
from restaurants.models import Restaurant


@contextmanager
def no_op_lock(*args, **kwargs):
    yield


@pytest.mark.django_db
class TestCancelScheduledOrderApi(BaseCancelScheduledOrderTestCase):
    @patch(
        "orders.interactors.order.cancel_scheduled_order_interactor.redis_lock",
        no_op_lock,
    )
    def test_cancel_scheduled_order_successfully_from_scheduled_status(self, snapshot):
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

        OrderFactory(
            id="orders-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.SCHEDULED.value,
        )

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"orderId": "orders-1"}},
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch(
        "orders.interactors.order.cancel_scheduled_order_interactor.redis_lock",
        no_op_lock,
    )
    def test_cancel_scheduled_order_successfully_from_recently_placed_status(
        self, snapshot
    ):
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

        updated_at = datetime.now() - timedelta(minutes=1)
        order = OrderFactory(
            id="orders-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
        )
        order.updated_at = updated_at
        order.save(update_fields=["updated_at"])

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"orderId": "orders-1"}},
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch(
        "orders.interactors.order.cancel_scheduled_order_interactor.redis_lock",
        no_op_lock,
    )
    def test_cancel_scheduled_order_not_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"orderId": "invalid-orders"}},
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch(
        "orders.interactors.order.cancel_scheduled_order_interactor.redis_lock",
        no_op_lock,
    )
    def test_cancel_scheduled_order_not_belongs_to_user(self, snapshot):
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

        OrderFactory(
            id="orders-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.SCHEDULED.value,
        )

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"orderId": "orders-1"}},
            snapshot=snapshot,
            user_id=other_user_id,
        )

    @patch(
        "orders.interactors.order.cancel_scheduled_order_interactor.redis_lock",
        no_op_lock,
    )
    def test_cancel_scheduled_order_time_exceeded_for_placed_order(self, snapshot):
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

        updated_at = datetime.now() - timedelta(minutes=10)
        order = OrderFactory(
            id="orders-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.PLACED.value,
        )
        order.updated_at = updated_at
        order.save(update_fields=["updated_at"])

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"orderId": "orders-1"}},
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch(
        "orders.interactors.order.cancel_scheduled_order_interactor.redis_lock",
        no_op_lock,
    )
    def test_cancel_scheduled_order_already_cancelled(self, snapshot):
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

        OrderFactory(
            id="orders-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.CANCELLED.value,
        )

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"orderId": "orders-1"}},
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch(
        "orders.interactors.order.cancel_scheduled_order_interactor.redis_lock",
        no_op_lock,
    )
    def test_cancel_scheduled_order_not_cancellable_delivered_status(self, snapshot):
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

        OrderFactory(
            id="orders-1",
            customer_id=user_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.DELIVERED.value,
        )

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"orderId": "orders-1"}},
            snapshot=snapshot,
            user_id=user_id,
        )
