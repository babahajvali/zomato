from typing import List

from restaurants.exception.custom_exceptions import DuplicateRestaurantTimings
from restaurants.interactors.dtos import (
    BulkUpdateRestaurantTimingDTO,
    RestaurantTimingDTO,
    CreateRestaurantTimingDTO,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from restaurants.mixins.restaurant_mixin import RestaurantMixin
from restaurants.mixins.restaurant_timing_mixin import TimingMixin
from utils.caching_decorators import invalidate_interactor_cache, interactor_cache


class RestaurantTimingInteractor(RestaurantMixin, TimingMixin):
    def __init__(
        self,
        restaurant_timing_storage: RestaurantTimingStorageInterface,
        restaurant_storage: RestaurantStorageInterface,
    ):
        self.restaurant_timing_storage = restaurant_timing_storage
        self.restaurant_storage = restaurant_storage

    @invalidate_interactor_cache(cache_name="restaurant_timings")
    def create_restaurant_timing(
        self, create_restaurant_timing_dto: CreateRestaurantTimingDTO, user_id: str
    ) -> RestaurantTimingDTO:
        self.validate_day_of_week(day_of_week=create_restaurant_timing_dto.day_of_week)
        self.validate_restaurant_exists(
            restaurant_id=create_restaurant_timing_dto.restaurant_id,
            restaurant_storage=self.restaurant_storage,
        )
        self.validate_user_is_restaurant_owner(
            restaurant_id=create_restaurant_timing_dto.restaurant_id,
            user_id=user_id,
            restaurant_storage=self.restaurant_storage,
        )

        self.validate_restaurant_timing_within_range(
            open_time=create_restaurant_timing_dto.open_time,
            close_time=create_restaurant_timing_dto.close_time,
        )

        return self.restaurant_timing_storage.create_bulk_restaurant_timing(
            create_restaurant_timing_dto=[create_restaurant_timing_dto]
        )[0]

    @interactor_cache(cache_name="restaurant_timings")
    def get_restaurant_timings(self, restaurant_id: str) -> List[RestaurantTimingDTO]:
        self.validate_restaurant_exists(
            restaurant_id=restaurant_id, restaurant_storage=self.restaurant_storage
        )

        return self.restaurant_timing_storage.get_restaurant_timings(
            restaurant_id=restaurant_id
        )

    @invalidate_interactor_cache(cache_name="restaurant_timings")
    def delete_restaurant_timing(self, timing_id: int, user_id: str):
        self.validate_restaurant_timing_exists(
            timing_id=timing_id,
            restaurant_timing_storage=self.restaurant_timing_storage,
        )
        self.validate_user_is_restaurant_owner_through_timing_id(
            timing_id=timing_id,
            user_id=user_id,
            restaurant_timing_storage=self.restaurant_timing_storage,
        )

        return self.restaurant_timing_storage.delete_restaurant_timing(
            timing_id=timing_id
        )

    def get_day_restaurant_timing(
        self, restaurant_id: str, day_of_week: int
    ) -> RestaurantTimingDTO:
        self.validate_restaurant_exists(
            restaurant_id=restaurant_id, restaurant_storage=self.restaurant_storage
        )

        return self.restaurant_timing_storage.get_day_restaurant_timing(
            restaurant_id=restaurant_id, day_of_week=day_of_week
        )

    def create_or_update_restaurant_timings(
        self, timing_dtos: List[CreateRestaurantTimingDTO]
    ) -> str:
        combinations = [
            (timing.restaurant_id, timing.day_of_week) for timing in timing_dtos
        ]
        self._validate_duplicate_combinations(combinations=combinations)

        to_create, to_update = self._split_new_and_existing(
            timing_dtos=timing_dtos,
            combinations=combinations,
        )

        created_timings = (
            self.restaurant_timing_storage.create_bulk_restaurant_timing(to_create)
            if to_create
            else []
        )
        updated_timings = (
            self.restaurant_timing_storage.update_bulk_restaurant_timings(to_update)
            if to_update
            else []
        )

        return (
            f"{len(created_timings)} restaurant timings created, "
            f"{len(updated_timings)} restaurant timings updated"
        )

    def _split_new_and_existing(
        self,
        timing_dtos: List[CreateRestaurantTimingDTO],
        combinations: List[tuple],
    ) -> tuple[List[CreateRestaurantTimingDTO], List[BulkUpdateRestaurantTimingDTO]]:
        existing_timings = (
            self.restaurant_timing_storage.get_existing_restaurant_timings(combinations)
        )

        existing_lookup = {
            (timing.restaurant_id, timing.day_of_week): timing.timing_id
            for timing in existing_timings
        }

        to_create = []
        to_update = []

        for dto in timing_dtos:
            key = (dto.restaurant_id, dto.day_of_week)
            if key in existing_lookup:
                to_update.append(
                    BulkUpdateRestaurantTimingDTO(
                        timing_id=existing_lookup[key],
                        open_time=dto.open_time,
                        close_time=dto.close_time,
                    )
                )
            else:
                to_create.append(dto)

        return to_create, to_update

    @staticmethod
    def _validate_duplicate_combinations(combinations: List[tuple]):
        seen = set()
        duplicates = []

        for combo in combinations:
            if combo in seen:
                duplicates.append(combo[0])
            seen.add(combo)

        if duplicates:
            raise DuplicateRestaurantTimings(restaurant_ids=duplicates)
