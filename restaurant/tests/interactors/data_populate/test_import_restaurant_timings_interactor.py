from unittest.mock import MagicMock, create_autospec, patch

import pytest

from restaurant.exception.custom_exceptions import DuplicateRestaurantTimings
from restaurant.interactors.populate_data.import_restaurant_timings import (
    ImportRestaurantTimings,
)
from restaurant.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from restaurant.tests.factories.interactor_factories import (
    CreateRestaurantTimingDTOFactory,
)


class TestImportRestaurantTimings:
    def setup_method(self):
        self.restaurant_timing_storage = create_autospec(
            RestaurantTimingStorageInterface
        )
        self.interactor = ImportRestaurantTimings(
            restaurant_timing_storage_interface=self.restaurant_timing_storage
        )

    def test_import_restaurant_timings_success(self):
        rows = [
            {
                "restaurant": " restaurant-1 ",
                "day_of_week": "1",
                "open_time": "09:00:00",
                "close_time": "21:00:00",
            }
        ]
        expected_dto = CreateRestaurantTimingDTOFactory(
            restaurant_id="restaurant-1",
            day_of_week=1,
            open_time="09:00:00",
            close_time="21:00:00",
        )
        expected_result = ["created-timing"]
        validate_row = MagicMock()
        self.restaurant_timing_storage.create_bulk_restaurant_timing.return_value = (
            expected_result
        )

        with patch(
            "restaurant.interactors.populate_data.import_restaurant_timings.read_csv",
            return_value=rows,
        ), patch(
            "restaurant.interactors.populate_data.import_restaurant_timings.validate_row",
            validate_row,
        ):
            result = self.interactor.import_restaurant_timings(
                file_path="restaurant_timings.csv"
            )

        assert result == expected_result
        validate_row.assert_called_once_with(
            rows[0],
            ["restaurant", "day_of_week", "open_time", "close_time"],
            "restaurant timing row 1",
        )
        self.restaurant_timing_storage.create_bulk_restaurant_timing.assert_called_once_with(
            [expected_dto]
        )

    def test_import_restaurant_timings_duplicate_combination(self):
        rows = [
            {
                "restaurant": " restaurant-1 ",
                "day_of_week": "1",
                "open_time": "09:00:00",
                "close_time": "21:00:00",
            },
            {
                "restaurant": "restaurant-1",
                "day_of_week": "1",
                "open_time": "10:00:00",
                "close_time": "22:00:00",
            },
        ]

        with patch(
            "restaurant.interactors.populate_data.import_restaurant_timings.read_csv",
            return_value=rows,
        ), patch(
            "restaurant.interactors.populate_data.import_restaurant_timings.validate_row",
            MagicMock(),
        ):
            with pytest.raises(DuplicateRestaurantTimings) as exc:
                self.interactor.import_restaurant_timings(
                    file_path="restaurant_timings.csv"
                )

        assert exc.value.restaurant_ids == ["restaurant-1"]
        self.restaurant_timing_storage.create_bulk_restaurant_timing.assert_not_called()
