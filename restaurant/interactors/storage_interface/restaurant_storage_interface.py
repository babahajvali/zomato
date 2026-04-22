from abc import ABC, abstractmethod
from typing import List

from restaurant.interactors.dtos import (
    CreateRestaurantDTO,
    CreateMenuItemDTO,
    MenuItemDTO,
    BrowseRestaurantFiltersDTO,
    MenuItemWithTagsDTO,
    RestaurantDTO,
)


class RestaurantStorageInterface(ABC):
    @abstractmethod
    def get_existing_restaurants(self, names: List[str]) -> List[str]:
        pass

    @abstractmethod
    def create_bulk_restaurants(
        self, restaurant_dtos: List[CreateRestaurantDTO]
    ) -> List:
        pass

    @abstractmethod
    def create_menu_items(
        self, create_item_dtos: List[CreateMenuItemDTO], restaurant_id: str
    ) -> List[MenuItemDTO]:
        pass

    @abstractmethod
    def get_restaurant_owner_id(self, restaurant_id: str) -> str:
        pass

    @abstractmethod
    def check_restaurant_is_exist(self, restaurant_id: str) -> bool:
        pass

    @abstractmethod
    def get_restaurants(
        self, filters_dto: BrowseRestaurantFiltersDTO
    ) -> List[RestaurantDTO]:
        pass

    @abstractmethod
    def get_available_menu_items_by_restaurant(
        self, restaurant_id: str
    ) -> List[MenuItemWithTagsDTO]:
        pass

    @abstractmethod
    def get_restaurants_by_ids(self, restaurant_ids: List[str]) -> List[str]:
        pass

    @abstractmethod
    def get_menu_item(self, menu_item_id: str) -> MenuItemDTO:
        pass
