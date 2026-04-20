from datetime import time
from unittest import result

from django.test import TestCase

from restaurant.interactors.dtos import (
    CreateRestaurantTimingDTO,
    UpdateRestaurantTimingDTO,
)
from restaurant.storages.restaurant_timing_storage import \
    RestaurantTimingStorage
from restaurant.tests.factories.storage_factories import (
    RestaurantFactory,
    RestaurantTimingFactory,
)


class TestRestaurantTimingStorage(TestCase):
    def setUp(self):
        self.storage = RestaurantTimingStorage()

    def test_create_bulk_restaurant_timing_success(self):
        restaurant = RestaurantFactory()
        create_dto = [
            CreateRestaurantTimingDTO(
                restaurant_id=restaurant.id,
                day_of_week=1,
                open_time=time(9, 0),
                close_time=time(21, 0),
            )
        ]

        result = self.storage.create_bulk_restaurant_timing(
            create_restaurant_timing_dto=create_dto
        )

        assert len(result) == 1
        assert result[0].restaurant_id == restaurant.id
        assert result[0].day_of_week == 1
        assert result[0].open_time == time(9, 0)
        assert result[0].close_time == time(21, 0)

    def test_get_restaurant_timing_success(self):
        timing = RestaurantTimingFactory(
            day_of_week=2,
            open_time=time(10, 0),
            close_time=time(20, 0),
        )

        result = self.storage.get_restaurant_timing(timing_id=timing.id)

        assert result is not None
        assert result.timing_id == timing.id
        assert result.day_of_week == 2
        assert result.open_time == time(10, 0)
        assert result.close_time == time(20, 0)

    def test_get_restaurant_timing_not_found(self):
        result = self.storage.get_restaurant_timing(timing_id=99999)

        assert result is None

    def test_update_restaurant_timing_success(self):
        timing = RestaurantTimingFactory(
            open_time=time(9, 0),
            close_time=time(21, 0),
        )
        update_dto = UpdateRestaurantTimingDTO(
            timing_id=timing.id,
            user_id=str(timing.restaurant.owner_id),
            open_time=time(11, 0),
            close_time=time(22, 0),
        )

        result = self.storage.update_restaurant_timing(
            update_restaurant_timing_dto=update_dto
        )

        assert result.open_time == time(11, 0)
        assert result.close_time == time(22, 0)

    def test_get_restaurant_owner_id(self):
        timing = RestaurantTimingFactory()

        result = self.storage.get_restaurant_owner_id(id=timing.id)

        assert result == str(timing.restaurant.owner_id)

    def test_delete_restaurant_timing_success(self):
        id = 1
        RestaurantTimingFactory(id=id)

        self.storage.delete_restaurant_timing(id=id)

        from restaurant.models import RestaurantTiming

        assert not RestaurantTiming.objects.filter(id=id).exists()

    def test_get_restaurant_timings_success(self):
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id)
        RestaurantTimingFactory.create_batch(
            3, restaurant_id=restaurant_id)

        result = self.storage.get_restaurant_timings(
            restaurant_id=restaurant_id)

        assert len(result) == 3
