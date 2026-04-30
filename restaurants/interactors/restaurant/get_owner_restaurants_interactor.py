from typing import List

from restaurants.interactors.dtos import RestaurantDTO
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)


class GetOwnerRestaurantsInteractor:
    def __init__(self, restaurant_storage: RestaurantStorageInterface):
        self.restaurant_storage = restaurant_storage

    def get_owner_restaurants(self, owner_id: str) -> List[RestaurantDTO]:
        restaurants = self.restaurant_storage.get_owner_restaurants(owner_id=owner_id)

        return [
            RestaurantDTO(
                id=restaurant.id,
                name=restaurant.name,
                description=restaurant.description,
                cuisine_type=restaurant.cuisine_type,
                address=restaurant.address,
                pin_code=restaurant.pin_code,
                is_veg_only=restaurant.is_veg_only,
                is_deleted=restaurant.is_deleted,
                owner_id=owner_id,
            )
            for restaurant in restaurants
        ]
