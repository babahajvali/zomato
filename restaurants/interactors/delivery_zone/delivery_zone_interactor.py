from restaurants.interactors.dtos import DeliveryZoneDTO
from restaurants.interactors.storage_interface.delivery_zone_storage_interface import (
    DeliveryZoneStorageInterface,
)


class DeliveryZoneInteractor:
    def __init__(self, delivery_zone_storage: DeliveryZoneStorageInterface):
        self.delivery_zone_storage = delivery_zone_storage

    def get_delivery_zone_by_restaurant_and_pin_code(
        self, restaurant_id: str, pin_code: str
    ) -> DeliveryZoneDTO:

        return self.delivery_zone_storage.get_restaurant_delivery_zones(
            restaurant_id=restaurant_id, pin_code=pin_code
        )
