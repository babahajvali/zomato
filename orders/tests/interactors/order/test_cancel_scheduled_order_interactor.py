from contextlib import contextmanager
from datetime import timedelta
from unittest.mock import create_autospec, patch

import pytest
from django.utils import timezone

from orders.constants.enums import OrderStatus
from orders.exception.custom_exceptions import (
    OrderAlreadyCancelled,
    OrderCancellationNotAllowed,
    OrderCancellationWindowExpired,
    OrderNotFound,
    OrderNotOwnedByUser,
)
from orders.interactors.order.cancel_scheduled_order_interactor import (
    CancelScheduledOrderInteractor,
)
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.tests.factories.interactor_factories import OrderDTOFactory


@contextmanager
def no_op_lock(*args, **kwargs):
    yield


TRANSACTION_ATOMIC = (
    "orders.interactors.order.cancel_scheduled_order_interactor.transaction.atomic"
)

REDIS_LOCK = "orders.interactors.order.cancel_scheduled_order_interactor.redis_lock"


class TestCancelScheduledOrderInteractor:
    def setup_method(self):
        self.order_storage = create_autospec(OrderStorageInterface)
        self.interactor = CancelScheduledOrderInteractor(
            order_storage=self.order_storage
        )

    @patch(TRANSACTION_ATOMIC, no_op_lock)
    @patch(REDIS_LOCK, no_op_lock)
    def test_cancel_scheduled_order_successfully_from_scheduled_status(self):
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
            status=OrderStatus.SCHEDULED,
        )
        cancelled_order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
            status=OrderStatus.CANCELLED,
        )
        self.order_storage.get_order.side_effect = [order_dto, order_dto]
        self.order_storage.update_order_status.return_value = cancelled_order_dto

        result = self.interactor.cancel_scheduled_order(
            order_id="orders-1",
            user_id="customer-1",
        )

        assert result.status == OrderStatus.CANCELLED
        self.order_storage.get_order_updated_at.assert_not_called()
        self.order_storage.update_order_status.assert_called_once_with(
            order_id="orders-1",
            status=OrderStatus.CANCELLED,
        )

    @patch(TRANSACTION_ATOMIC, no_op_lock)
    @patch(REDIS_LOCK, no_op_lock)
    def test_cancel_scheduled_order_successfully_from_recently_placed_status(self):
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
            status=OrderStatus.PLACED,
        )
        cancelled_order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
            status=OrderStatus.CANCELLED,
        )
        updated_at = timezone.now() - timedelta(minutes=1)
        self.order_storage.get_order.side_effect = [order_dto, order_dto]
        self.order_storage.get_order_updated_at.return_value = updated_at
        self.order_storage.update_order_status.return_value = cancelled_order_dto

        result = self.interactor.cancel_scheduled_order(
            order_id="orders-1",
            user_id="customer-1",
        )

        assert result.status == OrderStatus.CANCELLED
        self.order_storage.get_order_updated_at.assert_called_once_with(
            order_id="orders-1"
        )

    @pytest.mark.django_db
    def test_cancel_scheduled_order_raises_order_not_found(self):
        self.order_storage.get_order.return_value = None

        with pytest.raises(OrderNotFound):
            self.interactor.cancel_scheduled_order(
                order_id="invalid-orders",
                user_id="customer-1",
            )

    @pytest.mark.django_db
    def test_cancel_scheduled_order_raises_order_not_owned_by_user(self):
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
        )
        self.order_storage.get_order.side_effect = [order_dto]

        with pytest.raises(OrderNotOwnedByUser):
            self.interactor.cancel_scheduled_order(
                order_id="orders-1",
                user_id="other-user",
            )

    @patch(TRANSACTION_ATOMIC, no_op_lock)
    @patch(REDIS_LOCK, no_op_lock)
    def test_cancel_scheduled_order_raises_already_cancelled(self):
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
            status=OrderStatus.CANCELLED,
        )
        self.order_storage.get_order.side_effect = [order_dto, order_dto]

        with pytest.raises(OrderAlreadyCancelled):
            self.interactor.cancel_scheduled_order(
                order_id="orders-1",
                user_id="customer-1",
            )

    @patch(TRANSACTION_ATOMIC, no_op_lock)
    @patch(REDIS_LOCK, no_op_lock)
    def test_cancel_scheduled_order_raises_cancellation_window_expired_for_placed_order(
        self,
    ):
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
            status=OrderStatus.PLACED,
        )
        self.order_storage.get_order.side_effect = [order_dto, order_dto]
        self.order_storage.get_order_updated_at.return_value = (
            timezone.now() - timedelta(minutes=10)
        )

        with pytest.raises(OrderCancellationWindowExpired):
            self.interactor.cancel_scheduled_order(
                order_id="orders-1",
                user_id="customer-1",
            )

    @patch(TRANSACTION_ATOMIC, no_op_lock)
    @patch(REDIS_LOCK, no_op_lock)
    def test_cancel_scheduled_order_raises_not_cancellable_for_delivered_order(self):
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
            status=OrderStatus.DELIVERED,
        )
        self.order_storage.get_order.side_effect = [order_dto, order_dto]

        with pytest.raises(OrderCancellationNotAllowed):
            self.interactor.cancel_scheduled_order(
                order_id="orders-1",
                user_id="customer-1",
            )
