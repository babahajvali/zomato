from restaurant.exception import custom_exceptions

from restaurant.graphql.types.error_types import (
    InvalidCuisineTypeException,
    InvalidMinRatingException,
)
from restaurant.graphql.types.types import BrowseRestaurantType, BrowseRestaurantsType
from restaurant.interactors.dtos import BrowseRestaurantFiltersDTO
from restaurant.interactors.restaurant.browse_restaurants import (
    BrowseRestaurantsInteractor,
)
from restaurant.storages.restaurant_storage import RestaurantStorage
from restaurant.storages.restaurant_timing_storage import RestaurantTimingStorage


def _map_browse_restaurants_response(restaurants):
    response = [
        BrowseRestaurantType(
            restaurant_id=str(each.restaurant_id),
            name=each.name,
            description=each.description,
            cuisine_type=each.cuisine_type,
            address=each.address,
            pin_code=each.pin_code,
            is_veg_only=each.is_veg_only,
            is_deleted=each.is_deleted,
            average_rating=float(each.average_rating),
            total_reviews=each.total_reviews,
            is_open=each.is_open,
        )
        for each in restaurants
    ]
    return BrowseRestaurantsType(restaurants=response)


def get_browse_restaurants_resolver(root, info, params=None):
    filters_dto = BrowseRestaurantFiltersDTO(
        cuisine_type=params.cuisine_type if params.cuisine_type else None,
        is_veg_only=params.is_veg_only,
        pincode=params.pincode if params.pincode else None,
        min_rating=params.min_rating,
        search=params.search if params.search else None,
        limit=params.limit,
        offset=params.offset,
    )

    interactor = BrowseRestaurantsInteractor(
        restaurant_storage=RestaurantStorage(),
        restaurant_timing_storage=RestaurantTimingStorage(),
    )

    try:
        restaurants = interactor.browse_restaurants(filters_dto=filters_dto)
        return _map_browse_restaurants_response(restaurants=restaurants)
    except custom_exceptions.InvalidCuisineTypeException as exc:
        return InvalidCuisineTypeException(cuisine_type=str(exc.cuisine_type))
    except custom_exceptions.InvalidMinRating as exc:
        return InvalidMinRatingException(min_rating=exc.min_rating)
