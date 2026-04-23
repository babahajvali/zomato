from restaurants.interactors.dtos import CreateReviewDTO, ReviewDTO
from restaurants.interactors.storage_interface.review_storage_interface import (
    ReviewStorageInterface,
)
from restaurants.models import RestaurantReview


class ReviewStorage(ReviewStorageInterface):
    @staticmethod
    def _convert_to_review_dto(review_obj: RestaurantReview) -> ReviewDTO:
        return ReviewDTO(
            review_id=review_obj.pk,
            restaurant_id=review_obj.restaurant.id,
            customer_id=review_obj.customer_id,
            rating=review_obj.rating,
            review=review_obj.review_text,
        )

    def get_restaurant_reviews(self, restaurant_id: str):
        restaurant_reviews = RestaurantReview.objects.filter(
            restaurant_id=restaurant_id
        )

        return [
            self._convert_to_review_dto(review_obj=each) for each in restaurant_reviews
        ]

    def create_review(self, create_review_dto: CreateReviewDTO) -> ReviewDTO:
        created_review = RestaurantReview.objects.create(
            restaurant_id=create_review_dto.restaurant_id,
            customer_id=create_review_dto.customer_id,
            rating=create_review_dto.rating,
            review_text=create_review_dto.review,
        )

        return self._convert_to_review_dto(review_obj=created_review)

    def check_user_review_exists(self, user_id: str, restaurant_id: str) -> bool:
        return RestaurantReview.objects.filter(
            customer_id=user_id, restaurant_id=restaurant_id
        ).exists()
