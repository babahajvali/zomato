from restaurants.exception import custom_exceptions
from restaurants.graphql.types.error_types import InvalidLimit, InvalidOffset
from restaurants.graphql.types.types import ScoredRestaurantType, ScoredRestaurantsType
from restaurants.interactors.restaurant.get_scored_restaurant_interactor import (
    GetScoredRestaurantInteractor,
)
from restaurants.storages.restaurant_storage import RestaurantStorage
from restaurants.storages.review_storage import ReviewStorage


def get_user_recommended_restaurant_resolver(root, info, params):
    restaurant_storage = RestaurantStorage()
    review_storage = ReviewStorage()

    interactor = GetScoredRestaurantInteractor(
        restaurant_storage=restaurant_storage,
        review_storage=review_storage,
    )

    try:
        result = interactor.get_scored_restaurant(
            pincode=params.pincode,
            limit=params.limit,
            offset=params.offset,
            user_id=info.context.user_id,
        )

        restaurants = [
            ScoredRestaurantType(
                restaurant_id=each.restaurant_id,
                name=each.name,
                cuisine_type=each.cuisine_type,
                average_rating=each.average_rating,
                total_reviews=each.total_reviews,
                score=each.score,
                is_open=each.is_open,
                day_frequent=each.day_frequent,
                order_volume=each.order_volume,
            )
            for each in result
        ]

        return ScoredRestaurantsType(restaurants=restaurants)

    except custom_exceptions.InvalidLimitFound as e:
        return InvalidLimit(limit=e.limit)
    except custom_exceptions.InvalidOffsetFound as e:
        return InvalidOffset(offset=e.offset)
