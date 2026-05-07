from collections import defaultdict
from typing import List

from restaurants.interactors.dtos import (
    RestaurantMenuDTO,
    CategoryMenuDTO,
    MenuItemWithTagsDTO,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.mixins.restaurant_mixin import RestaurantMixin
from utils.caching_decorators import interactor_cache


class ViewRestaurantMenuInteractor(RestaurantMixin):
    def __init__(self, restaurant_storage: RestaurantStorageInterface):
        super().__init__(restaurant_storage=restaurant_storage)
        self.restaurant_storage = restaurant_storage

    @interactor_cache(cache_name="menu_items")
    def view_restaurant_menu(self, restaurant_id: str) -> RestaurantMenuDTO:

        self.validate_restaurant_exists(restaurant_id=restaurant_id)

        items = self.restaurant_storage.get_available_menu_items_by_restaurant(
            restaurant_id=restaurant_id
        )

        categories = self.group_menu_items_by_category(items=items)

        return RestaurantMenuDTO(
            restaurant_id=restaurant_id,
            categories=categories,
        )

    @staticmethod
    def group_menu_items_by_category(
        items: List[MenuItemWithTagsDTO],
    ) -> List[CategoryMenuDTO]:

        category_map = defaultdict(list)

        for item in items:
            category = item.category

            category_map[category].append(item)

        return [
            CategoryMenuDTO(category=category, items=menu_items)
            for category, menu_items in category_map.items()
        ]
