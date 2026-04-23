from unittest.mock import create_autospec

import pytest

from accounts.tests.factories.interactor_factories import UserDTOFactory
from restaurants.exception.custom_exceptions import (
    RestaurantTimingNotFound,
    UserIsNotRestaurantOwner,
    RestaurantNotFound,
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
from restaurants.tests.factories.interactor_factories import (
    RestaurantTimingDTOFactory,
    RestaurantDTOFactory,
)


class TestDeleteRestaurantTiming:
    def setup_method(self):
        self.restaurant_timing_storage = create_autospec(
            RestaurantTimingStorageInterface
        )
        self.restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.interactor = RestaurantTimingInteractor(
            restaurant_timing_storage=self.restaurant_timing_storage,
            restaurant_storage=self.restaurant_storage,
        )

    def test_delete_restaurant_timing_successful(self):
        id = 1
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        UserDTOFactory.create(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantDTOFactory(id=restaurant_id, owner_id=user_id)

        RestaurantTimingDTOFactory(timing_id=id, restaurant_id=restaurant_id)
        self.restaurant_timing_storage.get_restaurant_owner_id.return_value = user_id
        self.interactor.delete_restaurant_timing(timing_id=id, user_id=user_id)

        self.restaurant_timing_storage.delete_restaurant_timing.assert_called_once_with(
            timing_id=id
        )

    def test_restaurant_timing_not_exists(self):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        id = 2
        self.restaurant_timing_storage.get_restaurant_timing.return_value = None
        with pytest.raises(RestaurantTimingNotFound) as e:
            self.interactor.delete_restaurant_timing(timing_id=id, user_id=user_id)

        assert e.value.id == id

    def test_user_is_not_restaurant_owner(self):
        id = 1
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        UserDTOFactory.create(id=user_id)

        with pytest.raises(UserIsNotRestaurantOwner) as e:
            self.interactor.delete_restaurant_timing(timing_id=id, user_id=user_id)

        assert e.value.user_id == user_id

    def test_get_restaurant_timings_successful(self):
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"

        timings = RestaurantTimingDTOFactory.create_batch(
            3, restaurant_id=restaurant_id
        )

        self.restaurant_storage.check_restaurant_is_exist.return_value = True
        self.restaurant_timing_storage.get_restaurant_timings.return_value = timings

        result = self.interactor.get_restaurant_timings(restaurant_id=restaurant_id)

        assert len(result) == 3

    def test_invalid_restaurant_found(self):
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        self.restaurant_storage.check_restaurant_is_exist.return_value = False

        with pytest.raises(RestaurantNotFound) as e:
            self.interactor.get_restaurant_timings(restaurant_id=restaurant_id)

        assert e.value.restaurant_id == restaurant_id
