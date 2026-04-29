from restaurants.graphql.types.types import ReviewType
from restaurants.interactors.review.review_interactor import ReviewInteractor
from restaurants.storages.restaurant_storage import RestaurantStorage
from restaurants.storages.review_storage import ReviewStorage


def get_user_restaurant_review_resolver(root, info, params):

    review_storage = ReviewStorage()
    restaurant_storage = RestaurantStorage()

    interactor = ReviewInteractor(
        review_storage=review_storage, restaurant_storage=restaurant_storage
    )

    result = interactor.get_user_restaurant_review(
        restaurant_id=params.restaurant_id, user_id=params.user_id
    )

    if result is None:
        return None

    return ReviewType(
        review_id=result.review_id,
        restaurant_id=result.restaurant_id,
        customer_id=result.customer_id,
        rating=result.rating,
        review=result.review,
        created_at=result.created_at,
    )
