from abc import ABC, abstractmethod
from typing import List

from restaurants.interactors.dtos import (
    CreateReviewDTO,
    ReviewDTO,
    RestaurantReviewSummaryDTO,
    RatingSummaryDTO,
)


class ReviewStorageInterface(ABC):
    @abstractmethod
    def get_restaurant_review_summaries(
        self, restaurant_ids: List[str]
    ) -> List[RestaurantReviewSummaryDTO]:
        pass

    @abstractmethod
    def get_restaurant_reviews(self, restaurant_id: str):
        pass

    @abstractmethod
    def create_review(self, create_review_dto: CreateReviewDTO) -> ReviewDTO:
        pass

    @abstractmethod
    def check_user_review_exists(self, user_id: str, restaurant_id: str) -> bool:
        pass

    @abstractmethod
    def get_rating_summary(self, restaurant_id: str) -> RatingSummaryDTO:
        pass

    @abstractmethod
    def get_user_restaurant_review(self, restaurant_id: str, user_id: str) -> ReviewDTO:
        pass
