from django.test import TestCase

from restaurants.models import RestaurantReview
from restaurants.storages.review_storage import ReviewStorage
from restaurants.tests.factories.interactor_factories import CreateReviewDTOFactory
from restaurants.tests.factories.storage_factories import (
    RestaurantFactory,
    RestaurantReviewFactory,
)


class TestReviewStorage(TestCase):
    def setUp(self):
        self.storage = ReviewStorage()

    def test_create_review_success(self):
        # Arrange
        restaurant = RestaurantFactory()
        create_review_dto = CreateReviewDTOFactory(
            restaurant_id=restaurant.id, rating=4, review="Great food and service!"
        )

        # Act
        result = self.storage.create_review(create_review_dto=create_review_dto)

        # Assert
        assert result.review_id is not None
        assert str(result.restaurant_id) == str(restaurant.id)
        assert str(result.customer_id) == str(create_review_dto.customer_id)
        assert result.rating == 4
        assert result.review == "Great food and service!"

    def test_get_restaurant_reviews_success(self):
        # Arrange
        restaurant_id = "test-restaurant"
        restaurant = RestaurantFactory(id=restaurant_id)

        reviews = RestaurantReviewFactory.create_batch(1, restaurant_id=restaurant_id)

        # Act
        result = self.storage.get_restaurant_reviews(restaurant_id=restaurant.id)

        # Assert
        assert len(result) == 1

        result_ratings = sorted([r.rating for r in result])
        expected_ratings = sorted([r.rating for r in reviews])

        assert result_ratings == expected_ratings

        for review in result:
            assert review.restaurant_id == restaurant.id

    def test_get_restaurant_reviews_empty(self):
        # Arrange
        restaurant = RestaurantFactory()

        # Act
        result = self.storage.get_restaurant_reviews(restaurant_id=restaurant.id)

        # Assert
        self.assertEqual(len(result), 0)

    def test_check_user_review_exists_true(self):
        # Arrange
        restaurant = RestaurantFactory()
        customer_id = "test-user"

        RestaurantReview.objects.create(
            restaurant=restaurant, customer_id=customer_id, rating=4, review_text="Good"
        )

        # Act
        result = self.storage.check_user_review_exists(
            user_id=customer_id, restaurant_id=restaurant.id
        )

        # Assert
        self.assertTrue(result)

    def test_check_user_review_exists_false(self):
        # Arrange
        restaurant = RestaurantFactory()
        customer_id = "test-user"

        # Act
        result = self.storage.check_user_review_exists(
            user_id=customer_id, restaurant_id=restaurant.id
        )

        # Assert
        self.assertFalse(result)

    def test_check_user_review_exists_different_restaurant(self):
        # Arrange
        restaurant1 = RestaurantFactory()
        restaurant2 = RestaurantFactory()
        customer_id = "test-user"

        RestaurantReview.objects.create(
            restaurant=restaurant1,
            customer_id=customer_id,
            rating=4,
            review_text="Good",
        )

        # Act
        result = self.storage.check_user_review_exists(
            user_id=customer_id, restaurant_id=restaurant2.id
        )

        # Assert
        self.assertFalse(result)
