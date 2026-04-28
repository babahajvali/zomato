from datetime import time
from unittest.mock import create_autospec

import pytest

from restaurants.interactors.dtos import (
    CreateRestaurantTimingDTO,
    RestaurantTimingDTO,
)
from restaurants.interactors.restaurant_timing.restaurant_timing_interactor import (
    RestaurantTimingInteractor,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)

from restaurants.interactors.storage_interface.restaurant_timing_storage_interface import (
    RestaurantTimingStorageInterface,
)
from restaurants.exception.custom_exceptions import (
    RestaurantNotFound,
    UserIsNotRestaurantOwner,
    OpenTimeGreaterThanCloseTime,
)


class TestCreateRestaurantTimingInteractor:
    @staticmethod
    def _get_create_dto():
        return CreateRestaurantTimingDTO(
            restaurant_id="restaurant-1",
            day_of_week=1,
            open_time=time(9, 0),
            close_time=time(21, 0),
        )

    @staticmethod
    def _get_response_dto():
        return RestaurantTimingDTO(
            timing_id=1,
            restaurant_id="restaurant-1",
            day_of_week=1,
            open_time=time(9, 0),
            close_time=time(21, 0),
        )

    def setup_method(self):
        self.storage = create_autospec(RestaurantTimingStorageInterface)
        self.restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.interactor = RestaurantTimingInteractor(
            restaurant_timing_storage=self.storage,
            restaurant_storage=self.restaurant_storage,
        )

    def _setup_dependencies(
        self,
        *,
        restaurant_exists=True,
        owner_id="user-123",
        storage_response=None,
    ):
        self.restaurant_storage.check_restaurant_is_exist.return_value = (
            restaurant_exists
        )
        self.restaurant_storage.get_restaurant_owner_id.return_value = owner_id
        self.storage.create_bulk_restaurant_timing.return_value = (
            storage_response if storage_response else [self._get_response_dto()]
        )

    def test_create_restaurant_timing_success(self, snapshot):
        dto = self._get_create_dto()
        expected = [self._get_response_dto()]
        self._setup_dependencies(storage_response=expected)

        result = self.interactor.create_restaurant_timing(
            create_restaurant_timing_dto=dto,
            user_id="user-123",
        )

        snapshot.assert_match(
            repr(result),
            "create_restaurant_timing_success.txt",
        )

        self.storage.create_bulk_restaurant_timing.assert_called_once_with(
            create_restaurant_timing_dto=[dto]
        )

    def test_create_restaurant_timing_restaurant_not_found(self, snapshot):
        dto = self._get_create_dto()
        self._setup_dependencies(restaurant_exists=False)

        with pytest.raises(RestaurantNotFound) as exc:
            self.interactor.create_restaurant_timing(
                create_restaurant_timing_dto=dto,
                user_id="user-123",
            )

        snapshot.assert_match(
            repr(exc.value.restaurant_id),
            "create_restaurant_timing_restaurant_not_found.txt",
        )

        self.storage.get_restaurant_owner_id.assert_not_called()
        self.storage.create_bulk_restaurant_timing.assert_not_called()

    def test_create_restaurant_timing_user_not_owner(self, snapshot):
        dto = self._get_create_dto()
        self._setup_dependencies(owner_id="owner-456")

        with pytest.raises(UserIsNotRestaurantOwner) as exc:
            self.interactor.create_restaurant_timing(
                create_restaurant_timing_dto=dto,
                user_id="user-123",
            )

        snapshot.assert_match(
            repr(exc.value.user_id),
            "create_restaurant_timing_user_not_owner.txt",
        )

        self.storage.create_bulk_restaurant_timing.assert_not_called()

    def test_create_restaurant_timing_open_time_greater_than_close_time(self):
        dto = CreateRestaurantTimingDTO(
            restaurant_id="restaurant-1",
            day_of_week=1,
            open_time=time(22, 0),
            close_time=time(10, 0),
        )
        self._setup_dependencies()

        with pytest.raises(OpenTimeGreaterThanCloseTime) as exc:
            self.interactor.create_restaurant_timing(
                create_restaurant_timing_dto=dto,
                user_id="user-123",
            )

        assert str(exc.value) == "22:00:00 --> 10:00:00"
        self.storage.create_bulk_restaurant_timing.assert_not_called()
