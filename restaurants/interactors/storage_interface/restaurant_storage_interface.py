from abc import ABC, abstractmethod
from typing import List

from restaurants.interactors.dtos import (
    CreateRestaurantDTO,
    CreateMenuItemDTO,
    MenuItemDTO,
    BrowseRestaurantFiltersDTO,
    MenuItemWithTagsDTO,
    RestaurantDTO,
    UpdateMenuItemDTO,
    UpdateRestaurantDTO,
)


class RestaurantStorageInterface(ABC):
    @abstractmethod
    def get_existing_restaurants(self, names: List[str]) -> List[str]:
        pass

    @abstractmethod
    def get_existing_restaurant_dtos(self, names: List[str]) -> List[RestaurantDTO]:
        pass

    @abstractmethod
    def create_bulk_restaurants(
        self, restaurant_dtos: List[CreateRestaurantDTO]
    ) -> List:
        pass

    @abstractmethod
    def update_bulk_restaurants(
        self, restaurant_dtos: List[UpdateRestaurantDTO]
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

    @abstractmethod
    def update_menu_item(self, update_menu_item_dto: UpdateMenuItemDTO) -> MenuItemDTO:
        pass

    @abstractmethod
    def delete_menu_item(self, menu_item_id: str):
        pass

    @abstractmethod
    def get_unavailable_menu_items(self, menu_item_ids: List[str]) -> List[str]:
        pass

    @abstractmethod
    def get_owner_restaurants(self, owner_id: str) -> List[RestaurantDTO]:
        pass

    @abstractmethod
    def get_delivered_pincode_restaurants(self, pincode: str) -> List[RestaurantDTO]:
        pass
