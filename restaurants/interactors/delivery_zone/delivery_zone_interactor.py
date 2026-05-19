from typing import List, Optional, Tuple

from restaurants.exception.custom_exceptions import DuplicateDeliveryZones
from restaurants.interactors.dtos import (
    CreateDeliveryZoneDTO,
    DeliveryZoneDTO,
    UpdateDeliveryZoneDTO,
)
from restaurants.interactors.storage_interface.delivery_zone_storage_interface import (
    DeliveryZoneStorageInterface,
)


class DeliveryZoneInteractor:
    def __init__(self, delivery_zone_storage: DeliveryZoneStorageInterface):
        self.delivery_zone_storage = delivery_zone_storage

    def get_delivery_zone_by_restaurant_and_pin_code(
        self, restaurant_id: str, pin_code: str
    ) -> Optional[DeliveryZoneDTO]:

        return self.delivery_zone_storage.get_restaurant_delivery_zones(
            restaurant_id=restaurant_id, pin_code=pin_code
        )

    def create_or_update_delivery_zones(
        self, delivery_zone_dtos: List[CreateDeliveryZoneDTO]
    ) -> str:
        combinations = [
            (zone.restaurant_id, zone.pin_code) for zone in delivery_zone_dtos
        ]
        self._validate_duplicate_combinations(combinations=combinations)

        to_create, to_update = self._split_new_and_existing(
            delivery_zone_dtos=delivery_zone_dtos,
            combinations=combinations,
        )

        created_delivery_zones = (
            self.delivery_zone_storage.create_bulk_delivery_zones(to_create)
            if to_create
            else []
        )
        updated_delivery_zones = (
            self.delivery_zone_storage.update_bulk_delivery_zones(to_update)
            if to_update
            else []
        )

        return (
            f"{len(created_delivery_zones)} delivery zones created, "
            f"{len(updated_delivery_zones)} delivery zones updated"
        )

    def _split_new_and_existing(
        self,
        delivery_zone_dtos: List[CreateDeliveryZoneDTO],
        combinations: List[Tuple[str, str]],
    ) -> tuple[List[CreateDeliveryZoneDTO], List[UpdateDeliveryZoneDTO]]:
        existing = self.delivery_zone_storage.get_existing_delivery_zone_dtos(
            combinations
        )

        existing_lookup = {
            (zone.restaurant_id, zone.pin_code): zone.delivery_zone_id
            for zone in existing
        }

        to_create = []
        to_update = []

        for dto in delivery_zone_dtos:
            key = (dto.restaurant_id, dto.pin_code)
            if key in existing_lookup:
                to_update.append(
                    UpdateDeliveryZoneDTO(
                        delivery_zone_id=existing_lookup[key],
                        restaurant_id=dto.restaurant_id,
                        pin_code=dto.pin_code,
                        delivery_fee=dto.delivery_fee,
                        estimated_delivery_mins=dto.estimated_delivery_mins,
                    )
                )
            else:
                to_create.append(dto)

        return to_create, to_update

    @staticmethod
    def _validate_duplicate_combinations(combinations: List[Tuple[str, str]]):
        seen = set()
        duplicates = []

        for combo in combinations:
            if combo in seen:
                duplicates.append(combo)
            seen.add(combo)

        if duplicates:
            raise DuplicateDeliveryZones(combinations=duplicates)
