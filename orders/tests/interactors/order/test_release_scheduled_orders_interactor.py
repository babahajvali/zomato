from datetime import datetime, time
from contextlib import contextmanager
from unittest.mock import MagicMock, create_autospec, patch

import pytest
from django.utils import timezone

from orders.adapter.dtos import RestaurantTimingDTO
from orders.constants.enums import OrderStatus
from orders.interactors.order.release_scheduled_orders_interactor import (
    ReleaseScheduledOrdersInteractor,
)
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.tests.factories.interactor_factories import OrderDTOFactory


@contextmanager
def no_op_lock(*args, **kwargs):
    yield


TRANSACTION_ATOMIC = (
    "orders.interactors.order.release_scheduled_orders_interactor.transaction.atomic"
)


class TestReleaseScheduledOrdersInteractor:
    def setup_method(self):
        self.order_storage = create_autospec(OrderStorageInterface)
        self.interactor = ReleaseScheduledOrdersInteractor(
            order_storage=self.order_storage,
        )
        self.interactor.restaurant_adapter = MagicMock()

    @patch(TRANSACTION_ATOMIC, no_op_lock)
    def test_release_scheduled_orders_updates_order_to_placed(self):
        scheduled_order = OrderDTOFactory(
            order_id="orders-1",
            restaurant_id="restaurants-1",
            scheduled_for=timezone.make_aware(datetime(2026, 1, 1, 12, 0)),
        )

        self.order_storage.get_scheduled_orders_due_for_release.return_value = [
            scheduled_order
        ]
        self.order_storage.get_order_item_ids.return_value = ["item-1"]
        self.interactor.restaurant_adapter.get_unavailable_menu_items.return_value = []
        self.interactor.restaurant_adapter.get_restaurant_timing.return_value = (
            RestaurantTimingDTO(
                timing_id=1,
                restaurant_id="restaurants-1",
                day_of_week=4,
                open_time=time(10, 0),
                close_time=time(22, 0),
            )
        )

        self.interactor.release_scheduled_orders()

        self.order_storage.update_order_status.assert_called_once_with(
            order_id="orders-1",
            status=OrderStatus.PLACED,
        )

    @patch(TRANSACTION_ATOMIC, no_op_lock)
    def test_release_scheduled_orders_updates_order_to_cancelled_when_items_unavailable(
        self,
    ):
        scheduled_order = OrderDTOFactory(
            order_id="orders-1",
            restaurant_id="restaurants-1",
            scheduled_for=datetime(2026, 1, 1, 12, 0),
        )

        self.order_storage.get_scheduled_orders_due_for_release.return_value = [
            scheduled_order
        ]
        self.order_storage.get_order_item_ids.return_value = ["item-1"]
        self.interactor.restaurant_adapter.get_unavailable_menu_items.return_value = [
            "item-1"
        ]

        self.interactor.release_scheduled_orders()

        self.order_storage.update_order_status.assert_called_once_with(
            order_id="orders-1",
            status=OrderStatus.CANCELLED,
        )

    @patch(TRANSACTION_ATOMIC, no_op_lock)
    def test_release_scheduled_orders_updates_order_to_cancelled_when_restaurant_closed(
        self,
    ):
        scheduled_order = OrderDTOFactory(
            order_id="orders-1",
            restaurant_id="restaurants-1",
            scheduled_for=timezone.make_aware(datetime(2026, 1, 1, 9, 0)),
        )

        self.order_storage.get_scheduled_orders_due_for_release.return_value = [
            scheduled_order
        ]
        self.order_storage.get_order_item_ids.return_value = ["item-1"]
        self.interactor.restaurant_adapter.get_unavailable_menu_items.return_value = []
        self.interactor.restaurant_adapter.get_restaurant_timing.return_value = (
            RestaurantTimingDTO(
                timing_id=1,
                restaurant_id="restaurants-1",
                day_of_week=4,
                open_time=time(10, 0),
                close_time=time(22, 0),
            )
        )

        self.interactor.release_scheduled_orders()

        self.order_storage.update_order_status.assert_called_once_with(
            order_id="orders-1",
            status=OrderStatus.CANCELLED,
        )

    def test_should_cancel_returns_true_when_items_unavailable(self):
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            restaurant_id="restaurants-1",
            scheduled_for=datetime(2026, 1, 1, 12, 0),
        )

        self.order_storage.get_order_item_ids.return_value = ["item-1"]
        self.interactor.restaurant_adapter.get_unavailable_menu_items.return_value = [
            "item-1"
        ]

        result = self.interactor._should_cancel(order_dto=order_dto)

        assert result is True

    def test_should_cancel_returns_true_when_restaurant_closed(self):
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            restaurant_id="restaurants-1",
            scheduled_for=timezone.make_aware(datetime(2026, 1, 1, 9, 0)),
        )

        self.order_storage.get_order_item_ids.return_value = ["item-1"]
        self.interactor.restaurant_adapter.get_unavailable_menu_items.return_value = []
        self.interactor.restaurant_adapter.get_restaurant_timing.return_value = (
            RestaurantTimingDTO(
                timing_id=1,
                restaurant_id="restaurants-1",
                day_of_week=4,
                open_time=time(10, 0),
                close_time=time(22, 0),
            )
        )

        result = self.interactor._should_cancel(order_dto=order_dto)

        assert result is True

    def test_should_cancel_returns_false(self):
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            restaurant_id="restaurants-1",
            scheduled_for=timezone.make_aware(datetime(2026, 1, 1, 12, 0)),
        )

        self.order_storage.get_order_item_ids.return_value = ["item-1"]
        self.interactor.restaurant_adapter.get_unavailable_menu_items.return_value = []
        self.interactor.restaurant_adapter.get_restaurant_timing.return_value = (
            RestaurantTimingDTO(
                timing_id=1,
                restaurant_id="restaurants-1",
                day_of_week=4,
                open_time=time(10, 0),
                close_time=time(22, 0),
            )
        )

        result = self.interactor._should_cancel(order_dto=order_dto)

        assert result is False

    def test_has_unavailable_items_returns_true(self):
        self.order_storage.get_order_item_ids.return_value = ["item-1"]
        self.interactor.restaurant_adapter.get_unavailable_menu_items.return_value = [
            "item-1"
        ]

        result = self.interactor._has_unavailable_items(order_id="orders-1")

        assert result is True

    def test_has_unavailable_items_returns_false(self):
        self.order_storage.get_order_item_ids.return_value = ["item-1"]
        self.interactor.restaurant_adapter.get_unavailable_menu_items.return_value = []

        result = self.interactor._has_unavailable_items(order_id="orders-1")

        assert result is False

    def test_is_restaurant_closed_returns_true_when_timing_not_found(self):
        scheduled_for = timezone.make_aware(datetime(2026, 1, 1, 9, 0))

        self.interactor.restaurant_adapter.get_restaurant_timing.return_value = None

        result = self.interactor._is_restaurant_closed(
            scheduled_for=scheduled_for,
            restaurant_id="restaurants-1",
        )

        assert result is True

    def test_is_restaurant_closed_returns_true_when_outside_timing(self):
        scheduled_for = timezone.make_aware(datetime(2026, 1, 1, 23, 0))

        self.interactor.restaurant_adapter.get_restaurant_timing.return_value = (
            RestaurantTimingDTO(
                timing_id=1,
                restaurant_id="restaurants-1",
                day_of_week=4,
                open_time=time(10, 0),
                close_time=time(22, 0),
            )
        )

        result = self.interactor._is_restaurant_closed(
            scheduled_for=scheduled_for,
            restaurant_id="restaurants-1",
        )

        assert result is True

    def test_is_restaurant_closed_returns_false(self):
        scheduled_for = timezone.make_aware(datetime(2026, 1, 4, 12, 0))

        self.interactor.restaurant_adapter.get_restaurant_timing.return_value = (
            RestaurantTimingDTO(
                timing_id=1,
                restaurant_id="restaurants-1",
                day_of_week=4,
                open_time=time(10, 0),
                close_time=time(22, 0),
            )
        )

        result = self.interactor._is_restaurant_closed(
            scheduled_for=scheduled_for,
            restaurant_id="restaurants-1",
        )

        assert result is False
