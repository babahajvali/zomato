from enum import Enum


class PromoCodeType(Enum):
    PERCENTAGE = "PERCENTAGE"
    FLAT = "FLAT"

    @classmethod
    def get_list_of_tuples(cls):
        return [(member.value, member.value.capitalize()) for member in cls]