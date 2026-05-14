import graphene

from restaurants.exception import custom_exceptions
from restaurants.graphql.types.error_types import (
    RestaurantNotFound,
    RestaurantAlreadyReviewedByUser,
    InvalidRatingFound,
)
from restaurants.graphql.types.input_types import CreateReviewInputParams
from restaurants.graphql.types.response_types import CreateReviewResponse
from restaurants.graphql.types.types import ReviewType
from restaurants.interactors.dtos import CreateReviewDTO
from restaurants.interactors.review.review_interactor import (
    ReviewInteractor,
)
from restaurants.storages.restaurant_storage import RestaurantStorage
from restaurants.storages.review_storage import ReviewStorage


class CreateReviewMutation(graphene.Mutation):
    class Arguments:
        params = CreateReviewInputParams(required=True)

    Output = CreateReviewResponse

    @staticmethod
    def mutate(root, info, params):

        restaurant_storage = RestaurantStorage()
        review_storage = ReviewStorage()

        interactor = ReviewInteractor(
            restaurant_storage=restaurant_storage,
            review_storage=review_storage,
        )

        create_review_dto = CreateReviewDTO(
            restaurant_id=params.restaurant_id,
            customer_id=info.context.user_id,
            rating=params.rating,
            review=params.review,
        )

        try:
            result = interactor.create_review(create_review_dto=create_review_dto)

            # TODO: created_at not populated on the response though ReviewType declares it. Pass result.created_at through.
            return ReviewType(
                review_id=result.review_id,
                restaurant_id=result.restaurant_id,
                customer_id=result.customer_id,
                rating=result.rating,
                review=result.review,
                created_at=result.created_at,
            )

        except custom_exceptions.RestaurantNotFound as e:
            return RestaurantNotFound(restaurant_id=e.restaurant_id)
        except custom_exceptions.RestaurantAlreadyReviewedByUser as e:
            return RestaurantAlreadyReviewedByUser(user_id=e.user_id)
        except custom_exceptions.InvalidRating as e:
            return InvalidRatingFound(user_rating=e.rating)
