from enum import Enum


class PromoCodeType(Enum):
    PERCENTAGE = "PERCENTAGE"
    FLAT = "FLAT"

    @classmethod
    def get_list_of_tuples(cls):
        return [(member.value, member.value.capitalize()) for member in cls]


class OrderStatus(Enum):
    PLACED = "PLACED"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    OUT_OF_DELIVERY = "OUT_OF_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

    @classmethod
    def get_list_of_tuples(cls):
        return [(member.value, member.value.capitalize()) for member in cls]

    @classmethod
    def get_status(cls):
        return [member.value for member in cls]
