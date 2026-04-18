from typing import List

from restaurant.interactors.dtos import (
    BrowseRestaurantDTO,
    BrowseRestaurantFiltersDTO,
)
from restaurant.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurant.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from restaurant.mixins.restaurant_mixin import RestaurantMixin
from restaurant.mixins.restaurant_timing_mixin import TimingMixin


class BrowseRestaurantsInteractor(RestaurantMixin, TimingMixin):
    def __init__(
            self,
            restaurant_storage: RestaurantStorageInterface,
            restaurant_timing_storage: RestaurantTimingStorageInterface,
    ):
        super().__init__(
            restaurant_storage=restaurant_storage,
            restaurant_timing_storage=restaurant_timing_storage,
        )
        self.restaurant_storage = restaurant_storage
        self.restaurant_timing_storage = restaurant_timing_storage

    def browse_restaurants(
            self,
            filters_dto: BrowseRestaurantFiltersDTO,
    ) -> List[BrowseRestaurantDTO]:
        self._validate_filters(filters_dto=filters_dto)

        restaurants = self.restaurant_storage.get_restaurants(
            filters_dto=filters_dto
        )

        return self._attach_is_open(restaurants=restaurants)

    def _validate_filters(self, filters_dto: BrowseRestaurantFiltersDTO):
        if filters_dto.cuisine_type:
            cuisine_type = (
                filters_dto.cuisine_type.value
                if hasattr(filters_dto.cuisine_type, "value")
                else str(filters_dto.cuisine_type)
            )
            self.check_cuisine_type_is_valid(cuisine_type=cuisine_type)

        if filters_dto.min_rating is not None:
            self.check_min_rating_is_valid(
                min_rating=filters_dto.min_rating
            )

    def _attach_is_open(
            self,
            restaurants: List[BrowseRestaurantDTO],
    ) -> List[BrowseRestaurantDTO]:
        restaurant_ids = [str(restaurant.restaurant_id) for restaurant in restaurants]

        timings = self.restaurant_timing_storage.get_operating_hours_for_restaurants(
            restaurant_ids=restaurant_ids
        )

        self.compute_is_open_bulk(
            restaurants=restaurants,
            timings=timings,
        )

        return restaurants
