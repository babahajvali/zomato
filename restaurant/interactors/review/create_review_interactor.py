from restaurant.exception.custom_exceptions import UserAlreadyReviewedRestaurant
from restaurant.interactors.dtos import CreateReviewDTO, ReviewDTO
from restaurant.interactors.storage_interface.review_storage_interface import (
    ReviewStorageInterface,
)


class CreateReviewInteractor:
    def __init__(self, review_storage: ReviewStorageInterface):
        self.review_storage = review_storage

    def create_review(self, create_review_dto: CreateReviewDTO) -> ReviewDTO:

        self._validate_user_has_not_reviewed(user_id=create_review_dto.customer_id)

        return self.review_storage.create_review(create_review_dto=create_review_dto)

    def _validate_user_has_not_reviewed(self, user_id: str):
        is_review_exists = self.review_storage.check_user_review_exists(user_id=user_id)

        if is_review_exists:
            raise UserAlreadyReviewedRestaurant(user_id=user_id)
