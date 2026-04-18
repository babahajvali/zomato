from typing import List

from restaurant.exception.custom_exceptions import DuplicateRestaurantTimings
from restaurant.interactors.dtos import CreateRestaurantTimingDTO
from restaurant.interactors.storage_interface.restaurant_timing_storage_interface import RestaurantTimingStorageInterface
from utils.read_csv_util import read_csv, validate_row


class ImportRestaurantTimings:

    def __init__(self, restaurant_timing_storage_interface: RestaurantTimingStorageInterface):
        self.restaurant_timing_storage_interface = restaurant_timing_storage_interface

    def import_restaurant_timings(self, file_path="./sample_data/restaurant_timings.csv"):
        rows = read_csv(file_path=file_path)

        combinations = []

        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                ['restaurant', 'day_of_week', 'open_time', 'close_time'],
                f"restaurant timing row {index}"
            )

            restaurant_id = row['restaurant'].strip()
            day_of_week = int(row['day_of_week'])

            row['restaurant'] = restaurant_id
            row['day_of_week'] = day_of_week

            combinations.append((restaurant_id, day_of_week))

        self._check_duplicate_combinations(combinations)

        timings_dto = [
            CreateRestaurantTimingDTO(
                restaurant_id=row['restaurant'],
                day_of_week=row['day_of_week'],
                open_time=row['open_time'],
                close_time=row['close_time']
            )
            for row in rows
        ]

        created_timings = self.restaurant_timing_storage_interface.create_bulk_restaurant_timing(
            timings_dto
        )

        return created_timings


    @staticmethod
    def _check_duplicate_combinations(combinations: List[tuple]):
        seen = set()
        duplicates = []

        for combo in combinations:
            if combo in seen:
                duplicates.append(combo[0])
            seen.add(combo)

        if duplicates:
            raise DuplicateRestaurantTimings(restaurant_ids=duplicates)