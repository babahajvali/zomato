from datetime import timedelta
from unittest.mock import create_autospec

import pytest
from django.utils import timezone

from order.constants.enums import OrderStatus
from order.exception.custom_exceptions import (
    OrderCancellationTimeExceeded,
    OrderCannotBeCancelled,
    OrderDoesNotBelongToUser,
    OrderNotFound,
)
from order.interactors.order.order_interactor import OrderInteractor
from order.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from order.tests.factories.dto_factories import OrderDTOFactory


class TestOrderInteractor:
    def setup_method(self):
        self.order_storage = create_autospec(OrderStorageInterface)
        self.interactor = OrderInteractor(order_storage=self.order_storage)

    def test_cancel_order_successfully(self):
        order_dto = OrderDTOFactory(
            order_id="order-1",
            customer_id="customer-1",
            status=OrderStatus.PLACED.value,
        )
        cancelled_order_dto = OrderDTOFactory(
            order_id="order-1",
            customer_id="customer-1",
            status=OrderStatus.CANCELLED.value,
        )
        self.order_storage.get_order.side_effect = [order_dto, order_dto]
        self.order_storage.get_order_placed_at.return_value = timezone.now()
        self.order_storage.cancel_order.return_value = cancelled_order_dto

        result = self.interactor.cancel_order(
            order_id="order-1",
            user_id="customer-1",
        )

        assert result.order_id == "order-1"
        assert result.status == OrderStatus.CANCELLED.value
        self.order_storage.cancel_order.assert_called_once_with(order_id="order-1")

    def test_cancel_order_raises_order_not_found(self):
        self.order_storage.get_order.return_value = None

        with pytest.raises(OrderNotFound) as exc:
            self.interactor.cancel_order(
                order_id="invalid-order",
                user_id="customer-1",
            )

        assert exc.value.order_id == "invalid-order"
        self.order_storage.cancel_order.assert_not_called()

    def test_cancel_order_raises_order_does_not_belong_to_user(self):
        order_dto = OrderDTOFactory(
            order_id="order-1",
            customer_id="customer-1",
        )
        self.order_storage.get_order.side_effect = [order_dto, order_dto]

        with pytest.raises(OrderDoesNotBelongToUser) as exc:
            self.interactor.cancel_order(
                order_id="order-1",
                user_id="other-user",
            )

        assert exc.value.order_id == "order-1"
        assert exc.value.user_id == "other-user"
        self.order_storage.cancel_order.assert_not_called()

    def test_cancel_order_raises_cancellation_time_exceeded(self):
        order_dto = OrderDTOFactory(
            order_id="order-1",
            customer_id="customer-1",
        )
        self.order_storage.get_order.side_effect = [order_dto, order_dto]
        self.order_storage.get_order_placed_at.return_value = (
            timezone.now() - timedelta(minutes=6)
        )

        with pytest.raises(OrderCancellationTimeExceeded) as exc:
            self.interactor.cancel_order(
                order_id="order-1",
                user_id="customer-1",
            )

        assert exc.value.order_id == "order-1"
        self.order_storage.cancel_order.assert_not_called()

    def test_auto_cancel_order_successfully(self):
        order_dto = OrderDTOFactory(
            order_id="order-1",
            status=OrderStatus.PLACED.value,
        )
        cancelled_order_dto = OrderDTOFactory(
            order_id="order-1",
            status=OrderStatus.CANCELLED.value,
        )
        self.order_storage.get_order.side_effect = [order_dto, order_dto]
        self.order_storage.cancel_order.return_value = cancelled_order_dto

        result = self.interactor.auto_cancel_order(order_id="order-1")

        assert result.order_id == "order-1"
        assert result.status == OrderStatus.CANCELLED.value
        self.order_storage.cancel_order.assert_called_once_with(order_id="order-1")

    def test_auto_cancel_order_raises_order_not_found(self):
        self.order_storage.get_order.return_value = None

        with pytest.raises(OrderNotFound) as exc:
            self.interactor.auto_cancel_order(order_id="invalid-order")

        assert exc.value.order_id == "invalid-order"
        self.order_storage.cancel_order.assert_not_called()

    def test_auto_cancel_order_raises_order_cannot_be_cancelled(self):
        order_dto = OrderDTOFactory(
            order_id="order-1",
            status=OrderStatus.CONFIRMED.value,
        )
        self.order_storage.get_order.side_effect = [order_dto, order_dto]

        with pytest.raises(OrderCannotBeCancelled) as exc:
            self.interactor.auto_cancel_order(order_id="order-1")

        assert exc.value.order_id == "order-1"
        self.order_storage.cancel_order.assert_not_called()

    def test_user_orders_successfully(self):
        order_dtos = [
            OrderDTOFactory(order_id="order-1", customer_id="customer-1"),
            OrderDTOFactory(order_id="order-2", customer_id="customer-1"),
        ]
        self.order_storage.get_user_orders.return_value = order_dtos

        result = self.interactor.get_user_orders(user_id="customer-1")

        assert result == order_dtos
        self.order_storage.get_user_orders.assert_called_once_with(
            user_id="customer-1"
        )

    def test_get_order_successfully(self):
        order_dto = OrderDTOFactory(order_id="order-1")
        self.order_storage.get_order.return_value = order_dto

        result = self.interactor.get_order(order_id="order-1")

        assert result == order_dto
        assert self.order_storage.get_order.call_count == 2

    def test_get_order_raises_order_not_found(self):
        self.order_storage.get_order.return_value = None

        with pytest.raises(OrderNotFound) as exc:
            self.interactor.get_order(order_id="invalid-order")

        assert exc.value.order_id == "invalid-order"
