
from typing import List

from restaurant.interactors.dtos import RestaurantMenuDTO, CategoryMenuDTO, \
    MenuItemWithTagsDTO
from restaurant.interactors.storage_interface.restaurant_storage_interface import \
    RestaurantStorageInterface
from restaurant.mixins.restaurant_mixin import RestaurantMixin


class ViewRestaurantMenuInteractor(RestaurantMixin):

    def __init__(self, restaurant_storage: RestaurantStorageInterface):
        super().__init__(restaurant_storage=restaurant_storage)
        self.restaurant_storage = restaurant_storage

    def view_restaurant_menu(
            self,
            restaurant_id: str,
    ) -> RestaurantMenuDTO:

        self.check_restaurant_is_exists(
            restaurant_id=restaurant_id
        )

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
            items: List[MenuItemWithTagsDTO]) -> List[CategoryMenuDTO]:

        category_map = {}

        for item in items:
            category = item.category

            if category not in category_map:
                category_map[category] = []

            category_map[category].append(item)


        return [
            CategoryMenuDTO(category=category, items=items)
            for category, items in category_map.items()
        ]