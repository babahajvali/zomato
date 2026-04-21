from abc import ABC, abstractmethod
from typing import List

from restaurant.interactors.dtos import CartDTO, CartItemDTO


class CartStorageInterface(ABC):
    @abstractmethod
    def create_carts(self, customer_ids: list[str]) -> List[CartDTO]:
        pass

    @abstractmethod
    def get_cart(self, cart_id: str) -> CartDTO:
        pass

    @abstractmethod
    def create_or_update_cart_item(
        self, cart_id: str, menu_item_id: str, quantity: int, item_price=float
    ) -> CartItemDTO:
        pass

    @abstractmethod
    def get_cart_item_by_id(self, cart_item_id: int) -> CartItemDTO:
        pass

    @abstractmethod
    def remove_cart_item(self, cart_item_id: int):
        pass

    @abstractmethod
    def clear_cart_items(self, cart_id: str):
        pass
