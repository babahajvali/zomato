from typing import List, Tuple

from django.db.models import Q

from restaurants.interactors.dtos import CreateDeliveryZoneDTO, DeliveryZoneDTO
from restaurants.interactors.storage_interface.delivery_zone_storage_interface import (
    DeliveryZoneStorageInterface,
)
from restaurants.models import DeliveryZone


class DeliveryZoneStorage(DeliveryZoneStorageInterface):
    @staticmethod
    def _convert_to_delivery_zone_dto(zone_obj: DeliveryZone) -> DeliveryZoneDTO:
        return DeliveryZoneDTO(
            delivery_zone_id=zone_obj.pk,
            restaurant_id=zone_obj.restaurant_id,
            pin_code=zone_obj.pin_code,
            delivery_fee=float(zone_obj.delivery_fee),
            estimated_delivery_mins=zone_obj.estimated_delivery_mins,
        )

    def create_bulk_delivery_zones(
        self, create_delivery_zones: List[CreateDeliveryZoneDTO]
    ) -> List[DeliveryZoneDTO]:
        delivery_zone_objs = [
            DeliveryZone(
                restaurant_id=dto.restaurant_id,
                pin_code=dto.pin_code,
                delivery_fee=dto.delivery_fee,
                estimated_delivery_mins=dto.estimated_delivery_mins,
            )
            for dto in create_delivery_zones
        ]

        created_objs = DeliveryZone.objects.bulk_create(delivery_zone_objs)

        return [
            self._convert_to_delivery_zone_dto(zone_obj=each) for each in created_objs
        ]

    def get_delivery_zone_by_id(self, delivery_zone_id: int) -> DeliveryZoneDTO | None:
        delivery_zone_obj = DeliveryZone.objects.filter(id=delivery_zone_id).first()

        if delivery_zone_obj is None:
            return None

        return self._convert_to_delivery_zone_dto(zone_obj=delivery_zone_obj)

    def get_restaurant_delivery_zones(
        self, restaurant_id: str, pin_code: str
    ) -> DeliveryZoneDTO | None:
        zone_obj = DeliveryZone.objects.filter(
            restaurant_id=restaurant_id, pin_code=pin_code
        ).first()

        if zone_obj is None:
            return None

        return self._convert_to_delivery_zone_dto(zone_obj=zone_obj)

    def get_existing_delivery_zones(self, combinations: List[Tuple[str, str]]):
        if not combinations:
            return []

        query_filter = Q()
        for r, p in combinations:
            query_filter |= Q(restaurant_id=r, pin_code=p)

        existing_zones = DeliveryZone.objects.filter(query_filter).values_list(
            "restaurant_id", "pin_code"
        )

        existing_set = set(existing_zones)

        return [
            (restaurant_id, pin_code)
            for restaurant_id, pin_code in combinations
            if (restaurant_id, pin_code) in existing_set
        ]
