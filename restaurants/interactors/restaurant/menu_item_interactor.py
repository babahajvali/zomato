from typing import List

from restaurants.interactors.dtos import (
    CreateMenuItemDTO,
    MenuItemDTO,
    UpdateMenuItemDTO,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.mixins.restaurant_mixin import RestaurantMixin


class MenuItemInteractor(RestaurantMixin):
    def __init__(self, restaurant_storage: RestaurantStorageInterface):
        super().__init__(restaurant_storage=restaurant_storage)
        self.restaurant_storage = restaurant_storage

    def create_menu_item(
        self,
        create_items_dto: List[CreateMenuItemDTO],
        user_id: str,
        restaurant_id: str,
    ) -> List[MenuItemDTO]:

        self.validate_restaurant_exists(restaurant_id=restaurant_id)
        self.validate_user_is_restaurant_owner(
            user_id=user_id, restaurant_id=restaurant_id
        )

        categories = [each.category.value for each in create_items_dto]

        self.validate_categories(categories=categories)

        return self.restaurant_storage.create_menu_items(
            create_item_dtos=create_items_dto, restaurant_id=restaurant_id
        )

    def update_menu_item(
        self, update_menu_item_dto: UpdateMenuItemDTO, user_id: str
    ) -> MenuItemDTO:

        self.validate_menu_item_exists(menu_item_id=update_menu_item_dto.menu_item_id)
        menu_item_dto = self.restaurant_storage.get_menu_item(
            menu_item_id=update_menu_item_dto.menu_item_id
        )

        self.validate_user_is_restaurant_owner(
            user_id=user_id, restaurant_id=menu_item_dto.restaurant_id
        )

        return self.restaurant_storage.update_menu_item(
            update_menu_item_dto=update_menu_item_dto
        )

    def delete_menu_item(self, menu_item_id: str, user_id: str):

        self.validate_menu_item_exists(menu_item_id=menu_item_id)
        menu_item_dto = self.restaurant_storage.get_menu_item(menu_item_id=menu_item_id)

        self.validate_user_is_restaurant_owner(
            user_id=user_id, restaurant_id=menu_item_dto.restaurant_id
        )

        return self.restaurant_storage.delete_menu_item(menu_item_id=menu_item_id)

    def get_unavailable_items(self, menu_item_ids: List[str]) -> List[str]:

        return self.restaurant_storage.get_unavailable_menu_items(
            menu_item_ids=menu_item_ids
        )
