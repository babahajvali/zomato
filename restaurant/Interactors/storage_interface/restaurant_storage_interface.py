from abc import ABC, abstractmethod
from typing import List

from restaurant.Interactors.dtos import CreateRestaurantDTO


class RestaurantStorageInterface(ABC):

    @abstractmethod
    def get_existing_restaurants(self, names: List[str]) -> List[str]:
        pass

    @abstractmethod
    def create_bulk_restaurants(self, restaurants_dto: List[CreateRestaurantDTO]) -> List:
        pass
