from decimal import Decimal
from unittest.mock import create_autospec

import pytest

from orders.app_service.dtos import RestaurantOrderStatsDTO
from restaurants.exception.custom_exceptions import (
    InvalidLimitFound,
    InvalidOffsetFound,
)
from restaurants.interactors.restaurant.get_scored_restaurant_interactor import (
    GetScoredRestaurantInteractor,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.storage_interface.review_storage_interface import (
    ReviewStorageInterface,
)
from restaurants.tests.factories.interactor_factories import (
    RestaurantDTOFactory,
    RestaurantReviewDTOFactory,
)


class TestGetScoredRestaurantInteractor:
    def setup_method(self):
        self.restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.review_storage = create_autospec(ReviewStorageInterface)
        self.interactor = GetScoredRestaurantInteractor(
            restaurant_storage=self.restaurant_storage,
            review_storage=self.review_storage,
        )
        self.interactor.order_adapter = create_autospec(
            self.interactor.order_adapter, instance=True
        )

    def test_get_scored_restaurant_success(self):
        restaurant_1 = RestaurantDTOFactory(
            id="restaurant-1",
            name="Restaurant 1",
            cuisine_type="INDIAN",
        )
        restaurant_2 = RestaurantDTOFactory(
            id="restaurant-2",
            name="Restaurant 2",
            cuisine_type="CHINESE",
        )
        review_1 = RestaurantReviewDTOFactory(
            restaurant_id="restaurant-1",
            avg_rating=Decimal("5.00"),
            total_reviews=10,
        )
        review_2 = RestaurantReviewDTOFactory(
            restaurant_id="restaurant-2",
            avg_rating=Decimal("3.00"),
            total_reviews=2,
        )
        stat_1 = RestaurantOrderStatsDTO(
            restaurant_id="restaurant-1",
            order_count=6,
            daily_frequent=4,
        )
        stat_2 = RestaurantOrderStatsDTO(
            restaurant_id="restaurant-2",
            order_count=2,
            daily_frequent=1,
        )
        self.restaurant_storage.get_delivered_pincode_restaurants.return_value = [
            restaurant_1,
            restaurant_2,
        ]
        self.review_storage.get_restaurants_reviews.return_value = [review_1, review_2]
        self.interactor.order_adapter.get_user_restaurants_stat.return_value = [
            stat_1,
            stat_2,
        ]

        result = self.interactor.get_scored_restaurant(
            pincode="500001",
            limit=10,
            offset=0,
            user_id="user-1",
        )

        assert len(result) == 2
        assert result[0].restaurant_id == "restaurant-1"
        assert result[0].average_rating == Decimal("5.00")
        assert result[0].total_reviews == 10
        assert result[0].order_volume == 6
        assert result[0].day_frequent == 4
        assert result[0].score == Decimal("1.0000")
        assert result[1].restaurant_id == "restaurant-2"
        assert result[1].score == Decimal("0.4200")
        self.restaurant_storage.get_delivered_pincode_restaurants.assert_called_once_with(
            pincode="500001"
        )
        self.review_storage.get_restaurants_reviews.assert_called_once_with(
            restaurant_ids=["restaurant-1", "restaurant-2"]
        )
        self.interactor.order_adapter.get_user_restaurants_stat.assert_called_once_with(
            restaurant_ids=["restaurant-1", "restaurant-2"],
            user_id="user-1",
        )

    def test_get_scored_restaurant_applies_limit_and_offset(self):
        restaurants = [
            RestaurantDTOFactory(id="restaurant-1"),
            RestaurantDTOFactory(id="restaurant-2"),
            RestaurantDTOFactory(id="restaurant-3"),
        ]
        reviews = [
            RestaurantReviewDTOFactory(
                restaurant_id="restaurant-1",
                avg_rating=Decimal("5.00"),
                total_reviews=5,
            ),
            RestaurantReviewDTOFactory(
                restaurant_id="restaurant-2",
                avg_rating=Decimal("4.00"),
                total_reviews=4,
            ),
            RestaurantReviewDTOFactory(
                restaurant_id="restaurant-3",
                avg_rating=Decimal("3.00"),
                total_reviews=3,
            ),
        ]
        self.restaurant_storage.get_delivered_pincode_restaurants.return_value = (
            restaurants
        )
        self.review_storage.get_restaurants_reviews.return_value = reviews
        self.interactor.order_adapter.get_user_restaurants_stat.return_value = []

        result = self.interactor.get_scored_restaurant(
            pincode="500001",
            limit=1,
            offset=1,
            user_id="user-1",
        )

        assert len(result) == 1
        assert result[0].restaurant_id == "restaurant-2"

    def test_get_scored_restaurant_defaults_missing_reviews_and_stats(self):
        restaurant = RestaurantDTOFactory(id="restaurant-1")
        self.restaurant_storage.get_delivered_pincode_restaurants.return_value = [
            restaurant
        ]
        self.review_storage.get_restaurants_reviews.return_value = []
        self.interactor.order_adapter.get_user_restaurants_stat.return_value = []

        result = self.interactor.get_scored_restaurant(
            pincode="500001",
            limit=10,
            offset=0,
            user_id="user-1",
        )

        assert len(result) == 1
        assert result[0].average_rating == Decimal("0")
        assert result[0].total_reviews == 0
        assert result[0].order_volume == 0
        assert result[0].day_frequent == 0
        assert result[0].score == Decimal("0.1000")

    def test_get_scored_restaurant_empty_results(self):
        self.restaurant_storage.get_delivered_pincode_restaurants.return_value = []
        self.review_storage.get_restaurants_reviews.return_value = []
        self.interactor.order_adapter.get_user_restaurants_stat.return_value = []

        result = self.interactor.get_scored_restaurant(
            pincode="500001",
            limit=10,
            offset=0,
            user_id="user-1",
        )

        assert result == []
        self.review_storage.get_restaurants_reviews.assert_called_once_with(
            restaurant_ids=[]
        )
        self.interactor.order_adapter.get_user_restaurants_stat.assert_called_once_with(
            restaurant_ids=[],
            user_id="user-1",
        )

    def test_get_scored_restaurant_with_invalid_limit(self):
        with pytest.raises(InvalidLimitFound) as exc:
            self.interactor.get_scored_restaurant(
                pincode="500001",
                limit=-1,
                offset=0,
                user_id="user-1",
            )

        assert exc.value.limit == -1
        self.restaurant_storage.get_delivered_pincode_restaurants.assert_not_called()

    def test_get_scored_restaurant_with_invalid_offset(self):
        with pytest.raises(InvalidOffsetFound) as exc:
            self.interactor.get_scored_restaurant(
                pincode="500001",
                limit=10,
                offset=-1,
                user_id="user-1",
            )

        assert exc.value.offset == -1
        self.restaurant_storage.get_delivered_pincode_restaurants.assert_not_called()
