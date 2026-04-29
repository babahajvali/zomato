from typing import List

from restaurants.exception.custom_exceptions import (
    RestaurantAlreadyReviewedByUser,
    InvalidRating,
)
from restaurants.interactors.dtos import (
    CreateReviewDTO,
    ReviewDTO,
    RestaurantReviewSummaryDTO,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.storage_interface.review_storage_interface import (
    ReviewStorageInterface,
)
from restaurants.mixins.restaurant_mixin import RestaurantMixin


class ReviewInteractor(RestaurantMixin):
    def __init__(
        self,
        review_storage: ReviewStorageInterface,
        restaurant_storage: RestaurantStorageInterface,
    ):
        super().__init__(restaurant_storage=restaurant_storage)
        self.review_storage = review_storage
        self.restaurant_storage = restaurant_storage

    def create_review(self, create_review_dto: CreateReviewDTO) -> ReviewDTO:

        self.validate_restaurant_exists(restaurant_id=create_review_dto.restaurant_id)
        self._validate_rating(rating=create_review_dto.rating)
        self._validate_user_has_not_reviewed(
            user_id=create_review_dto.customer_id,
            restaurant_id=create_review_dto.restaurant_id,
        )

        return self.review_storage.create_review(create_review_dto=create_review_dto)

    def get_restaurant_review_summaries(
        self, restaurant_ids: List[str]
    ) -> List[RestaurantReviewSummaryDTO]:
        return self.review_storage.get_restaurant_review_summaries(
            restaurant_ids=restaurant_ids
        )

    def _validate_user_has_not_reviewed(self, user_id: str, restaurant_id: str):
        is_review_exists = self.review_storage.check_user_review_exists(
            user_id=user_id, restaurant_id=restaurant_id
        )

        if is_review_exists:
            raise RestaurantAlreadyReviewedByUser(user_id=user_id)

    @staticmethod
    def _validate_rating(rating: int):
        if rating < 1 or rating > 5:
            raise InvalidRating(rating=rating)
