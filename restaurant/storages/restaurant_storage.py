from typing import List

from account.models import User
from restaurant.Interactors.storage_interface.restaurant_storage_interface import RestaurantStorageInterface
from restaurant.Interactors.dtos import CreateRestaurantDTO
from restaurant.exception.custom_exceptions import OwnerNotFound
from restaurant.models.restaurant import Restaurant


class RestaurantStorage(RestaurantStorageInterface):

    def create_bulk_restaurants(self, restaurants_dto: List[CreateRestaurantDTO]):
        restaurants = []
        
        for dto in restaurants_dto:
            try:
                owner = User.objects.get(
                    email=dto.owner_email,
                    role='OWNER'
                )
            except User.DoesNotExist:
                raise OwnerNotFound(email=dto.owner_email)
            
            restaurant = Restaurant(
                name=dto.name,
                owner=owner,
                description=dto.description,
                cuisine_type=dto.cuisine_type,
                address=dto.address,
                pin_code=dto.pin_code,
                is_veg_only=dto.is_veg_only,
                is_active=dto.is_active
            )
            restaurants.append(restaurant)

        created_restaurants = Restaurant.objects.bulk_create(restaurants)

        return created_restaurants

    def get_existing_restaurants(self, names: List[str]) -> List[str]:
        return list(Restaurant.objects.filter(name__in=names)
                    .values_list('name', flat=True))
