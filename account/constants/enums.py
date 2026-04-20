from enum import Enum


class Role(Enum):
    OWNER = "OWNER"
    CUSTOMER = "CUSTOMER"

    @classmethod
    def get_list_of_tuples(cls):
        return [(member.value, member.value.capitalize()) for member in cls]
    