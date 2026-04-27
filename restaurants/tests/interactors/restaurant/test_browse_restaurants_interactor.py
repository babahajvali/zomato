from datetime import datetime, time
from unittest.mock import Mock, create_autospec

from restaurants.interactors.restaurant.browse_restaurants import (
    BrowseRestaurantsInteractor,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from restaurants.interactors.storage_interface.review_storage_interface import (
    ReviewStorageInterface,
)
from restaurants.tests.factories.interactor_factories import (
    RestaurantDTOFactory,
    RestaurantReviewSummaryDTOFactory,
    RestaurantTimingDTOFactory,
)


class TestBrowseRestaurantsInteractor:
    def setup_method(self):
        self.restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.restaurant_timing_storage = create_autospec(
            RestaurantTimingStorageInterface
        )
        self.review_storage = create_autospec(ReviewStorageInterface)
        self.interactor = BrowseRestaurantsInteractor(
            restaurant_storage=self.restaurant_storage,
            restaurant_timing_storage=self.restaurant_timing_storage,
            review_storage=self.review_storage,
        )

    def test_browse_restaurants_maps_review_summary(self):
        restaurant = RestaurantDTOFactory(id="restaurant-1")
        timing = RestaurantTimingDTOFactory(
            restaurant_id="restaurant-1",
            day_of_week=datetime.now().isoweekday(),
            open_time=time(0, 0),
            close_time=time(23, 59),
        )
        review_summary = RestaurantReviewSummaryDTOFactory(
            restaurant_id="restaurant-1",
            average_rating=4.5,
            total_reviews=2,
        )
        filters_dto = Mock(min_rating=None)

        self.restaurant_storage.get_restaurants.return_value = [restaurant]
        self.restaurant_timing_storage.get_operating_hours_for_restaurants.return_value = [
            timing
        ]
        self.review_storage.get_restaurant_review_summaries.return_value = [
            review_summary
        ]

        result = self.interactor.browse_restaurants(filters_dto=filters_dto)

        assert len(result) == 1
        assert result[0].average_rating == 4.5
        assert result[0].total_reviews == 2
        self.review_storage.get_restaurant_review_summaries.assert_called_once_with(
            restaurant_ids=["restaurant-1"]
        )
