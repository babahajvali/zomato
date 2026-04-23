from datetime import time
from unittest.mock import create_autospec

import pytest

from restaurants.interactors.dtos import RestaurantTimingDTO, UpdateRestaurantTimingDTO
from restaurants.interactors.restaurant_timing.update_restaurant_timing_interactor import (
    UpdateRestaurantTimingInteractor,
)
from restaurants.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from restaurants.exception.custom_exceptions import (
    OpenTimeGreaterThanCloseTime,
    RestaurantTimingNotFound,
    UserIsNotRestaurantOwner,
)


class TestUpdateRestaurantTimingInteractor:
    @staticmethod
    def _get_timing_dto(*, open_time_value=time(9, 0), close_time_value=time(21, 0)):
        return RestaurantTimingDTO(
            timing_id=1,
            restaurant_id="restaurants-1",
            day_of_week=1,
            open_time=open_time_value,
            close_time=close_time_value,
        )

    def setup_method(self):
        self.restaurant_timing_storage = create_autospec(
            RestaurantTimingStorageInterface
        )
        self.interactor = UpdateRestaurantTimingInteractor(
            restaurant_timing_storage=self.restaurant_timing_storage,
        )

    def _setup_dependencies(
        self,
        *,
        timing_exists=True,
        owner_id="user-123",
        storage_result=None,
        existing_open_time=time(9, 0),
        existing_close_time=time(21, 0),
    ):
        self.restaurant_timing_storage.get_restaurant_timing.return_value = (
            self._get_timing_dto(
                open_time_value=existing_open_time,
                close_time_value=existing_close_time,
            )
            if timing_exists
            else None
        )
        self.restaurant_timing_storage.get_restaurant_owner_id.return_value = owner_id
        self.restaurant_timing_storage.update_restaurant_timing.return_value = (
            storage_result if storage_result is not None else self._get_timing_dto()
        )

    def test_update_restaurant_timing_success(self, snapshot):
        update_dto = UpdateRestaurantTimingDTO(
            timing_id=1,
            user_id="user-123",
            open_time=time(10, 0),
            close_time=time(20, 0),
        )
        expected = self._get_timing_dto(
            open_time_value=time(10, 0),
            close_time_value=time(20, 0),
        )
        self._setup_dependencies(storage_result=expected)

        result = self.interactor.update_restaurant_timing(
            update_restaurant_timing_dto=update_dto
        )

        snapshot.assert_match(
            repr(result),
            "update_restaurant_timing_success.txt",
        )
        self.restaurant_timing_storage.update_restaurant_timing.assert_called_once_with(
            update_restaurant_timing_dto=update_dto
        )

    def test_update_restaurant_timing_not_found(self, snapshot):
        update_dto = UpdateRestaurantTimingDTO(
            timing_id=1,
            user_id="user-123",
            open_time=time(10, 0),
            close_time=time(20, 0),
        )
        self._setup_dependencies(timing_exists=False)

        with pytest.raises(RestaurantTimingNotFound) as exc:
            self.interactor.update_restaurant_timing(
                update_restaurant_timing_dto=update_dto
            )

        snapshot.assert_match(
            repr(exc.value),
            "update_restaurant_timing_not_found.txt",
        )
        self.restaurant_timing_storage.get_restaurant_owner_id.assert_not_called()
        self.restaurant_timing_storage.update_restaurant_timing.assert_not_called()

    def test_update_restaurant_timing_non_owner(self, snapshot):
        update_dto = UpdateRestaurantTimingDTO(
            timing_id=1,
            user_id="user-123",
            open_time=time(10, 0),
            close_time=time(20, 0),
        )
        self._setup_dependencies(owner_id="owner-456")

        with pytest.raises(UserIsNotRestaurantOwner) as exc:
            self.interactor.update_restaurant_timing(
                update_restaurant_timing_dto=update_dto
            )

        snapshot.assert_match(
            repr(exc.value),
            "update_restaurant_timing_non_owner.txt",
        )
        self.restaurant_timing_storage.update_restaurant_timing.assert_not_called()

    def test_update_restaurant_timing_open_time_greater_than_close_time(self, snapshot):
        update_dto = UpdateRestaurantTimingDTO(
            timing_id=1,
            user_id="user-123",
            open_time=time(22, 0),
            close_time=time(10, 0),
        )
        self._setup_dependencies()

        with pytest.raises(OpenTimeGreaterThanCloseTime) as exc:
            self.interactor.update_restaurant_timing(
                update_restaurant_timing_dto=update_dto
            )

        snapshot.assert_match(
            repr(exc.value),
            "update_restaurant_timing_open_time_greater_than_close_time.txt",
        )
        self.restaurant_timing_storage.update_restaurant_timing.assert_not_called()

    def test_update_restaurant_timing_open_time_equal_to_existing_close_time(
        self, snapshot
    ):
        update_dto = UpdateRestaurantTimingDTO(
            timing_id=1,
            user_id="user-123",
            open_time=time(21, 0),
            close_time=None,
        )
        self._setup_dependencies(existing_close_time=time(21, 0))

        with pytest.raises(OpenTimeGreaterThanCloseTime) as exc:
            self.interactor.update_restaurant_timing(
                update_restaurant_timing_dto=update_dto
            )

        snapshot.assert_match(
            repr(exc.value),
            "update_restaurant_timing_open_time_equal_to_existing_close_time.txt",
        )
        self.restaurant_timing_storage.update_restaurant_timing.assert_not_called()

    def test_update_restaurant_timing_close_time_equal_to_existing_open_time(
        self, snapshot
    ):
        update_dto = UpdateRestaurantTimingDTO(
            timing_id=1,
            user_id="user-123",
            open_time=None,
            close_time=time(9, 0),
        )
        self._setup_dependencies(existing_open_time=time(9, 0))

        with pytest.raises(OpenTimeGreaterThanCloseTime) as exc:
            self.interactor.update_restaurant_timing(
                update_restaurant_timing_dto=update_dto
            )

        snapshot.assert_match(
            repr(exc.value),
            "update_restaurant_timing_close_time_equal_to_existing_open_time.txt",
        )
        self.restaurant_timing_storage.update_restaurant_timing.assert_not_called()

    def test_update_restaurant_timing_only_open_time_success(self, snapshot):
        update_dto = UpdateRestaurantTimingDTO(
            timing_id=1,
            user_id="user-123",
            open_time=time(10, 0),
            close_time=None,
        )
        expected = self._get_timing_dto(
            open_time_value=time(10, 0),
            close_time_value=time(21, 0),
        )
        self._setup_dependencies(storage_result=expected)

        result = self.interactor.update_restaurant_timing(
            update_restaurant_timing_dto=update_dto
        )

        snapshot.assert_match(
            repr(result),
            "update_restaurant_timing_only_open_time_success.txt",
        )
        self.restaurant_timing_storage.update_restaurant_timing.assert_called_once_with(
            update_restaurant_timing_dto=update_dto
        )

    def test_update_restaurant_timing_only_close_time_success(self, snapshot):
        update_dto = UpdateRestaurantTimingDTO(
            timing_id=1,
            user_id="user-123",
            open_time=None,
            close_time=time(20, 0),
        )
        expected = self._get_timing_dto(
            open_time_value=time(9, 0),
            close_time_value=time(20, 0),
        )
        self._setup_dependencies(storage_result=expected)

        result = self.interactor.update_restaurant_timing(
            update_restaurant_timing_dto=update_dto
        )

        snapshot.assert_match(
            repr(result),
            "update_restaurant_timing_only_close_time_success.txt",
        )
        self.restaurant_timing_storage.update_restaurant_timing.assert_called_once_with(
            update_restaurant_timing_dto=update_dto
        )
