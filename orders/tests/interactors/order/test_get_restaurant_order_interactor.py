from unittest.mock import MagicMock, create_autospec

import pytest
from django.utils import timezone

from orders.constants.enums import OrderStatus
from orders.exception.custom_exceptions import UserNotRestaurantOwner
from orders.interactors.order.get_restaurant_order_interactor import (
    GetRestaurantOrderInteractor,
)
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.tests.factories.interactor_factories import (
    OrderDTOFactory,
    OrderItemDTOFactory,
)


class TestGetRestaurantOrderInteractor:
    def setup_method(self):
        self.order_storage = create_autospec(OrderStorageInterface)
        self.interactor = GetRestaurantOrderInteractor(
            order_storage=self.order_storage,
        )
        self.interactor.restaurant_adapter = MagicMock()

    def test_get_restaurant_order_successfully(self):
        order_dtos = [
            OrderDTOFactory(order_id="orders-1", restaurant_id="restaurants-1"),
            OrderDTOFactory(order_id="orders-2", restaurant_id="restaurants-1"),
        ]
        self.interactor.restaurant_adapter.get_restaurant_owner_id.return_value = (
            "owner-1"
        )
        self.order_storage.get_restaurant_orders.return_value = order_dtos

        result = self.interactor.get_restaurant_orders(
            restaurant_id="restaurants-1",
            user_id="owner-1",
            limit=10,
            offset=0,
        )

        assert result == order_dtos
        self.order_storage.get_restaurant_orders.assert_called_once_with(
            restaurant_id="restaurants-1", limit=10, offset=0
        )

    def test_get_restaurant_order_raises_user_is_not_restaurant_owner(self):
        self.interactor.restaurant_adapter.get_restaurant_owner_id.return_value = (
            "owner-1"
        )

        with pytest.raises(UserNotRestaurantOwner) as exc:
            self.interactor.get_restaurant_orders(
                restaurant_id="restaurants-1",
                user_id="other-user",
                limit=10,
                offset=0,
            )

        assert exc.value.user_id == "other-user"
        self.order_storage.get_restaurant_orders.assert_not_called()

    def test_get_today_restaurant_orders_successfully(self):
        old_order = OrderDTOFactory(
            order_id="orders-1",
            restaurant_id="restaurants-1",
            customer_id="customer-1",
            status=OrderStatus.PLACED,
            placed_at=timezone.now() - timezone.timedelta(minutes=2),
        )
        recent_order = OrderDTOFactory(
            order_id="orders-2",
            restaurant_id="restaurants-1",
            customer_id="customer-2",
            status=OrderStatus.PLACED,
            placed_at=timezone.now(),
        )
        order_item_dtos = [
            OrderItemDTOFactory(order_id="orders-1", item_id="item-1"),
            OrderItemDTOFactory(order_id="orders-1", item_id="item-2", quantity=1),
        ]
        self.interactor.restaurant_adapter.get_restaurant_owner_id.return_value = (
            "owner-1"
        )
        self.order_storage.get_today_restaurant_orders.return_value = [
            recent_order,
            old_order,
        ]
        self.order_storage.get_orders_items.return_value = order_item_dtos

        result = self.interactor.get_today_restaurant_orders(
            restaurant_id="restaurants-1",
            user_id="owner-1",
            limit=10,
            offset=0,
        )

        assert len(result) == 1
        assert result[0].order_id == "orders-1"
        assert [item.item_id for item in result[0].items] == ["item-1", "item-2"]
        self.order_storage.get_today_restaurant_orders.assert_called_once_with(
            restaurant_id="restaurants-1", limit=10, offset=0
        )
        self.order_storage.get_orders_items.assert_called_once_with(
            order_ids=["orders-1"]
        )

    def test_get_today_restaurant_orders_returns_empty_for_recent_orders(self):
        recent_order = OrderDTOFactory(
            order_id="orders-1",
            restaurant_id="restaurants-1",
            placed_at=timezone.now(),
        )
        self.interactor.restaurant_adapter.get_restaurant_owner_id.return_value = (
            "owner-1"
        )
        self.order_storage.get_today_restaurant_orders.return_value = [recent_order]

        result = self.interactor.get_today_restaurant_orders(
            restaurant_id="restaurants-1",
            user_id="owner-1",
            limit=10,
            offset=0,
        )

        assert result == []
        self.order_storage.get_orders_items.assert_not_called()

    def test_get_today_restaurant_orders_raises_user_is_not_restaurant_owner(self):
        self.interactor.restaurant_adapter.get_restaurant_owner_id.return_value = (
            "owner-1"
        )

        with pytest.raises(UserNotRestaurantOwner) as exc:
            self.interactor.get_today_restaurant_orders(
                restaurant_id="restaurants-1",
                user_id="other-user",
                limit=10,
                offset=0,
            )

        assert exc.value.user_id == "other-user"
        self.order_storage.get_today_restaurant_orders.assert_not_called()

    def test_get_today_restaurant_orders_filters_cancellation_window(self):
        order_within_window = OrderDTOFactory(
            order_id="orders-1",
            restaurant_id="restaurants-1",
            customer_id="customer-1",
            status=OrderStatus.PLACED,
            placed_at=timezone.now() - timezone.timedelta(minutes=1),
        )
        order_outside_window = OrderDTOFactory(
            order_id="orders-2",
            restaurant_id="restaurants-1",
            customer_id="customer-2",
            status=OrderStatus.PLACED,
            placed_at=timezone.now() - timezone.timedelta(minutes=3),
        )
        order_item_dtos = [
            OrderItemDTOFactory(order_id="orders-2", item_id="item-1"),
        ]

        self.interactor.restaurant_adapter.get_restaurant_owner_id.return_value = (
            "owner-1"
        )
        self.order_storage.get_today_restaurant_orders.return_value = [
            order_within_window,
            order_outside_window,
        ]
        self.order_storage.get_orders_items.return_value = order_item_dtos

        result = self.interactor.get_today_restaurant_orders(
            restaurant_id="restaurants-1",
            user_id="owner-1",
            limit=10,
            offset=0,
        )

        assert len(result) == 2
        assert result[0].order_id == "orders-2"
        self.order_storage.get_orders_items.assert_called_once_with(
            order_ids=["orders-2"]
        )
