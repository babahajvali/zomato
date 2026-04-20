from abc import ABC, abstractmethod
from typing import List

from restaurant.interactors.dtos import UpdateRestaurantTimingDTO, \
    CreateRestaurantTimingDTO, RestaurantTimingDTO


class RestaurantTimingStorageInterface(ABC):

    @abstractmethod
    def create_bulk_restaurant_timing(
            self, create_restaurant_timing_dto: List[CreateRestaurantTimingDTO]):
        pass

    @abstractmethod
    def update_restaurant_timing(
            self, update_restaurant_timing_dto: UpdateRestaurantTimingDTO):
        pass

    @abstractmethod
    def get_restaurant_timing(self, id: int) -> RestaurantTimingDTO | None:
        pass

    @abstractmethod
    def get_restaurant_owner_id(self, id: int) -> str | None:
        pass

    @abstractmethod
    def get_operating_hours_for_restaurants(
            self, restaurant_ids: List[str]) -> List[RestaurantTimingDTO]:
        pass

    @abstractmethod
    def delete_restaurant_timing(self, id: int):
        pass

    @abstractmethod
    def get_restaurant_timings(
            self, restaurant_id: str) -> List[RestaurantTimingDTO]:
        pass

