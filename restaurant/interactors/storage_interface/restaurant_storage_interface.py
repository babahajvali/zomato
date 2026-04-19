from abc import ABC, abstractmethod
from typing import List

from restaurant.interactors.dtos import CreateRestaurantDTO, CreateMenuItemDTO, \
    MenuItemDTO, BrowseRestaurantDTO, BrowseRestaurantFiltersDTO, \
    MenuItemWithTagsDTO


class RestaurantStorageInterface(ABC):

    @abstractmethod
    def get_existing_restaurants(self, names: List[str]) -> List[str]:
        pass

    @abstractmethod
    def create_bulk_restaurants(self, restaurants_dto: List[
        CreateRestaurantDTO]) -> List:
        pass

    @abstractmethod
    def create_menu_items(
            self, create_items_dto: List[CreateMenuItemDTO]) -> List[
        MenuItemDTO]:
        pass

    @abstractmethod
    def get_restaurant_owner_id(self, restaurant_id: str) -> str:
        pass

    @abstractmethod
    def check_restaurant_is_exist(self, restaurant_id: str) -> bool:
        pass

    @abstractmethod
    def get_restaurants(self, filters_dto: BrowseRestaurantFiltersDTO) -> List[
        BrowseRestaurantDTO]:
        pass

    @abstractmethod
    def get_available_menu_items_by_restaurant(
            self, restaurant_id: str) -> List[MenuItemWithTagsDTO]:
        pass
