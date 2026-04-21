from abc import ABC, abstractmethod
from typing import List

from restaurant.interactors.dtos import CreateDeliveryZoneDTO, DeliveryZoneDTO


class DeliveryZoneStorageInterface(ABC):
    @abstractmethod
    def create_bulk_delivery_zones(
        self, create_delivery_zones: List[CreateDeliveryZoneDTO]
    ) -> List[DeliveryZoneDTO]:
        pass

    @abstractmethod
    def get_delivery_zone_by_id(self, delivery_zone_id: int) -> DeliveryZoneDTO:
        pass

    @abstractmethod
    def get_restaurant_delivery_zones(
        self, restaurant_id: str, pin_code: str
    ) -> DeliveryZoneDTO:
        pass
