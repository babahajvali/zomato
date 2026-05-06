import pytest
from unittest.mock import create_autospec

from restaurants.exception.custom_exceptions import (
    RestaurantAlreadyReviewedByUser,
    InvalidRating,
    RestaurantNotFound,
)
from restaurants.interactors.review.review_interactor import (
    ReviewInteractor,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.storage_interface.review_storage_interface import (
    ReviewStorageInterface,
)
from restaurants.tests.factories.interactor_factories import (
    CreateReviewDTOFactory,
    ReviewDTOFactory,
)


class TestCreateReviewInteractor:
    def setup_method(self):
        self.mock_review_storage = create_autospec(ReviewStorageInterface)
        self.mock_restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.interactor = ReviewInteractor(
            review_storage=self.mock_review_storage,
            restaurant_storage=self.mock_restaurant_storage,
        )

    def test_create_review_success(self):
        # Arrange
        create_review_dto = CreateReviewDTOFactory()
        expected_review = ReviewDTOFactory(
            restaurant_id=create_review_dto.restaurant_id,
            customer_id=create_review_dto.customer_id,
            rating=create_review_dto.rating,
            review=create_review_dto.review,
        )

        self.mock_restaurant_storage.check_restaurant_is_exist.return_value = True
        self.mock_review_storage.check_user_review_exists.return_value = False
        self.mock_review_storage.create_review.return_value = expected_review

        # Act
        result = self.interactor.create_review(create_review_dto=create_review_dto)

        # Assert
        assert result == expected_review
        self.mock_restaurant_storage.check_restaurant_is_exist.assert_called_once_with(
            restaurant_id=create_review_dto.restaurant_id
        )
        self.mock_review_storage.check_user_review_exists.assert_called_once_with(
            user_id=create_review_dto.customer_id,
            restaurant_id=create_review_dto.restaurant_id,
        )
        self.mock_review_storage.create_review.assert_called_once_with(
            create_review_dto=create_review_dto
        )

    def test_create_review_restaurant_not_found(self):
        # Arrange
        create_review_dto = CreateReviewDTOFactory()

        self.mock_restaurant_storage.check_restaurant_is_exist.side_effect = (
            RestaurantNotFound(restaurant_id=create_review_dto.restaurant_id)
        )

        # Act & Assert
        with pytest.raises(RestaurantNotFound) as exc_info:
            self.interactor.create_review(create_review_dto=create_review_dto)

        assert exc_info.value.restaurant_id == create_review_dto.restaurant_id
        self.mock_restaurant_storage.check_restaurant_is_exist.assert_called_once_with(
            restaurant_id=create_review_dto.restaurant_id
        )
        self.mock_review_storage.check_user_review_exists.assert_not_called()
        self.mock_review_storage.create_review.assert_not_called()

    def test_create_review_invalid_rating_low(self):
        # Arrange
        create_review_dto = CreateReviewDTOFactory(rating=0)

        self.mock_restaurant_storage.check_restaurant_is_exist.return_value = True

        # Act & Assert
        with pytest.raises(InvalidRating) as exc_info:
            self.interactor.create_review(create_review_dto=create_review_dto)

        assert exc_info.value.rating == 0
        self.mock_restaurant_storage.check_restaurant_is_exist.assert_called_once_with(
            restaurant_id=create_review_dto.restaurant_id
        )
        self.mock_review_storage.check_user_review_exists.assert_not_called()
        self.mock_review_storage.create_review.assert_not_called()

    def test_create_review_invalid_rating_high(self):
        # Arrange
        create_review_dto = CreateReviewDTOFactory(rating=6)

        self.mock_restaurant_storage.check_restaurant_is_exist.return_value = True

        # Act & Assert
        with pytest.raises(InvalidRating) as exc_info:
            self.interactor.create_review(create_review_dto=create_review_dto)

        assert exc_info.value.rating == 6
        self.mock_restaurant_storage.check_restaurant_is_exist.assert_called_once_with(
            restaurant_id=create_review_dto.restaurant_id
        )
        self.mock_review_storage.check_user_review_exists.assert_not_called()
        self.mock_review_storage.create_review.assert_not_called()

    def test_create_review_user_already_reviewed(self):
        # Arrange
        create_review_dto = CreateReviewDTOFactory()

        self.mock_restaurant_storage.check_restaurant_is_exist.return_value = True
        self.mock_review_storage.check_user_review_exists.return_value = True

        # Act & Assert
        with pytest.raises(RestaurantAlreadyReviewedByUser) as exc_info:
            self.interactor.create_review(create_review_dto=create_review_dto)

        assert exc_info.value.user_id == create_review_dto.customer_id
        self.mock_restaurant_storage.check_restaurant_is_exist.assert_called_once_with(
            restaurant_id=create_review_dto.restaurant_id
        )
        self.mock_review_storage.check_user_review_exists.assert_called_once_with(
            user_id=create_review_dto.customer_id,
            restaurant_id=create_review_dto.restaurant_id,
        )
        self.mock_review_storage.create_review.assert_not_called()

    def test_create_review_boundary_rating_1(self):
        create_review_dto = CreateReviewDTOFactory(rating=1)
        expected_review = ReviewDTOFactory(
            restaurant_id=create_review_dto.restaurant_id,
            customer_id=create_review_dto.customer_id,
            rating=1,
            review=create_review_dto.review,
        )

        self.mock_restaurant_storage.check_restaurant_is_exist.return_value = True
        self.mock_review_storage.check_user_review_exists.return_value = False
        self.mock_review_storage.create_review.return_value = expected_review

        result = self.interactor.create_review(create_review_dto=create_review_dto)

        assert result == expected_review
        assert result.rating == 1
        self.mock_review_storage.create_review.assert_called_once_with(
            create_review_dto=create_review_dto
        )

    def test_create_review_boundary_rating_5(self):
        create_review_dto = CreateReviewDTOFactory(rating=5)
        expected_review = ReviewDTOFactory(
            restaurant_id=create_review_dto.restaurant_id,
            customer_id=create_review_dto.customer_id,
            rating=5,
            review=create_review_dto.review,
        )

        self.mock_restaurant_storage.check_restaurant_is_exist.return_value = True
        self.mock_review_storage.check_user_review_exists.return_value = False
        self.mock_review_storage.create_review.return_value = expected_review

        result = self.interactor.create_review(create_review_dto=create_review_dto)

        assert result == expected_review
        assert result.rating == 5
        self.mock_review_storage.create_review.assert_called_once_with(
            create_review_dto=create_review_dto
        )
