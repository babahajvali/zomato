from typing import List


class AlreadyExistsRestaurant(Exception):
    def __init__(self, names):
        self.names = names

    def __str__(self):
        return str(self.names)


class DuplicateRestaurants(Exception):
    def __init__(self, names):
        self.names = names

    def __str__(self):
        return str(self.names)


class OwnerNotFound(Exception):
    def __init__(self, email):
        self.email = email

    def __str__(self):
        return str(self.email)


class OpenTimeGreaterThanCloseTime(Exception):
    def __init__(self, open_time, close_time):
        self.open_time = open_time
        self.close_time = close_time

    def __str__(self):
        return f"{self.open_time} --> {self.close_time}"


class RestaurantTimingNotFound(Exception):
    def __init__(self, id: int):
        self.id = id


class UserIsNotRestaurantOwner(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id

    def __str__(self):
        return str(self.user_id)


class InvalidCategoriesFound(Exception):
    def __init__(self, categories: List[str]):
        self.categories = categories

    def __str__(self):
        return str(self.categories)


class RestaurantNotFound(Exception):
    def __init__(self, restaurant_id: str):
        self.restaurant_id = restaurant_id

    def __str__(self):
        return str(self.restaurant_id)


class InvalidRestaurantIdsFound(Exception):
    def __init__(self, restaurant_ids: List[str]):
        self.restaurant_ids = restaurant_ids

    def __str__(self):
        return str(self.restaurant_ids)

class DuplicateRestaurantTimings(Exception):
    def __init__(self, restaurant_ids: List[str]):
        self.restaurant_ids = restaurant_ids

    def __str__(self):
        return str(self.restaurant_ids)


class InvalidCuisineTypeException(Exception):
    def __init__(self, cuisine_type: str):
        self.cuisine_type = cuisine_type

    def __str__(self):
        return str(self.cuisine_type)


class InvalidMinRatingException(Exception):
    def __init__(self, min_rating: float):
        self.min_rating = min_rating

    def __str__(self):
        return str(self.min_rating)
