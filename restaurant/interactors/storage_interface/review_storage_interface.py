from abc import ABC, abstractmethod

from restaurant.interactors.dtos import CreateReviewDTO, ReviewDTO


class ReviewStorageInterface(ABC):
    @abstractmethod
    def get_restaurant_reviews(self, restaurant_id: str):
        pass

    @abstractmethod
    def create_review(self, create_review_dto: CreateReviewDTO) -> ReviewDTO:
        pass

    @abstractmethod
    def check_user_review_exists(self, user_id: str) -> bool:
        pass
