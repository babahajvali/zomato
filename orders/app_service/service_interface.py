from datetime import date
from typing import List

from orders.app_service.dtos import RestaurantOrdersSummaryDTO, OrdersByStatusDTO
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
