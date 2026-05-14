from utils.graphql_types import UnauthorizedFound
from restaurants.graphql.types.types import OwnerRestaurantType, OwnerRestaurantsType
from restaurants.interactors.restaurant.get_owner_restaurants_interactor import (
    GetOwnerRestaurantsInteractor,
)
from restaurants.storages.restaurant_storage import RestaurantStorage


def get_owner_restaurants_resolver(root, info):
    owner_id = info.context.user_id
    if owner_id is None:
        return UnauthorizedFound(user_id=owner_id)

    restaurant_storage = RestaurantStorage()
    interactor = GetOwnerRestaurantsInteractor(restaurant_storage=restaurant_storage)

    owner_restaurant_dtos = interactor.get_owner_restaurants(owner_id=owner_id)

    owner_restaurants = []
    for restaurant_dto in owner_restaurant_dtos:
        owner_restaurant = OwnerRestaurantType(
            restaurant_id=restaurant_dto.id,
            name=restaurant_dto.name,
            description=restaurant_dto.description,
            cuisine_type=restaurant_dto.cuisine_type,
            address=restaurant_dto.address,
            pin_code=restaurant_dto.pin_code,
            is_veg_only=restaurant_dto.is_veg_only,
            is_deleted=restaurant_dto.is_deleted,
            owner_id=restaurant_dto.owner_id,
        )
        owner_restaurants.append(owner_restaurant)

    return OwnerRestaurantsType(restaurants=owner_restaurants)
