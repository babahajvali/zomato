from unittest.mock import create_autospec

import pytest
from django.core.cache import cache

from restaurants.constants.enums import Category
from restaurants.exception.custom_exceptions import RestaurantNotFound
from restaurants.interactors.restaurant.view_restaurant_menu import (
    ViewRestaurantMenuInteractor,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.tests.factories.interactor_factories import (
    MenuItemWithTagsDTOFactory,
)


class TestViewRestaurantMenuInteractor:
    def setup_method(self):
        cache.clear()
        self.restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.interactor = ViewRestaurantMenuInteractor(
            restaurant_storage=self.restaurant_storage,
        )

    def test_view_restaurant_menu_with_valid_data_success(self):
        starter_item = MenuItemWithTagsDTOFactory(
            item_id="item-1",
            category=Category.STARTER,
        )
        main_course_item = MenuItemWithTagsDTOFactory(
            item_id="item-2",
            category=Category.MAIN_COURSE,
        )
        self.restaurant_storage.check_restaurant_is_exist.return_value = True
        self.restaurant_storage.get_available_menu_items_by_restaurant.return_value = [
            starter_item,
            main_course_item,
        ]

        result = self.interactor.view_restaurant_menu(
            restaurant_id="restaurants-1",
        )

        assert result.restaurant_id == "restaurants-1"
        assert len(result.categories) == 2
        assert result.categories[0].category == Category.STARTER
        assert result.categories[0].items == [starter_item]
        assert result.categories[1].category == Category.MAIN_COURSE
        assert result.categories[1].items == [main_course_item]
        self.restaurant_storage.check_restaurant_is_exist.assert_called_once_with(
            restaurant_id="restaurants-1"
        )
        self.restaurant_storage.get_available_menu_items_by_restaurant.assert_called_once_with(
            restaurant_id="restaurants-1"
        )

    def test_view_restaurant_menu_with_same_category_items_success(self):
        item_1 = MenuItemWithTagsDTOFactory(
            item_id="item-1",
            category=Category.STARTER,
        )
        item_2 = MenuItemWithTagsDTOFactory(
            item_id="item-2",
            category=Category.STARTER,
        )
        self.restaurant_storage.check_restaurant_is_exist.return_value = True
        self.restaurant_storage.get_available_menu_items_by_restaurant.return_value = [
            item_1,
            item_2,
        ]

        result = self.interactor.view_restaurant_menu(
            restaurant_id="restaurants-1",
        )

        assert len(result.categories) == 1
        assert result.categories[0].category == Category.STARTER
        assert result.categories[0].items == [item_1, item_2]

    def test_view_restaurant_menu_with_empty_items_success(self):
        self.restaurant_storage.check_restaurant_is_exist.return_value = True
        self.restaurant_storage.get_available_menu_items_by_restaurant.return_value = []

        result = self.interactor.view_restaurant_menu(
            restaurant_id="restaurants-1",
        )

        assert result.restaurant_id == "restaurants-1"
        assert result.categories == []

    def test_view_restaurant_menu_with_restaurant_not_found_raises_error(self):
        self.restaurant_storage.check_restaurant_is_exist.return_value = False

        with pytest.raises(RestaurantNotFound) as exc:
            self.interactor.view_restaurant_menu(
                restaurant_id="restaurants-1",
            )

        assert exc.value.restaurant_id == "restaurants-1"
        self.restaurant_storage.get_available_menu_items_by_restaurant.assert_not_called()
