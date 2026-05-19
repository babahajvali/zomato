from typing import List

from restaurants.constants.enums import Category
from restaurants.exception.custom_exceptions import (
    UserNotRestaurantOwner,
    InvalidCategories,
    RestaurantNotFound,
    InvalidMinRating,
    MenuItemNotFound,
    InvalidLimitFound,
    InvalidOffsetFound,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)


class RestaurantMixin:
    @staticmethod
    def validate_user_is_restaurant_owner(
        user_id: str, restaurant_id: str, restaurant_storage: RestaurantStorageInterface
    ):

        owner_id = restaurant_storage.get_restaurant_owner_id(
            restaurant_id=restaurant_id
        )

        if str(owner_id) != user_id:
            raise UserNotRestaurantOwner(user_id=user_id)

    @staticmethod
    def validate_categories(categories: List[str]):

        existed_categories = Category.get_values()
        invalid_categories = []
        for category in categories:
            if category not in existed_categories:
                invalid_categories.append(category)

        if invalid_categories:
            raise InvalidCategories(categories=invalid_categories)

    @staticmethod
    def validate_restaurant_exists(
        restaurant_id: str, restaurant_storage: RestaurantStorageInterface
    ):

        is_restaurant_exists = restaurant_storage.check_restaurant_is_exist(
            restaurant_id=restaurant_id
        )

        if not is_restaurant_exists:
            raise RestaurantNotFound(restaurant_id=restaurant_id)

    @staticmethod
    def validate_min_rating(min_rating: float):
        if not (0.0 <= min_rating <= 5.0):
            raise InvalidMinRating(min_rating=min_rating)

    @staticmethod
    def validate_menu_item_exists(
        menu_item_id: str, restaurant_storage: RestaurantStorageInterface
    ):

        menu_item_dto = restaurant_storage.get_menu_item(menu_item_id=menu_item_id)

        if not menu_item_dto:
            raise MenuItemNotFound(menu_item_id=menu_item_id)

        return menu_item_dto

    @staticmethod
    def validate_limit_offset(limit: int, offset: int):

        if limit < 0:
            raise InvalidLimitFound(limit=limit)

        if offset < 0:
            raise InvalidOffsetFound(offset=offset)
