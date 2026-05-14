from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from restaurants.interactors.dtos import (
    CreateDeliveryZoneDTO,
    DeliveryZoneDTO,
    UpdateDeliveryZoneDTO,
)


class DeliveryZoneStorageInterface(ABC):
    @abstractmethod
    def create_bulk_delivery_zones(
        self, create_delivery_zones: List[CreateDeliveryZoneDTO]
    ) -> List[DeliveryZoneDTO]:
        pass

    @abstractmethod
    def update_bulk_delivery_zones(
        self, update_delivery_zones: List[UpdateDeliveryZoneDTO]
    ) -> List[DeliveryZoneDTO]:
        pass

    @abstractmethod
    def get_delivery_zone_by_id(
        self, delivery_zone_id: int
    ) -> Optional[DeliveryZoneDTO]:
        pass

    @abstractmethod
    def get_restaurant_delivery_zones(
        self, restaurant_id: str, pin_code: str
    ) -> Optional[DeliveryZoneDTO]:
        pass

    @abstractmethod
    def get_existing_delivery_zones(self, combinations: List[Tuple[str, str]]):
        pass

    @abstractmethod
    def get_existing_delivery_zone_dtos(
        self, combinations: List[Tuple[str, str]]
    ) -> List[DeliveryZoneDTO]:
        pass
