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

    def test_get_restaurant_review_summaries_success(self):
        restaurant_1 = RestaurantFactory(id="restaurant-1")
        restaurant_2 = RestaurantFactory(id="restaurant-2")

        RestaurantReviewFactory(restaurant=restaurant_1, rating=4, customer_id="user-1")
        RestaurantReviewFactory(restaurant=restaurant_1, rating=5, customer_id="user-2")
        RestaurantReviewFactory(restaurant=restaurant_2, rating=3, customer_id="user-3")

        result = self.storage.get_restaurant_review_summaries(
            restaurant_ids=["restaurant-1", "restaurant-2"]
        )

        assert len(result) == 2
        assert result[0].restaurant_id == "restaurant-1"
        assert result[0].average_rating == 4.5
        assert result[0].total_reviews == 2
        assert result[1].restaurant_id == "restaurant-2"
        assert result[1].average_rating == 3.0
        assert result[1].total_reviews == 1

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
