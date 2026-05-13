from datetime import date
from typing import List

from orders.app_service.service_interface import ServiceInterface
from restaurants.interactors.dtos import (
    RestaurantOrdersSummaryDTO,
    OrdersByStatusDTO,
    PeakHourDTO,
    TopSellingItemDTO,
    RestaurantOrderStatsDTO,
    MenuItemOrderStatsDTO,
)


class OrderAdapter:
    def __init__(self):
        self.interface = ServiceInterface()

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

    def get_user_restaurants_stat(
        self, restaurant_ids: List[str], user_id: str
    ) -> List[RestaurantOrderStatsDTO]:

        return self.interface.get_user_restaurants_stat(
            restaurant_ids=restaurant_ids, user_id=user_id
        )

    def get_menu_item_order_stats(
        self, menu_item_ids: List[str], user_id: str
    ) -> List[MenuItemOrderStatsDTO]:

        return self.interface.get_menu_item_order_stats(
            menu_item_ids=menu_item_ids, user_id=user_id
        )
