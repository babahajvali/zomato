from typing import List

from restaurants.interactors.dtos import CreateRestaurantTimingDTO
from restaurants.interactors.restaurant_timing.restaurant_timing_interactor import (
    RestaurantTimingInteractor,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportRestaurantTimings:
    def __init__(
        self,
        restaurant_timing_storage: RestaurantTimingStorageInterface,
        restaurant_storage: RestaurantStorageInterface,
    ):
        self.restaurant_timing_storage = restaurant_timing_storage
        self.restaurant_storage = restaurant_storage

    def import_restaurant_timings(
        self, file_path="./sample_data/restaurant_timings.csv"
    ):
        rows = list(read_csv(file_path=file_path))

        self._validate_rows(rows=rows)
        timings_dto = self._build_restaurant_timing_dtos(rows=rows)

        interactor = RestaurantTimingInteractor(
            restaurant_timing_storage=self.restaurant_timing_storage,
            restaurant_storage=self.restaurant_storage,
        )

        return interactor.create_or_update_restaurant_timings(timing_dtos=timings_dto)

    @staticmethod
    def _validate_rows(rows):
        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                ["restaurant", "day_of_week", "open_time", "close_time"],
                f"restaurants timing row {index}",
            )
            row["restaurant"] = row["restaurant"].strip()
            row["day_of_week"] = int(row["day_of_week"])
            row["open_time"] = row["open_time"].strip()
            row["close_time"] = row["close_time"].strip()

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
