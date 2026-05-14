from decimal import Decimal
from unittest.mock import create_autospec

import pytest

from orders.app_service.dtos import MenuItemOrderStatsDTO
from restaurants.exception.custom_exceptions import (
    RestaurantNotFound,
)
from restaurants.interactors.restaurant.get_scored_items_interactor import (
    GetScoredItemsInteractor,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.storage_interface.review_storage_interface import (
    ReviewStorageInterface,
)
from restaurants.tests.factories.interactor_factories import (
    MenuItemWithTagsDTOFactory,
    RatingSummaryDTOFactory,
)


class TestGetScoredItemsInteractor:
    def setup_method(self):
        self.restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.review_storage = create_autospec(ReviewStorageInterface)
        self.interactor = GetScoredItemsInteractor(
            restaurant_storage=self.restaurant_storage,
            review_storage=self.review_storage,
        )
        self.interactor.order_adapter = create_autospec(
            self.interactor.order_adapter, instance=True
        )

    def test_get_scored_restaurant_items_success(self):
        item_1 = MenuItemWithTagsDTOFactory(
            item_id="item-1",
            name="Paneer Tikka",
            price=Decimal("200.00"),
            is_available=True,
        )
        item_2 = MenuItemWithTagsDTOFactory(
            item_id="item-2",
            name="Noodles",
            price=Decimal("150.00"),
            is_available=True,
        )
        self.restaurant_storage.check_restaurant_is_exist.return_value = True
        self.restaurant_storage.get_available_menu_items_by_restaurant.return_value = [
            item_1,
            item_2,
        ]
        self.review_storage.get_rating_summary.return_value = RatingSummaryDTOFactory(
            average_rating=Decimal("5.00")
        )
        self.interactor.order_adapter.get_menu_item_order_stats.return_value = [
            MenuItemOrderStatsDTO(
                item_id="item-1",
                order_count=4,
                total_order_count=10,
            ),
            MenuItemOrderStatsDTO(
                item_id="item-2",
                order_count=1,
                total_order_count=2,
            ),
        ]

        result = self.interactor.get_scored_restaurant_items(
            restaurant_id="restaurant-1",
            user_id="user-1",
        )

        assert len(result) == 2
        assert result[0].menu_item_id == "item-1"
        assert result[0].restaurant_id == "restaurant-1"
        assert result[0].average_rating == Decimal("5.00")
        assert result[0].order_count == 4
        assert result[0].total_order_count == 10
        assert result[0].score == Decimal("1.0000")
        assert result[1].menu_item_id == "item-2"
        assert result[1].score == Decimal("0.4975")
        self.restaurant_storage.check_restaurant_is_exist.assert_called_once_with(
            restaurant_id="restaurant-1"
        )
        self.restaurant_storage.get_available_menu_items_by_restaurant.assert_called_once_with(
            restaurant_id="restaurant-1"
        )
        self.review_storage.get_rating_summary.assert_called_once_with(
            restaurant_id="restaurant-1"
        )
        self.interactor.order_adapter.get_menu_item_order_stats.assert_called_once_with(
            menu_item_ids=["item-1", "item-2"],
            user_id="user-1",
        )

    def test_get_scored_restaurant_items(self):
        items = [
            MenuItemWithTagsDTOFactory(item_id="item-1"),
            MenuItemWithTagsDTOFactory(item_id="item-2"),
            MenuItemWithTagsDTOFactory(item_id="item-3"),
        ]
        self.restaurant_storage.check_restaurant_is_exist.return_value = True
        self.restaurant_storage.get_available_menu_items_by_restaurant.return_value = (
            items
        )
        self.review_storage.get_rating_summary.return_value = RatingSummaryDTOFactory(
            average_rating=Decimal("5.00")
        )
        self.interactor.order_adapter.get_menu_item_order_stats.return_value = [
            MenuItemOrderStatsDTO(
                item_id="item-1",
                order_count=3,
                total_order_count=3,
            ),
            MenuItemOrderStatsDTO(
                item_id="item-2",
                order_count=2,
                total_order_count=2,
            ),
            MenuItemOrderStatsDTO(
                item_id="item-3",
                order_count=1,
                total_order_count=1,
            ),
        ]

        result = self.interactor.get_scored_restaurant_items(
            restaurant_id="restaurant-1",
            user_id="user-1",
        )

        assert len(result) == 3
        assert result[0].menu_item_id == "item-1"

    def test_get_scored_restaurant_items_defaults_missing_stats(self):
        self.restaurant_storage.check_restaurant_is_exist.return_value = True
        self.restaurant_storage.get_available_menu_items_by_restaurant.return_value = [
            MenuItemWithTagsDTOFactory(item_id="item-1")
        ]
        self.review_storage.get_rating_summary.return_value = RatingSummaryDTOFactory(
            average_rating=Decimal("0.00")
        )
        self.interactor.order_adapter.get_menu_item_order_stats.return_value = []

        result = self.interactor.get_scored_restaurant_items(
            restaurant_id="restaurant-1",
            user_id="user-1",
        )

        assert len(result) == 1
        assert result[0].order_count == 0
        assert result[0].total_order_count == 0
        assert result[0].score == Decimal("0.1500")

    def test_get_scored_restaurant_items_empty_results(self):
        self.restaurant_storage.check_restaurant_is_exist.return_value = True
        self.restaurant_storage.get_available_menu_items_by_restaurant.return_value = []

        result = self.interactor.get_scored_restaurant_items(
            restaurant_id="restaurant-1",
            user_id="user-1",
        )

        assert result == []
        self.review_storage.get_rating_summary.assert_not_called()
        self.interactor.order_adapter.get_menu_item_order_stats.assert_not_called()

    def test_get_scored_restaurant_items_restaurant_not_found(self):
        self.restaurant_storage.check_restaurant_is_exist.return_value = False

        with pytest.raises(RestaurantNotFound) as exc:
            self.interactor.get_scored_restaurant_items(
                restaurant_id="restaurant-404",
                user_id="user-1",
            )

        assert exc.value.restaurant_id == "restaurant-404"
        self.restaurant_storage.get_available_menu_items_by_restaurant.assert_not_called()
