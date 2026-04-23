from restaurants.exception.custom_exceptions import (
    UserAlreadyReviewedRestaurant,
    InvalidRatingFound,
)
from restaurants.interactors.dtos import CreateReviewDTO, ReviewDTO
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.storage_interface.review_storage_interface import (
    ReviewStorageInterface,
)
from restaurants.mixins.restaurant_mixin import RestaurantMixin


class CreateReviewInteractor(RestaurantMixin):
    def __init__(
        self,
        review_storage: ReviewStorageInterface,
        restaurant_storage: RestaurantStorageInterface,
    ):
        super().__init__(restaurant_storage=restaurant_storage)
        self.review_storage = review_storage
        self.restaurant_storage = restaurant_storage

    def create_review(self, create_review_dto: CreateReviewDTO) -> ReviewDTO:

        self.validate_restaurant_is_exists(
            restaurant_id=create_review_dto.restaurant_id
        )
        self._validate_rating(rating=create_review_dto.rating)
        self._validate_user_has_not_reviewed(
            user_id=create_review_dto.customer_id,
            restaurant_id=create_review_dto.restaurant_id,
        )

        return self.review_storage.create_review(create_review_dto=create_review_dto)

    def _validate_user_has_not_reviewed(self, user_id: str, restaurant_id: str):
        is_review_exists = self.review_storage.check_user_review_exists(
            user_id=user_id, restaurant_id=restaurant_id
        )

        if is_review_exists:
            raise UserAlreadyReviewedRestaurant(user_id=user_id)

    @staticmethod
    def _validate_rating(rating: int):
        print(rating)
        if rating < 1 or rating > 5:
            raise InvalidRatingFound(rating=rating)
