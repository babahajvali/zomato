from unittest.mock import create_autospec

import pytest

from restaurants.exception.custom_exceptions import (
    UserIsNotRestaurantOwner,
    RestaurantNotFound,
)
from restaurants.interactors.restaurant.menu_item_interactor import MenuItemInteractor
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.tests.factories.interactor_factories import MenuItemDTOFactory


class TestDeleteMenuItemInteractor:
    def setup_method(self):
        self.restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.interactor = MenuItemInteractor(
            restaurant_storage=self.restaurant_storage,
        )

    def test_delete_menu_item_success(self):
        menu_item_id = "menu-1"
        user_id = "user-123"

        existing_item = MenuItemDTOFactory(restaurant_id="restaurant-1")

        self.restaurant_storage.get_menu_item.return_value = existing_item
        self.restaurant_storage.get_restaurant_owner_id.return_value = user_id

        self.interactor.delete_menu_item(menu_item_id=menu_item_id, user_id=user_id)

        self.restaurant_storage.delete_menu_item.assert_called_once_with(
            menu_item_id=menu_item_id
        )

    def test_delete_menu_item_not_found(self):
        menu_item_id = "menu-1"

        self.restaurant_storage.get_menu_item.side_effect = RestaurantNotFound(
            restaurant_id=menu_item_id
        )

        with pytest.raises(RestaurantNotFound):
            self.interactor.delete_menu_item(
                menu_item_id=menu_item_id, user_id="user-123"
            )

        self.restaurant_storage.delete_menu_item.assert_not_called()

    def test_delete_menu_item_user_not_owner(self):
        menu_item_id = "menu-1"

        existing_item = MenuItemDTOFactory(restaurant_id="restaurant-1")

        self.restaurant_storage.get_menu_item.return_value = existing_item

        self.restaurant_storage.get_restaurant_owner_id.return_value = "owner-456"

        with pytest.raises(UserIsNotRestaurantOwner):
            self.interactor.delete_menu_item(
                menu_item_id=menu_item_id, user_id="user-123"
            )

        self.restaurant_storage.delete_menu_item.assert_not_called()
