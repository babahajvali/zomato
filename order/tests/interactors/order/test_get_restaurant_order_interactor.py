from unittest.mock import MagicMock, create_autospec

import pytest

from order.exception.custom_exceptions import UserIsNotRestaurantOwnerInOrder
from order.interactors.order.get_restaurant_order_interactor import (
    GetRestaurantOrderInteractor,
)
from order.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from order.tests.factories.dto_factories import OrderDTOFactory


class TestGetRestaurantOrderInteractor:
    def setup_method(self):
        self.order_storage = create_autospec(OrderStorageInterface)
        self.interactor = GetRestaurantOrderInteractor(
            order_storage=self.order_storage,
        )
        self.interactor.restaurant_adapter = MagicMock()

    def test_get_restaurant_order_successfully(self):
        order_dtos = [
            OrderDTOFactory(order_id="order-1", restaurant_id="restaurant-1"),
            OrderDTOFactory(order_id="order-2", restaurant_id="restaurant-1"),
        ]
        self.interactor.restaurant_adapter.get_restaurant_owner_id.return_value = (
            "owner-1"
        )
        self.order_storage.get_restaurant_orders.return_value = order_dtos

        result = self.interactor.get_restaurant_order(
            restaurant_id="restaurant-1",
            user_id="owner-1",
        )

        assert result == order_dtos
        self.order_storage.get_restaurant_orders.assert_called_once_with(
            restaurant_id="restaurant-1"
        )

    def test_get_restaurant_order_raises_user_is_not_restaurant_owner(self):
        self.interactor.restaurant_adapter.get_restaurant_owner_id.return_value = (
            "owner-1"
        )

        with pytest.raises(UserIsNotRestaurantOwnerInOrder) as exc:
            self.interactor.get_restaurant_order(
                restaurant_id="restaurant-1",
                user_id="other-user",
            )

        assert exc.value.user_id == "other-user"
        self.order_storage.get_restaurant_orders.assert_not_called()
