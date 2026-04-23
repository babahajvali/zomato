from enum import Enum


class CuisineType(Enum):
    SOUTH_INDIAN = "SOUTH_INDIAN"
    NORTH_INDIAN = "NORTH_INDIAN"
    CHINESE = "CHINESE"
    ITALIAN = "ITALIAN"
    FAST_FOOD = "FAST_FOOD"
    BAKERY = "BAKERY"
    CAFE = "CAFE"

    @classmethod
    def get_list_of_tuples(cls):
        return [(member.value, member.value.capitalize()) for member in cls]


class Category(Enum):
    STARTER = "STARTER"
    MAIN_COURSE = "MAIN_COURSE"
    BREADS = "BREADS"
    RICE_AND_BIRYANI = "RICE_AND_BIRYANI"
    BEVERAGES = "BEVERAGES"
    DESSERTS = "DESSERTS"
    SOUPS = "SOUPS"
    SALADS = "SALADS"
    COMBO = "COMBO"

    @classmethod
    def get_list_of_tuples(cls):
        return [(member.value, member.value.capitalize()) for member in cls]

    @classmethod
    def get_values(cls):
        return [member.value for member in cls]
