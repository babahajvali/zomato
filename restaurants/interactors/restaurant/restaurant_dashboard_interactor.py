from datetime import date

from restaurants.adapter.order import OrderAdapter
from restaurants.exception.custom_exceptions import InvalidDateRange
from restaurants.interactors.dtos import DashboardFiltersDTO, RestaurantDashboardDTO
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.storage_interface.review_storage_interface import (
    ReviewStorageInterface,
)
from restaurants.mixins.restaurant_mixin import RestaurantMixin


class RestaurantDashboardInteractor(RestaurantMixin):
    def __init__(
        self,
        restaurant_storage: RestaurantStorageInterface,
        review_storage: ReviewStorageInterface,
    ):
        self.review_storage = review_storage
        self.restaurant_storage = restaurant_storage
        self.order_adapter = OrderAdapter()

    def get_restaurant_dashboard(
        self, dashboard_filter_dto: DashboardFiltersDTO
    ) -> RestaurantDashboardDTO:

        self.validate_restaurant_exists(
            restaurant_id=dashboard_filter_dto.restaurant_id,
            restaurant_storage=self.restaurant_storage,
        )
        self.validate_user_is_restaurant_owner(
            restaurant_id=dashboard_filter_dto.restaurant_id,
            user_id=dashboard_filter_dto.owner_id,
            restaurant_storage=self.restaurant_storage,
        )
        self._validate_date_range(
            date_from=dashboard_filter_dto.date_from,
            date_to=dashboard_filter_dto.date_to,
        )

        restaurant_orders_summary = self.order_adapter.get_restaurant_orders_summary(
            restaurant_id=dashboard_filter_dto.restaurant_id,
            date_from=dashboard_filter_dto.date_from,
            date_to=dashboard_filter_dto.date_to,
        )

        orders_status = self.order_adapter.get_orders_count_by_status(
            restaurant_id=dashboard_filter_dto.restaurant_id,
            date_from=dashboard_filter_dto.date_from,
            date_to=dashboard_filter_dto.date_to,
        )
        rating_summary = self.review_storage.get_rating_summary(
            restaurant_id=dashboard_filter_dto.restaurant_id
        )

        peak_hours = self.order_adapter.get_peak_hours(
            restaurant_id=dashboard_filter_dto.restaurant_id,
            date_from=dashboard_filter_dto.date_from,
            date_to=dashboard_filter_dto.date_to,
        )
        top_selling_items = self.order_adapter.get_top_selling_items(
            restaurant_id=dashboard_filter_dto.restaurant_id,
            date_from=dashboard_filter_dto.date_from,
            date_to=dashboard_filter_dto.date_to,
        )

        return RestaurantDashboardDTO(
            summary=restaurant_orders_summary,
            orders_by_status=orders_status,
            rating_summary=rating_summary,
            peak_hours=peak_hours,
            top_selling_items=top_selling_items,
        )

    @staticmethod
    def _validate_date_range(date_from: date, date_to: date):
        if date_from > date_to:
            raise InvalidDateRange(
                date_from=date_from,
                date_to=date_to,
            )
