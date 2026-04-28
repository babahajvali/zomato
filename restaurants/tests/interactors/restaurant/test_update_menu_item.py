from unittest.mock import create_autospec

import pytest

from restaurants.exception.custom_exceptions import (
    RestaurantNotFound,
    UserIsNotRestaurantOwner,
)
from restaurants.interactors.restaurant.menu_item_interactor import MenuItemInteractor
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.tests.factories.interactor_factories import (
    CreateMenuItemDTOFactory,
    MenuItemDTOFactory,
)


class TestUpdateMenuItemInteractor:
    def setup_method(self):
        self.restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.interactor = MenuItemInteractor(
            restaurant_storage=self.restaurant_storage,
        )

    def test_update_menu_item_success(self):
        update_dto = CreateMenuItemDTOFactory()
        update_dto.menu_item_id = "menu-1"

        existing_item = MenuItemDTOFactory(restaurant_id="restaurant-1")
        updated_item = MenuItemDTOFactory(restaurant_id="restaurant-1")

        self.restaurant_storage.get_menu_item.return_value = existing_item
        self.restaurant_storage.update_menu_item.return_value = updated_item
        self.restaurant_storage.get_restaurant_owner_id.return_value = "user-123"

        result = self.interactor.update_menu_item(
            update_menu_item_dto=update_dto, user_id="user-123"
        )

        assert result == updated_item
        self.restaurant_storage.update_menu_item.assert_called_once_with(
            update_menu_item_dto=update_dto
        )

    def test_update_menu_item_not_found(self):
        update_dto = CreateMenuItemDTOFactory()
        update_dto.menu_item_id = "menu-1"

        self.restaurant_storage.get_menu_item.side_effect = RestaurantNotFound(
            restaurant_id="menu-1"
        )

        with pytest.raises(RestaurantNotFound):
            self.interactor.update_menu_item(
                update_menu_item_dto=update_dto, user_id="user-123"
            )

        self.restaurant_storage.update_menu_item.assert_not_called()

    def test_update_menu_item_user_not_owner(self):
        update_dto = CreateMenuItemDTOFactory()
        update_dto.menu_item_id = "menu-1"

        existing_item = MenuItemDTOFactory(restaurant_id="restaurant-1")

        self.restaurant_storage.get_menu_item.return_value = existing_item

        self.restaurant_storage.get_restaurant_owner_id.return_value = "owner-456"

        with pytest.raises(UserIsNotRestaurantOwner):
            self.interactor.update_menu_item(
                update_menu_item_dto=update_dto, user_id="user-123"
            )

        self.restaurant_storage.update_menu_item.assert_not_called()
