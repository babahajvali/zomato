from decimal import Decimal
from typing import List

from django.db.models import Avg, Count

from restaurants.interactors.dtos import (
    CreateReviewDTO,
    ReviewDTO,
    RestaurantReviewSummaryDTO,
    RatingSummaryDTO,
)
from restaurants.interactors.storage_interface.review_storage_interface import (
    ReviewStorageInterface,
)
from restaurants.models import RestaurantReview


class ReviewStorage(ReviewStorageInterface):
    def get_restaurant_review_summaries(
        self, restaurant_ids: List[str]
    ) -> List[RestaurantReviewSummaryDTO]:
        review_summaries = (
            RestaurantReview.objects.filter(restaurant_id__in=restaurant_ids)
            .values("restaurant_id")
            .annotate(
                average_rating=Avg("rating"),
                total_reviews=Count("id"),
            )
            .order_by("restaurant_id")
        )

        return [
            RestaurantReviewSummaryDTO(
                restaurant_id=str(summary["restaurant_id"]),
                average_rating=float(summary["average_rating"]),
                total_reviews=summary["total_reviews"],
            )
            for summary in review_summaries
        ]

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

    def get_rating_summary(self, restaurant_id: str) -> RatingSummaryDTO:
        reviews = RestaurantReview.objects.filter(restaurant_id=restaurant_id)

        result = reviews.aggregate(
            average_rating=Avg("rating"),
            total_reviews=Count("id"),
        )

        distribution_qs = reviews.values("rating").annotate(count=Count("id"))
        distribution = {str(row["rating"]): row["count"] for row in distribution_qs}

        for star in range(1, 6):
            distribution.setdefault(str(star), 0)

        return RatingSummaryDTO(
            average_rating=Decimal(str(result["average_rating"] or 0)).quantize(
                Decimal("0.01")
            ),
            total_reviews=result["total_reviews"] or 0,
            distribution=distribution,
        )
