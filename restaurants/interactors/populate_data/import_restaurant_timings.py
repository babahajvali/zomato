from typing import List

from restaurants.exception.custom_exceptions import DuplicateRestaurantTimings
from restaurants.interactors.dtos import (
    BulkUpdateRestaurantTimingDTO,
    CreateRestaurantTimingDTO,
)
from restaurants.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportRestaurantTimings:
    def __init__(self, restaurant_timing_storage: RestaurantTimingStorageInterface):
        self.restaurant_timing_storage = restaurant_timing_storage

    def import_restaurant_timings(
        self, file_path="./sample_data/restaurant_timings.csv"
    ):
        rows = read_csv(file_path=file_path)

        combinations = self._parse_and_normalize_rows(rows=rows)
        self._validate_duplicate_combinations(combinations)
        timings_dto = self._build_restaurant_timing_dtos(rows=rows)

        to_create, to_update = self._split_new_and_existing(
            timing_dtos=timings_dto,
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

    @staticmethod
    def _parse_and_normalize_rows(rows) -> List[tuple]:
        combinations = []
        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                ["restaurant", "day_of_week", "open_time", "close_time"],
                f"restaurants timing row {index}",
            )
            row["restaurant"] = row["restaurant"].strip()
            row["day_of_week"] = int(row["day_of_week"])
            combinations.append((row["restaurant"], row["day_of_week"]))
        return combinations

    @staticmethod
    def _build_restaurant_timing_dtos(rows) -> List[CreateRestaurantTimingDTO]:
        return [
            CreateRestaurantTimingDTO(
                restaurant_id=row["restaurant"],
                day_of_week=row["day_of_week"],
                open_time=row["open_time"],
                close_time=row["close_time"],
            )
            for row in rows
        ]
