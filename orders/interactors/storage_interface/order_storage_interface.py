from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from orders.app_service.dtos import RestaurantOrdersSummaryDTO
from orders.constants.enums import OrderStatus
from orders.interactors.dtos import (
    CreateOrderDTO,
    OrderDTO,
    CreateOrderItemDTO,
    OrderItemSummaryDTO,
)


class OrderStorageInterface(ABC):
    @abstractmethod
    def get_order(self, order_id: str) -> OrderDTO:
        pass

    @abstractmethod
    def get_order_items(self, order_id: str) -> List[OrderItemSummaryDTO]:
        pass

    @abstractmethod
    def get_promo_code_usage(self, promo_code_id: int) -> int:
        pass

    @abstractmethod
    def create_order(self, create_order_dto: CreateOrderDTO) -> OrderDTO:
        pass

    @abstractmethod
    def create_order_items(self, order_item_dtos: List[CreateOrderItemDTO]):
        pass

    @abstractmethod
    def update_order_status(self, order_id: str, status: OrderStatus) -> OrderDTO:
        pass

    @abstractmethod
    def get_user_orders(self, user_id: str, limit: int, offset: int) -> List[OrderDTO]:
        pass

    @abstractmethod
    def get_order_placed_at(self, order_id: str) -> datetime:
        pass

    @abstractmethod
    def get_restaurant_orders(
        self, restaurant_id: str, limit: int, offset: int
    ) -> List[OrderDTO]:
        pass

    @abstractmethod
    def get_today_restaurant_orders(
        self, restaurant_id: str, limit: int, offset: int
    ) -> List[OrderDTO]:
        pass

    @abstractmethod
    def get_restaurant_orders_summary(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> RestaurantOrdersSummaryDTO:
        pass

    @abstractmethod
    def get_orders_count_by_status(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> List[OrdersByStatusDTO]:
        pass
