from restaurant.exception.custom_exceptions import (
    InvalidCuisineTypeException,
    InvalidMinRatingException,
)
from restaurant.graphql.types.error_types import (
    InvalidCuisineTypeExceptionType,
    InvalidMinRatingExceptionType,
)
from restaurant.graphql.types.types import BrowseRestaurantType, BrowseRestaurantsType
from restaurant.interactors.dtos import BrowseRestaurantFiltersDTO
from restaurant.interactors.restaurant.browse_restaurants import (
    BrowseRestaurantsInteractor,
)
from restaurant.storages.restaurant_storage import RestaurantStorage
from restaurant.storages.restaurant_timing_storage import RestaurantTimingStorage


def _build_filters_dto(params) -> BrowseRestaurantFiltersDTO:
    return BrowseRestaurantFiltersDTO(
        cuisine_type=getattr(params, "cuisine_type", None),
        is_veg_only=getattr(params, "is_veg_only", None),
        pincode=getattr(params, "pincode", None),
        min_rating=getattr(params, "min_rating", None),
        search=getattr(params, "search", None),
        limit=getattr(params, "limit", 10) or 10,
        offset=getattr(params, "offset", 0) or 0,
    )


def _map_browse_restaurants_response(restaurants):
    response = [
        BrowseRestaurantType(
            restaurant_id=str(each.restaurant_id),
            name=each.name,
            description=each.description,
            cuisine_type=(
                each.cuisine_type.value
                if hasattr(each.cuisine_type, "value")
                else str(each.cuisine_type)
            ),
            address=each.address,
            pin_code=each.pin_code,
            is_veg_only=each.is_veg_only,
            is_active=each.is_active,
            average_rating=float(each.average_rating),
            total_reviews=each.total_reviews,
            is_open=each.is_open,
        )
        for each in restaurants
    ]
    return BrowseRestaurantsType(restaurants=response)


def resolve_browse_restaurants(root, info, params=None):
    filters_dto = _build_filters_dto(params=params)

    interactor = BrowseRestaurantsInteractor(
        restaurant_storage=RestaurantStorage(),
        restaurant_timing_storage=RestaurantTimingStorage(),
    )

    try:
        restaurants = interactor.browse_restaurants(filters_dto=filters_dto)
        return _map_browse_restaurants_response(restaurants=restaurants)
    except InvalidCuisineTypeException as exc:
        return InvalidCuisineTypeExceptionType(cuisine_type=str(exc.cuisine_type))
    except InvalidMinRatingException as exc:
        return InvalidMinRatingExceptionType(min_rating=exc.min_rating)
