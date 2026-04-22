from typing import List

from restaurant.interactors.dtos import CreateMenuItemDTO, MenuItemDTO
from restaurant.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurant.mixins.restaurant_mixin import RestaurantMixin


class CreateMenuItemInteractor(RestaurantMixin):
    def __init__(self, restaurant_storage: RestaurantStorageInterface):
        super().__init__(restaurant_storage=restaurant_storage)
        self.restaurant_storage = restaurant_storage

    def create_menu_item(
        self,
        create_items_dto: List[CreateMenuItemDTO],
        user_id: str,
        restaurant_id: str,
    ) -> List[MenuItemDTO]:
        self.validate_restaurant_is_exists(restaurant_id=restaurant_id)
        self.validate_user_is_restaurant_owner(
            user_id=user_id, restaurant_id=restaurant_id
        )

        categories = [each.category.value for each in create_items_dto]

        self.validate_categories(categories=categories)

        return self.restaurant_storage.create_menu_items(
            create_item_dtos=create_items_dto, restaurant_id=restaurant_id
        )
