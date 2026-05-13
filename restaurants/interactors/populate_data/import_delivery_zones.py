from typing import List, Tuple

from restaurants.exception.custom_exceptions import DuplicateDeliveryZones
from restaurants.interactors.dtos import CreateDeliveryZoneDTO, UpdateDeliveryZoneDTO
from restaurants.interactors.storage_interface.delivery_zone_storage_interface import (
    DeliveryZoneStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportDeliveryZones:
    def __init__(self, delivery_zone_storage_interface: DeliveryZoneStorageInterface):
        self.delivery_zone_storage_interface = delivery_zone_storage_interface

    def import_delivery_zones(self, file_path="./sample_data/delivery_zones.csv"):
        rows = read_csv(file_path=file_path)

        combinations = self._parse_and_normalize_rows(rows)

        self._validate_duplicate_combinations(combinations)

        delivery_zones_dto = self._build_delivery_zone_dtos(rows)
        to_create, to_update = self._split_new_and_existing(
            delivery_zone_dtos=delivery_zones_dto,
            combinations=combinations,
        )

        created_delivery_zones = (
            self.delivery_zone_storage_interface.create_bulk_delivery_zones(to_create)
            if to_create
            else []
        )
        updated_delivery_zones = (
            self.delivery_zone_storage_interface.update_bulk_delivery_zones(to_update)
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
        existing = self.delivery_zone_storage_interface.get_existing_delivery_zone_dtos(
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

    @staticmethod
    def _parse_and_normalize_rows(rows) -> List[Tuple[str, str]]:
        combinations = []
        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                ["restaurant", "pin_code", "delivery_fee", "estimated_delivery_mins"],
                f"delivery zone row {index}",
            )
            row["restaurant"] = row["restaurant"].strip()
            row["pin_code"] = row["pin_code"].strip()
            row["delivery_fee"] = float(row["delivery_fee"])
            row["estimated_delivery_mins"] = int(row["estimated_delivery_mins"])
            combinations.append((row["restaurant"], row["pin_code"]))
        return combinations

    @staticmethod
    def _build_delivery_zone_dtos(rows) -> List[CreateDeliveryZoneDTO]:
        return [
            CreateDeliveryZoneDTO(
                restaurant_id=row["restaurant"],
                pin_code=row["pin_code"],
                delivery_fee=row["delivery_fee"],
                estimated_delivery_mins=row["estimated_delivery_mins"],
            )
            for row in rows
        ]
