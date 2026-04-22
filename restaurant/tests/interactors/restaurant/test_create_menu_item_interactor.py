from unittest.mock import create_autospec

import pytest

from restaurant.exception.custom_exceptions import (
    InvalidCategoriesFound,
    RestaurantNotFound,
    UserIsNotRestaurantOwner,
)
from restaurant.interactors.restaurant.create_menu_item_interactor import (
    CreateMenuItemInteractor,
)
from restaurant.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurant.tests.factories.interactor_factories import (
    CreateMenuItemDTOFactory,
    MenuItemDTOFactory,
)


class TestCreateMenuItemInteractor:
    def setup_method(self):
        self.restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.interactor = CreateMenuItemInteractor(
            restaurant_storage=self.restaurant_storage,
        )

    def test_create_menu_item_success(self):
        create_items_dto = [
            CreateMenuItemDTOFactory(),
            CreateMenuItemDTOFactory(),
        ]
        expected_items = [
            MenuItemDTOFactory(restaurant_id="restaurant-1"),
            MenuItemDTOFactory(restaurant_id="restaurant-1"),
        ]

        self.restaurant_storage.check_restaurant_is_exist.return_value = True
        self.restaurant_storage.get_restaurant_owner_id.return_value = "user-123"
        self.restaurant_storage.create_menu_items.return_value = expected_items

        result = self.interactor.create_menu_item(
            create_items_dto=create_items_dto,
            user_id="user-123",
            restaurant_id="restaurant-1",
        )

        assert result == expected_items
        self.restaurant_storage.check_restaurant_is_exist.assert_called_once_with(
            restaurant_id="restaurant-1"
        )
        self.restaurant_storage.get_restaurant_owner_id.assert_called_once_with(
            restaurant_id="restaurant-1"
        )
        self.restaurant_storage.create_menu_items.assert_called_once_with(
            create_items_dto=create_items_dto,
            restaurant_id="restaurant-1"
        )

    def test_create_menu_item_restaurant_not_found(self):
        create_items_dto = [CreateMenuItemDTOFactory()]
        self.restaurant_storage.check_restaurant_is_exist.return_value = False

        with pytest.raises(RestaurantNotFound) as exc:
            self.interactor.create_menu_item(
                create_items_dto=create_items_dto,
                user_id="user-123",
                restaurant_id="restaurant-1",
            )

        assert exc.value.restaurant_id == "restaurant-1"
        self.restaurant_storage.get_restaurant_owner_id.assert_not_called()
        self.restaurant_storage.create_menu_items.assert_not_called()

    def test_create_menu_item_user_is_not_restaurant_owner(self):
        create_items_dto = [CreateMenuItemDTOFactory()]
        self.restaurant_storage.check_restaurant_is_exist.return_value = True
        self.restaurant_storage.get_restaurant_owner_id.return_value = "owner-456"

        with pytest.raises(UserIsNotRestaurantOwner) as exc:
            self.interactor.create_menu_item(
                create_items_dto=create_items_dto,
                user_id="user-123",
                restaurant_id="restaurant-1",
            )

        assert exc.value.user_id == "user-123"
        self.restaurant_storage.create_menu_items.assert_not_called()

    def test_create_menu_item_invalid_category(self):
        invalid_category = create_autospec(object)
        invalid_category.value = "INVALID_CATEGORY"
        create_items_dto = [
            CreateMenuItemDTOFactory(
                category=invalid_category,
            ),
            CreateMenuItemDTOFactory(
                category=invalid_category,
            ),
        ]
        self.restaurant_storage.check_restaurant_is_exist.return_value = True
        self.restaurant_storage.get_restaurant_owner_id.return_value = "user-123"

        with pytest.raises(InvalidCategoriesFound) as exc:
            self.interactor.create_menu_item(
                create_items_dto=create_items_dto,
                user_id="user-123",
                restaurant_id="restaurant-1",
            )

        assert exc.value.categories == ["INVALID_CATEGORY", "INVALID_CATEGORY"]
        self.restaurant_storage.create_menu_items.assert_not_called()
