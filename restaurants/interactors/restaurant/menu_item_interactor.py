from typing import List

from restaurants.exception.custom_exceptions import NothingToUpdate
from restaurants.interactors.dtos import (
    CreateMenuItemDTO,
    MenuItemDTO,
    UpdateMenuItemDTO,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.mixins.restaurant_mixin import RestaurantMixin
from utils.caching_decorators import invalidate_interactor_cache


class MenuItemInteractor(RestaurantMixin):
    def __init__(self, restaurant_storage: RestaurantStorageInterface):
        self.restaurant_storage = restaurant_storage

    @invalidate_interactor_cache(cache_name="menu_items")
    def create_menu_item(
        self,
        create_items_dto: List[CreateMenuItemDTO],
        user_id: str,
        restaurant_id: str,
    ) -> List[MenuItemDTO]:

        self.validate_restaurant_exists(
            restaurant_id=restaurant_id, restaurant_storage=self.restaurant_storage
        )
        self.validate_user_is_restaurant_owner(
            user_id=user_id,
            restaurant_id=restaurant_id,
            restaurant_storage=self.restaurant_storage,
        )

        categories = [each.category.value for each in create_items_dto]

        self.validate_categories(categories=categories)

        return self.restaurant_storage.create_menu_items(
            create_item_dtos=create_items_dto, restaurant_id=restaurant_id
        )

    @invalidate_interactor_cache(cache_name="menu_items")
    def update_menu_item(
        self, update_menu_item_dto: UpdateMenuItemDTO, user_id: str
    ) -> MenuItemDTO:

        menu_item_dto = self.validate_menu_item_exists(
            menu_item_id=update_menu_item_dto.menu_item_id,
            restaurant_storage=self.restaurant_storage,
        )

        self.validate_user_is_restaurant_owner(
            user_id=user_id,
            restaurant_id=menu_item_dto.restaurant_id,
            restaurant_storage=self.restaurant_storage,
        )
        self._validate_menu_item_update_properties(
            update_menu_item_dto=update_menu_item_dto
        )

        return self.restaurant_storage.update_menu_item(
            update_menu_item_dto=update_menu_item_dto
        )

    @invalidate_interactor_cache(cache_name="menu_items")
    def delete_menu_item(self, menu_item_id: str, user_id: str):

        menu_item_dto = self.validate_menu_item_exists(
            menu_item_id=menu_item_id, restaurant_storage=self.restaurant_storage
        )

        self.validate_user_is_restaurant_owner(
            user_id=user_id,
            restaurant_id=menu_item_dto.restaurant_id,
            restaurant_storage=self.restaurant_storage,
        )

        return self.restaurant_storage.delete_menu_item(menu_item_id=menu_item_id)

    def get_unavailable_items(self, menu_item_ids: List[str]) -> List[str]:

        return self.restaurant_storage.get_unavailable_menu_items(
            menu_item_ids=menu_item_ids
        )

    def import_menu_items(self, create_item_dtos: List[CreateMenuItemDTO]) -> str:
        restaurant_ids = list({item.restaurant_id for item in create_item_dtos})
        for restaurant_id in restaurant_ids:
            self.validate_restaurant_exists(
                restaurant_id=restaurant_id, restaurant_storage=self.restaurant_storage
            )

        categories = [item.category.value for item in create_item_dtos]
        self.validate_categories(categories=categories)

        created_items = self.restaurant_storage.create_menu_items(
            create_item_dtos, restaurant_id=restaurant_ids[0]
        )

        return f"{len(created_items)} menu items created, 0 menu items updated"

    @staticmethod
    def _validate_menu_item_update_properties(update_menu_item_dto: UpdateMenuItemDTO):

        is_empty_updates = all(
            [
                update_menu_item_dto.name is None,
                update_menu_item_dto.price is None,
                update_menu_item_dto.tags is None,
                update_menu_item_dto.is_available is None,
                update_menu_item_dto.preparation_time_in_minutes is None,
                update_menu_item_dto.description is None,
            ]
        )

        if is_empty_updates:
            raise NothingToUpdate()
