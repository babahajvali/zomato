from typing import List

from restaurant.constants.enums import Category, CuisineType
from restaurant.exception.custom_exceptions import UserIsNotRestaurantOwner, \
    InvalidCategoriesFound, RestaurantNotFound, InvalidCuisineTypeException, \
    InvalidMinRatingException
from restaurant.interactors.storage_interface.restaurant_storage_interface import \
    RestaurantStorageInterface


class RestaurantMixin:

    def __init__(self, restaurant_storage: RestaurantStorageInterface, **kwargs):
        self.restaurant_storage = restaurant_storage
        super().__init__(**kwargs)

    def check_user_is_restaurant_owner(
            self, user_id: str, restaurant_id: str):

        owner_id = self.restaurant_storage.get_restaurant_owner_id(
            restaurant_id=restaurant_id)

        # print(owner_id , user_id, str(owner_id)==user_id)

        if str(owner_id) != user_id:
            raise UserIsNotRestaurantOwner(user_id=user_id)

    @staticmethod
    def check_categories_are_valid(categories: List[str]):

        existed_categories = Category.get_categories()
        invalid_categories = []
        for category in categories:
            if category not in existed_categories:
                invalid_categories.append(category)

        if invalid_categories:
            raise InvalidCategoriesFound(categories=invalid_categories)

    def check_restaurant_is_exists(self, restaurant_id: str):

        is_restaurant_exists = self.restaurant_storage.check_restaurant_is_exist(
            restaurant_id=restaurant_id)

        if not is_restaurant_exists:
            raise RestaurantNotFound(restaurant_id=restaurant_id)

    @staticmethod
    def check_cuisine_type_is_valid(cuisine_type: str):
        valid_cuisines = [c.value for c in CuisineType]
        if cuisine_type not in valid_cuisines:
            raise InvalidCuisineTypeException(
                f"Invalid cuisine_type '{cuisine_type}'."
                f" Valid options: {valid_cuisines}"
            )

    @staticmethod
    def check_min_rating_is_valid(min_rating: float):
        if not (0.0 <= min_rating <= 5.0):
            raise InvalidMinRatingException(min_rating=min_rating)



