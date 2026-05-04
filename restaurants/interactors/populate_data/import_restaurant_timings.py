from typing import List

from restaurants.exception.custom_exceptions import DuplicateRestaurantTimings
from restaurants.interactors.dtos import CreateRestaurantTimingDTO
from restaurants.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportRestaurantTimings:
    def __init__(
        self, restaurant_timing_storage_interface: RestaurantTimingStorageInterface
    ):
        self.restaurant_timing_storage_interface = restaurant_timing_storage_interface

    def import_restaurant_timings(
        self, file_path="./sample_data/restaurant_timings.csv"
    ):
        rows = read_csv(file_path=file_path)

        combinations = self._parse_and_normalize_rows(rows=rows)
        self._validate_duplicate_combinations(combinations)
        timings_dto = self._build_restaurant_timing_dtos(rows=rows)

        created_timings = (
            self.restaurant_timing_storage_interface.create_bulk_restaurant_timing(
                timings_dto
            )
        )

        return f"{len(created_timings)} restaurant timings were created"

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
