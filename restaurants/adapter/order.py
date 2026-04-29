from datetime import date
from typing import List

from orders.app_service.service_interface import ServiceInterface
from restaurants.interactors.dtos import (
    RestaurantOrdersSummaryDTO,
    OrdersByStatusDTO,
    PeakHourDTO,
    TopSellingItemDTO,
)


class OrderAdapter:
    @property
    def interface(self):

        return ServiceInterface()

    def get_restaurant_orders_summary(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> RestaurantOrdersSummaryDTO:

        return self.interface.get_restaurant_orders_summary(
            restaurant_id=restaurant_id, date_from=date_from, date_to=date_to
        )

    def get_orders_count_by_status(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> List[OrdersByStatusDTO]:

        return self.interface.get_orders_count_by_status(
            restaurant_id=restaurant_id, date_from=date_from, date_to=date_to
        )

    def get_peak_hours(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> List[PeakHourDTO]:

        return self.interface.get_peak_hours(
            restaurant_id=restaurant_id, date_from=date_from, date_to=date_to
        )

    def get_top_selling_items(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> List[TopSellingItemDTO]:

        return self.interface.get_top_selling_items(
            restaurant_id=restaurant_id, date_from=date_from, date_to=date_to
        )
