from datetime import timedelta
from contextlib import contextmanager
from unittest.mock import create_autospec, patch

import pytest
from django.core.cache import cache
from django.utils import timezone

from orders.constants.enums import OrderStatus
from orders.exception.custom_exceptions import (
    OrderCancellationWindowExpired,
    OrderNotOwnedByUser,
    OrderNotFound,
    OrderAlreadyCancelled,
    OrderCancellationNotAllowed,
)
from orders.interactors.order.order_interactor import OrderInteractor
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.tests.factories.interactor_factories import (
    OrderDTOFactory,
    OrderSummaryDTOFactory,
)


@contextmanager
def no_op_lock(*args, **kwargs):
    yield


TRANSACTION_ATOMIC = "orders.interactors.order.order_interactor.transaction.atomic"

REDIS_LOCK = "orders.interactors.order.order_interactor.redis_lock"


class TestOrderInteractor:
    def setup_method(self):
        cache.clear()
        self.order_storage = create_autospec(OrderStorageInterface)
        self.interactor = OrderInteractor(order_storage=self.order_storage)

    @patch(TRANSACTION_ATOMIC, no_op_lock)
    @patch(REDIS_LOCK, no_op_lock)
    def test_cancel_order_successfully(self):
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
            status=OrderStatus.PLACED,
            placed_at=timezone.now(),
        )
        cancelled_order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
            status=OrderStatus.CANCELLED,
        )
        self.order_storage.get_order.side_effect = [order_dto, order_dto]
        self.order_storage.get_order_updated_at.return_value = (
            timezone.now() - timedelta(minutes=1)
        )
        self.order_storage.update_order_status.return_value = cancelled_order_dto

        result = self.interactor.cancel_order(
            order_id="orders-1",
            user_id="customer-1",
        )

        assert result.order_id == "orders-1"
        assert result.status == OrderStatus.CANCELLED
        self.order_storage.update_order_status.assert_called_once_with(
            order_id="orders-1", status=OrderStatus.CANCELLED
        )

    @pytest.mark.django_db
    def test_cancel_order_raises_order_not_found(self):
        self.order_storage.get_order.return_value = None

        with pytest.raises(OrderNotFound) as exc:
            self.interactor.cancel_order(
                order_id="invalid-orders",
                user_id="customer-1",
            )

        assert exc.value.order_id == "invalid-orders"
        self.order_storage.update_order_status.assert_not_called()

    @pytest.mark.django_db
    def test_cancel_order_raises_order_does_not_belong_to_user(self):
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
        )
        self.order_storage.get_order.side_effect = [order_dto, order_dto]

        with pytest.raises(OrderNotOwnedByUser) as exc:
            self.interactor.cancel_order(
                order_id="orders-1",
                user_id="other-user",
            )

        assert exc.value.order_id == "orders-1"
        assert exc.value.user_id == "other-user"
        self.order_storage.update_order_status.assert_not_called()

    @pytest.mark.django_db
    def test_cancel_order_raises_cancellation_time_exceeded(self):
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
            status=OrderStatus.PLACED,
            placed_at=timezone.now() - timedelta(minutes=6),
        )
        self.order_storage.get_order.side_effect = [order_dto, order_dto]
        self.order_storage.get_order_updated_at.return_value = (
            timezone.now() - timedelta(minutes=6)
        )

        with pytest.raises(OrderCancellationWindowExpired) as exc:
            self.interactor.cancel_order(
                order_id="orders-1",
                user_id="customer-1",
            )

        assert exc.value.order_id == "orders-1"
        self.order_storage.update_order_status.assert_not_called()

    @patch(TRANSACTION_ATOMIC, no_op_lock)
    @patch(REDIS_LOCK, no_op_lock)
    def test_cancel_order_raises_already_cancelled(self):
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
            status=OrderStatus.CANCELLED,
        )

        self.order_storage.get_order_updated_at.return_value = (
            timezone.now() - timedelta(minutes=6)
        )
        self.order_storage.get_order.side_effect = [order_dto, order_dto]

        with pytest.raises(OrderAlreadyCancelled):
            self.interactor.cancel_order(
                order_id="orders-1",
                user_id="customer-1",
            )

        self.order_storage.update_order_status.assert_not_called()

    @patch(TRANSACTION_ATOMIC, no_op_lock)
    @patch(REDIS_LOCK, no_op_lock)
    def test_cancel_order_raises_order_not_cancellable(self):
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
            status=OrderStatus.DELIVERED,
        )

        self.order_storage.get_order_updated_at.return_value = (
            timezone.now() - timedelta(minutes=6)
        )
        self.order_storage.get_order.side_effect = [order_dto, order_dto]

        with pytest.raises(OrderCancellationNotAllowed):
            self.interactor.cancel_order(
                order_id="orders-1",
                user_id="customer-1",
            )

        self.order_storage.update_order_status.assert_not_called()

    @patch(TRANSACTION_ATOMIC, no_op_lock)
    @patch(REDIS_LOCK, no_op_lock)
    def test_cancel_order_at_boundary_time_allowed(self):
        placed_at = timezone.now() - timedelta(minutes=2) + timedelta(seconds=5)

        order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
            status=OrderStatus.PLACED,
            placed_at=placed_at,
        )

        cancelled_order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
            status=OrderStatus.CANCELLED,
        )

        self.order_storage.get_order.side_effect = [order_dto, order_dto]
        self.order_storage.get_order_updated_at.return_value = placed_at
        self.order_storage.update_order_status.return_value = cancelled_order_dto

        result = self.interactor.cancel_order(
            order_id="orders-1",
            user_id="customer-1",
        )

        assert result.status == OrderStatus.CANCELLED

    @patch(TRANSACTION_ATOMIC, no_op_lock)
    @patch(REDIS_LOCK, no_op_lock)
    def test_cancel_order_just_after_boundary_fails(self):
        from orders.constants.constants import CANCEL_TIME

        placed_at = (
            timezone.now() - timedelta(minutes=CANCEL_TIME) - timedelta(seconds=1)
        )

        order_dto = OrderDTOFactory(
            order_id="orders-1",
            customer_id="customer-1",
            status=OrderStatus.PLACED,
            placed_at=placed_at,
        )

        self.order_storage.get_order.side_effect = [order_dto, order_dto]
        self.order_storage.get_order_updated_at.return_value = placed_at

        with pytest.raises(OrderCancellationWindowExpired):
            self.interactor.cancel_order(
                order_id="orders-1",
                user_id="customer-1",
            )

    def test_user_orders_successfully(self):
        order_dtos = [
            OrderDTOFactory(order_id="orders-1", customer_id="customer-1"),
            OrderDTOFactory(order_id="orders-2", customer_id="customer-1"),
        ]
        self.order_storage.get_user_orders.return_value = order_dtos

        result = self.interactor.get_user_orders(
            user_id="customer-1",
            limit=10,
            offset=0,
        )

        assert result == order_dtos
        self.order_storage.get_user_orders.assert_called_once_with(
            user_id="customer-1",
            limit=10,
            offset=0,
        )

    def test_get_user_orders_empty_list(self):
        self.order_storage.get_user_orders.return_value = []

        result = self.interactor.get_user_orders(
            user_id="customer-1",
            limit=10,
            offset=0,
        )

        assert result == []
        self.order_storage.get_user_orders.assert_called_once_with(
            user_id="customer-1",
            limit=10,
            offset=0,
        )

    def test_get_order_successfully(self):
        placed_at = timezone.now()
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            status=OrderStatus.PLACED,
            placed_at=placed_at,
        )
        order_summary_dto = OrderSummaryDTOFactory(
            order_id="orders-1",
            status=OrderStatus.PLACED,
            placed_at=placed_at,
        )
        self.order_storage.get_order.return_value = order_dto
        self.order_storage.get_order_items.return_value = order_summary_dto.items

        result = self.interactor.get_order(order_id="orders-1")

        assert result == order_summary_dto
        self.order_storage.get_order_items.assert_called_once_with(order_id="orders-1")

    def test_get_order_raises_order_not_found(self):
        self.order_storage.get_order.return_value = None

        with pytest.raises(OrderNotFound) as exc:
            self.interactor.get_order(order_id="invalid-orders")

        assert exc.value.order_id == "invalid-orders"
