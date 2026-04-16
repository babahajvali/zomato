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