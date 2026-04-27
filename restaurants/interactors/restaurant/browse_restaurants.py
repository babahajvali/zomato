from typing import List

from restaurants.interactors.dtos import (
    BrowseRestaurantDTO,
    BrowseRestaurantFiltersDTO,
    RestaurantDTO,
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
from restaurants.mixins.restaurant_mixin import RestaurantMixin
from restaurants.mixins.restaurant_timing_mixin import TimingMixin


class BrowseRestaurantsInteractor(RestaurantMixin, TimingMixin):
    def __init__(
        self,
        restaurant_storage: RestaurantStorageInterface,
        restaurant_timing_storage: RestaurantTimingStorageInterface,
        review_storage: ReviewStorageInterface,
    ):
        super().__init__(
            restaurant_storage=restaurant_storage,
            restaurant_timing_storage=restaurant_timing_storage,
        )
        self.restaurant_storage = restaurant_storage
        self.restaurant_timing_storage = restaurant_timing_storage
        self.review_storage = review_storage

    def browse_restaurants(
        self,
        filters_dto: BrowseRestaurantFiltersDTO,
    ) -> List[BrowseRestaurantDTO]:
        self._validate_filters(filters_dto=filters_dto)

        restaurants = self.restaurant_storage.get_restaurants(filters_dto=filters_dto)

        return self._get_browse_restaurants(restaurants=restaurants)

    def get_restaurant_owner_id(self, restaurant_id: str) -> str:
        self.validate_restaurant_is_exists(restaurant_id=restaurant_id)

        return self.restaurant_storage.get_restaurant_owner_id(
            restaurant_id=restaurant_id
        )

    def _validate_filters(self, filters_dto: BrowseRestaurantFiltersDTO):

        if filters_dto.min_rating is not None:
            self.validate_min_rating(min_rating=filters_dto.min_rating)

    def _get_browse_restaurants(
        self,
        restaurants: List[RestaurantDTO],
    ) -> List[BrowseRestaurantDTO]:
        restaurant_ids = [str(restaurant.id) for restaurant in restaurants]

        timings = self.restaurant_timing_storage.get_operating_hours_for_restaurants(
            restaurant_ids=restaurant_ids
        )
        review_summaries = self.review_storage.get_restaurant_review_summaries(
            restaurant_ids=restaurant_ids
        )

        restaurant_dtos = self.compute_is_open_bulk(
            restaurants=restaurants,
            timings=timings,
            review_summaries=review_summaries,
        )

        return restaurant_dtos
