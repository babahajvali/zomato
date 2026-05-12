from restaurants.exception import custom_exceptions
from restaurants.graphql.types.error_types import (
    InvalidLimit,
    InvalidOffset,
    RestaurantNotFound,
)
from restaurants.graphql.types.types import ScoreItemType, ScoredItemsType
from restaurants.interactors.restaurant.get_scored_items_interactor import (
    GetScoredItemsInteractor,
)
from restaurants.storages.restaurant_storage import RestaurantStorage
from restaurants.storages.review_storage import ReviewStorage


def get_scored_restaurant_menu_items(root, info, params):

    restaurant_storage = RestaurantStorage()
    review_storage = ReviewStorage()

    interactor = GetScoredItemsInteractor(
        restaurant_storage=restaurant_storage, review_storage=review_storage
    )

    try:
        scored_item_dtos = interactor.get_scored_restaurant_items(
            restaurant_id=params.restaurant_id,
            user_id=info.context.user_id,
            limit=params.limit,
            offset=params.offset,
        )

        result = [
            ScoreItemType(
                restaurant_id=each.restaurant_id,
                menu_item_id=each.menu_item_id,
                name=each.name,
                price=each.price,
                score=each.score,
                average_rating=each.average_rating,
                total_orders_count=each.total_order_count,
                recently_order_count=each.order_count,
                is_available=each.is_available,
            )
            for each in scored_item_dtos
        ]

        return ScoredItemsType(menu_items=result)

    except custom_exceptions.RestaurantNotFound as e:
        return RestaurantNotFound(restaurant_id=e.restaurant_id)
    except custom_exceptions.InvalidLimitFound as e:
        return InvalidLimit(limit=e.limit)
    except custom_exceptions.InvalidOffsetFound as e:
        return InvalidOffset(offset=e.offset)
