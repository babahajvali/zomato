from unittest.mock import create_autospec

from restaurants.interactors.delivery_zone.delivery_zone_interactor import (
    DeliveryZoneInteractor,
)
from restaurants.interactors.storage_interface.delivery_zone_storage_interface import (
    DeliveryZoneStorageInterface,
)
from restaurants.tests.factories.interactor_factories import DeliveryZoneDTOFactory


class TestDeliveryZoneInteractor:
    def setup_method(self):
        self.delivery_zone_storage = create_autospec(DeliveryZoneStorageInterface)
        self.interactor = DeliveryZoneInteractor(
            delivery_zone_storage=self.delivery_zone_storage
        )

    def test_get_delivery_zone_by_restaurant_and_pin_code_success(self):
        delivery_zone = DeliveryZoneDTOFactory(
            restaurant_id="restaurant-1",
            pin_code="500001",
            delivery_fee=40.0,
            estimated_delivery_mins=25,
        )
        self.delivery_zone_storage.get_restaurant_delivery_zones.return_value = (
            delivery_zone
        )

        result = self.interactor.get_delivery_zone_by_restaurant_and_pin_code(
            restaurant_id="restaurant-1",
            pin_code="500001",
        )

        assert result == delivery_zone
        self.delivery_zone_storage.get_restaurant_delivery_zones.assert_called_once_with(
            restaurant_id="restaurant-1",
            pin_code="500001",
        )

    def test_get_delivery_zone_by_restaurant_and_pin_code_returns_none(self):
        self.delivery_zone_storage.get_restaurant_delivery_zones.return_value = None

        result = self.interactor.get_delivery_zone_by_restaurant_and_pin_code(
            restaurant_id="restaurant-1",
            pin_code="999999",
        )

        assert result is None
        self.delivery_zone_storage.get_restaurant_delivery_zones.assert_called_once_with(
            restaurant_id="restaurant-1",
            pin_code="999999",
        )
