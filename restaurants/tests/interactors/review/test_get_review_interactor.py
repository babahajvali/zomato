from unittest.mock import create_autospec

from restaurants.interactors.review.review_interactor import ReviewInteractor
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.storage_interface.review_storage_interface import (
    ReviewStorageInterface,
)
from restaurants.tests.factories.interactor_factories import ReviewDTOFactory


class TestGetReviewInteractor:
    def setup_method(self):
        self.mock_review_storage = create_autospec(ReviewStorageInterface)
        self.mock_restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.interactor = ReviewInteractor(
            review_storage=self.mock_review_storage,
            restaurant_storage=self.mock_restaurant_storage,
        )

    def test_get_user_restaurant_review_success(self):
        expected_review = ReviewDTOFactory(
            review_id=1,
            restaurant_id="restaurant-1",
            customer_id="user-1",
            rating=4,
            review="Good food",
        )
        self.mock_review_storage.get_user_restaurant_review.return_value = (
            expected_review
        )

        result = self.interactor.get_user_restaurant_review(
            user_id="user-1",
            restaurant_id="restaurant-1",
        )

        assert result == expected_review
        self.mock_review_storage.get_user_restaurant_review.assert_called_once_with(
            user_id="user-1",
            restaurant_id="restaurant-1",
        )

    def test_get_user_restaurant_review_returns_none(self):
        self.mock_review_storage.get_user_restaurant_review.return_value = None

        result = self.interactor.get_user_restaurant_review(
            user_id="user-1",
            restaurant_id="restaurant-1",
        )

        assert result is None
        self.mock_review_storage.get_user_restaurant_review.assert_called_once_with(
            user_id="user-1",
            restaurant_id="restaurant-1",
        )
