from typing import List

from restaurant.constants.enums import Category
from restaurant.exception.custom_exceptions import (
    UserIsNotRestaurantOwner,
    InvalidCategoriesFound,
    RestaurantNotFound,
    InvalidMinRatingException,
    MenuItemNotFound,
)
from restaurant.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)


class RestaurantMixin:
    def __init__(self, restaurant_storage: RestaurantStorageInterface, **kwargs):
        self.restaurant_storage = restaurant_storage
        super().__init__(**kwargs)

    def validate_user_is_restaurant_owner(self, user_id: str, restaurant_id: str):

        owner_id = self.restaurant_storage.get_restaurant_owner_id(
            restaurant_id=restaurant_id
        )

        if str(owner_id) != user_id:
            raise UserIsNotRestaurantOwner(user_id=user_id)

    @staticmethod
    def validate_categories(categories: List[str]):

        existed_categories = Category.get_values()
        invalid_categories = []
        for category in categories:
            if category not in existed_categories:
                invalid_categories.append(category)

        if invalid_categories:
            raise InvalidCategoriesFound(categories=invalid_categories)

    def validate_restaurant_is_exists(self, restaurant_id: str):

        is_restaurant_exists = self.restaurant_storage.check_restaurant_is_exist(
            restaurant_id=restaurant_id
        )

        if not is_restaurant_exists:
            raise RestaurantNotFound(restaurant_id=restaurant_id)

    @staticmethod
    def validate_min_rating(min_rating: float):
        if not (0.0 <= min_rating <= 5.0):
            raise InvalidMinRatingException(min_rating=min_rating)

    def validate_menu_item_exists(self, menu_item_id: str):

        menu_item_dto = self.restaurant_storage.get_menu_item(menu_item_id=menu_item_id)

        if not menu_item_dto:
            raise MenuItemNotFound(menu_item_id=menu_item_id)
