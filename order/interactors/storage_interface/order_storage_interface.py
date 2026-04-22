from abc import ABC, abstractmethod
from typing import List

from order.interactors.dtos import CreateOrderDTO, OrderDTO, CreateOrderItemDTO


class OrderStorageInterface(ABC):
    @abstractmethod
    def get_order(self, order_id: str):
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
