from datetime import date
from decimal import Decimal
from unittest.mock import create_autospec

import pytest

from restaurants.exception.custom_exceptions import (
    InvalidDateRange,
    RestaurantNotFound,
    UserIsNotRestaurantOwner,
)
from restaurants.interactors.dtos import (
    DashboardFiltersDTO,
    RestaurantOrdersSummaryDTO,
    OrdersByStatusDTO,
    RatingSummaryDTO,
)
from restaurants.interactors.restaurant.restaurant_dashboard_interactor import (
    RestaurantDashboardInteractor,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.storage_interface.review_storage_interface import (
    ReviewStorageInterface,
)
from restaurants.adapter.order import OrderAdapter


class TestRestaurantDashboardInteractor:
    def setup_method(self):
        self.restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.review_storage = create_autospec(ReviewStorageInterface)

        self.interactor = RestaurantDashboardInteractor(
            restaurant_storage=self.restaurant_storage,
            review_storage=self.review_storage,
        )

        self.interactor.order_adapter = create_autospec(OrderAdapter)

    def test_get_restaurant_dashboard_success(self):
        dashboard_input = DashboardFiltersDTO(
            restaurant_id="restaurant-1",
            date_from=date(2026, 4, 20),
            date_to=date(2026, 4, 27),
            owner_id="user-123",
        )

        summary = RestaurantOrdersSummaryDTO(
            total_orders=100,
            total_revenue=Decimal("1000"),
            avg_order_value=Decimal("10"),
            total_cancelled=5,
            cancellation_rate=Decimal("0.05"),
        )

        orders_status = [
            OrdersByStatusDTO(status="DELIVERED", count=80),
            OrdersByStatusDTO(status="CANCELLED", count=20),
        ]

        rating_summary = RatingSummaryDTO(
            average_rating=Decimal("4.2"),
            total_reviews=50,
            distribution={"5": 30, "4": 20},
        )

        self.restaurant_storage.check_restaurant_is_exist.return_value = True
        self.restaurant_storage.get_restaurant_owner_id.return_value = "user-123"

        self.interactor.order_adapter.get_restaurant_orders_summary.return_value = (
            summary
        )
        self.interactor.order_adapter.get_orders_count_by_status.return_value = (
            orders_status
        )
        self.review_storage.get_rating_summary.return_value = rating_summary

        result = self.interactor.get_restaurant_dashboard(
            dashboard_filter_dto=dashboard_input
        )

        assert result.summary == summary
        assert result.orders_by_status == orders_status
        assert result.rating_summary == rating_summary

    def test_get_restaurant_dashboard_restaurant_not_found(self):
        dashboard_input = DashboardFiltersDTO(
            restaurant_id="restaurant-1",
            date_from=date(2026, 4, 20),
            date_to=date(2026, 4, 27),
            owner_id="user-123",
        )

        self.restaurant_storage.check_restaurant_is_exist.return_value = False

        with pytest.raises(RestaurantNotFound) as exc:
            self.interactor.get_restaurant_dashboard(
                dashboard_filter_dto=dashboard_input
            )

        assert exc.value.restaurant_id == "restaurant-1"

        self.restaurant_storage.get_restaurant_owner_id.assert_not_called()
        self.review_storage.get_rating_summary.assert_not_called()

    def test_get_restaurant_dashboard_user_not_owner(self):
        dashboard_input = DashboardFiltersDTO(
            restaurant_id="restaurant-1",
            date_from=date(2026, 4, 20),
            date_to=date(2026, 4, 27),
            owner_id="user-123",
        )

        self.restaurant_storage.check_restaurant_is_exist.return_value = True
        self.restaurant_storage.get_restaurant_owner_id.return_value = "owner-456"

        with pytest.raises(UserIsNotRestaurantOwner) as exc:
            self.interactor.get_restaurant_dashboard(
                dashboard_filter_dto=dashboard_input
            )

        assert exc.value.user_id == "user-123"

    def test_get_restaurant_dashboard_invalid_date_range(self):
        dashboard_input = DashboardFiltersDTO(
            restaurant_id="restaurant-1",
            date_from=date(2026, 4, 27),
            date_to=date(2026, 4, 20),  # invalid
            owner_id="user-123",
        )

        self.restaurant_storage.check_restaurant_is_exist.return_value = True
        self.restaurant_storage.get_restaurant_owner_id.return_value = "user-123"

        with pytest.raises(InvalidDateRange) as exc:
            self.interactor.get_restaurant_dashboard(
                dashboard_filter_dto=dashboard_input
            )

        assert exc.value.date_from == dashboard_input.date_from
        assert exc.value.date_to == dashboard_input.date_to
