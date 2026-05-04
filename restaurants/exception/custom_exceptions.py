import datetime
from typing import List


class RestaurantAlreadyExists(Exception):
    def __init__(self, names: List[str]):
        self.names = names

    def __str__(self):
        return str(self.names)


class DuplicateRestaurants(Exception):
    def __init__(self, names: List[str]):
        self.names = names

    def __str__(self):
        return str(self.names)


class InvalidTimingRange(Exception):
    def __init__(self, open_time: datetime.time, close_time: datetime.time):
        self.open_time = open_time
        self.close_time = close_time

    def __str__(self):
        return f"{self.open_time} --> {self.close_time}"


class RestaurantTimingNotFound(Exception):
    def __init__(self, id: int):
        self.id = id


class UserNotRestaurantOwner(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id

    def __str__(self):
        return str(self.user_id)


class InvalidCategories(Exception):
    def __init__(self, categories: List[str]):
        self.categories = categories

    def __str__(self):
        return str(self.categories)


class RestaurantNotFound(Exception):
    def __init__(self, restaurant_id: str):
        self.restaurant_id = restaurant_id

    def __str__(self):
        return str(self.restaurant_id)


class InvalidRestaurantIds(Exception):
    def __init__(self, restaurant_ids: List[str]):
        self.restaurant_ids = restaurant_ids

    def __str__(self):
        return str(self.restaurant_ids)


class DuplicateRestaurantTimings(Exception):
    def __init__(self, restaurant_ids: List[str]):
        self.restaurant_ids = restaurant_ids

    def __str__(self):
        return str(self.restaurant_ids)


class InvalidCuisineType(Exception):
    def __init__(self, cuisine_type: str):
        self.cuisine_type = cuisine_type

    def __str__(self):
        return str(self.cuisine_type)


class InvalidMinRating(Exception):
    def __init__(self, min_rating: float):
        self.min_rating = min_rating

    def __str__(self):
        return str(self.min_rating)


class CartNotFound(Exception):
    def __init__(self, cart_id: str):
        self.cart_id = cart_id

    def __str__(self):
        return f"{self.cart_id} cart not found"


class MenuItemNotFound(Exception):
    def __init__(self, menu_item_id: str):
        self.menu_item_id = menu_item_id

    def __str__(self):
        return f"{self.menu_item_id} menu item not found"


class InvalidQuantity(Exception):
    def __init__(self, quantity: int):
        self.quantity = quantity

    def __str__(self):
        return f"Invalid quantity: {self.quantity}"


class CartItemNotFound(Exception):
    def __init__(self, cart_item_id: int):
        self.cart_item_id = cart_item_id

    def __str__(self):
        return f"{self.cart_item_id} cart item not found"


class DuplicateDeliveryZones(Exception):
    def __init__(self, combinations):
        self.combinations = combinations
        self.message = self._build_message(combinations)

    @staticmethod
    def _build_message(combinations):
        formatted = [
            f"(restaurant_id={restaurant_id}, pin_code={pin_code})"
            for restaurant_id, pin_code in combinations
        ]
        return f"Duplicate delivery zones found for: {', '.join(formatted)}"

    def __str__(self):
        return self.message


class RestaurantAlreadyReviewedByUser(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id

    def __str__(self):
        return f"{self.user_id} user already reviewed"


class InvalidRating(Exception):
    def __init__(self, rating: int):
        self.rating = rating

    def __str__(self):
        return f" Invalid rating: {self.rating} found "


class InvalidDateRange(Exception):
    def __init__(self, date_from: datetime.date, date_to: datetime.date):
        self.date_from = date_from
        self.date_to = date_to

    def __str__(self):
        return f"{self.date_from} --> {self.date_to}"


class NothingToUpdate(Exception):
    def __str__(self):
        return "Nothing to update"
