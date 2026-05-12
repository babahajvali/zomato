from datetime import date
from typing import List

from orders.app_service.dtos import (
    RestaurantOrdersSummaryDTO,
    OrdersByStatusDTO,
    RestaurantOrderStatsDTO,
    MenuItemOrderStatsDTO,
)
from orders.interactors.dtos import PeakHourDTO, TopSellingItemDTO
from orders.interactors.order.order_interactor import OrderInteractor
from orders.storages.order_storage import OrderStorage


class ServiceInterface:
    def __init__(self):
        self.order_storage = OrderStorage()

    def get_restaurant_orders_summary(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> RestaurantOrdersSummaryDTO:
        interactor = OrderInteractor(order_storage=self.order_storage)

        return interactor.get_restaurant_orders_summary(
            restaurant_id=restaurant_id, date_from=date_from, date_to=date_to
        )

    def get_orders_count_by_status(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> List[OrdersByStatusDTO]:
        interactor = OrderInteractor(order_storage=self.order_storage)

        return interactor.get_orders_count_by_status(
            restaurant_id=restaurant_id, date_from=date_from, date_to=date_to
        )

    def get_peak_hours(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> List[PeakHourDTO]:

        interactor = OrderInteractor(order_storage=self.order_storage)

        return interactor.get_peak_hours(
            restaurant_id=restaurant_id, date_from=date_from, date_to=date_to
        )

    def get_top_selling_items(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> List[TopSellingItemDTO]:

        interactor = OrderInteractor(order_storage=self.order_storage)

        return interactor.get_top_selling_items(
            restaurant_id=restaurant_id, date_from=date_from, date_to=date_to
        )

    def get_user_restaurants_stat(
        self, restaurant_ids: List[str], user_id: str
    ) -> List[RestaurantOrderStatsDTO]:

        interactor = OrderInteractor(order_storage=self.order_storage)

        return interactor.get_user_restaurants_stats(
            restaurant_ids=restaurant_ids, user_id=user_id
        )

    def get_menu_item_order_stats(
        self, menu_item_ids: List[str], user_id: str
    ) -> List[MenuItemOrderStatsDTO]:

        interactor = OrderInteractor(order_storage=self.order_storage)

        return interactor.get_menu_item_order_stats(
            menu_item_ids=menu_item_ids, user_id=user_id
        )
