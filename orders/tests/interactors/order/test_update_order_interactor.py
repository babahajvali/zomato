from contextlib import contextmanager
from unittest.mock import MagicMock, create_autospec, patch

import pytest

from orders.constants.enums import OrderStatus
from orders.exception.custom_exceptions import (
    InvalidOrderStatusTransition,
    OrderNotFound,
    UserNotRestaurantOwner,
)
from orders.interactors.order.update_order_interactor import UpdateOrderInteractor
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.tests.factories.interactor_factories import OrderDTOFactory


@contextmanager
def no_op_lock(*args, **kwargs):
    yield


class TestUpdateOrderStatusInteractor:
    def setup_method(self):
        self.order_storage = create_autospec(OrderStorageInterface)
        self.interactor = UpdateOrderInteractor(
            order_storage=self.order_storage,
        )
        self.interactor.restaurant_adapter = MagicMock()

    @patch(
        "orders.interactors.order.update_order_interactor.transaction.atomic",
        no_op_lock,
    )
    @patch("orders.interactors.order.update_order_interactor.redis_lock", no_op_lock)
    def test_update_order_status_successfully(self):
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            restaurant_id="restaurants-1",
            status=OrderStatus.PLACED.value,
        )
        updated_order_dto = OrderDTOFactory(
            order_id="orders-1",
            restaurant_id="restaurants-1",
            status=OrderStatus.CONFIRMED.value,
        )
        self.order_storage.get_order.side_effect = [
            order_dto,
            order_dto,
            order_dto,
        ]
        self.interactor.restaurant_adapter.get_restaurant_owner_id.return_value = (
            "owner-1"
        )
        self.order_storage.update_order_status.return_value = updated_order_dto

        result = self.interactor.update_order_status(
            order_id="orders-1",
            status=OrderStatus.CONFIRMED,
            user_id="owner-1",
        )

        assert result.order_id == "orders-1"
        assert result.status == OrderStatus.CONFIRMED.value
        self.order_storage.update_order_status.assert_called_once_with(
            order_id="orders-1",
            status=OrderStatus.CONFIRMED,
        )

    def test_update_order_status_raises_order_not_found(self):
        self.order_storage.get_order.return_value = None

        with pytest.raises(OrderNotFound) as exc:
            self.interactor.update_order_status(
                order_id="invalid-orders",
                status=OrderStatus.CONFIRMED,
                user_id="owner-1",
            )

        assert exc.value.order_id == "invalid-orders"
        self.interactor.restaurant_adapter.get_restaurant_owner_id.assert_not_called()
        self.order_storage.update_order_status.assert_not_called()

    def test_update_order_status_raises_user_is_not_restaurant_owner(self):
        self.order_storage.get_order.return_value = OrderDTOFactory(
            order_id="orders-1",
            restaurant_id="restaurants-1",
            status=OrderStatus.PLACED.value,
        )
        self.interactor.restaurant_adapter.get_restaurant_owner_id.return_value = (
            "owner-1"
        )

        with pytest.raises(UserNotRestaurantOwner) as exc:
            self.interactor.update_order_status(
                order_id="orders-1",
                status=OrderStatus.CONFIRMED,
                user_id="other-user",
            )

        assert exc.value.user_id == "other-user"
        self.order_storage.update_order_status.assert_not_called()

    @patch(
        "orders.interactors.order.update_order_interactor.transaction.atomic",
        no_op_lock,
    )
    @patch("orders.interactors.order.update_order_interactor.redis_lock", no_op_lock)
    def test_update_order_status_raises_invalid_transition(self):
        self.order_storage.get_order.return_value = OrderDTOFactory(
            order_id="orders-1",
            restaurant_id="restaurants-1",
            status=OrderStatus.PLACED.value,
        )
        self.interactor.restaurant_adapter.get_restaurant_owner_id.return_value = (
            "owner-1"
        )

        with pytest.raises(InvalidOrderStatusTransition) as exc:
            self.interactor.update_order_status(
                order_id="orders-1",
                status=OrderStatus.DELIVERED,
                user_id="owner-1",
            )

        assert exc.value.current_status == OrderStatus.PLACED.value
        assert exc.value.new_status == OrderStatus.DELIVERED.value
        assert exc.value.allowed == [OrderStatus.CONFIRMED.value]
        self.order_storage.update_order_status.assert_not_called()
