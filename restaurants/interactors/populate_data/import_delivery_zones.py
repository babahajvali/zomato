from typing import List, Tuple

from restaurants.exception.custom_exceptions import DuplicateDeliveryZones
from restaurants.interactors.dtos import CreateDeliveryZoneDTO
from restaurants.interactors.storage_interface.delivery_zone_storage_interface import (
    DeliveryZoneStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportDeliveryZones:
    def __init__(self, delivery_zone_storage_interface: DeliveryZoneStorageInterface):
        self.delivery_zone_storage_interface = delivery_zone_storage_interface

    def import_delivery_zones(self, file_path="./sample_data/delivery_zones.csv"):
        rows = read_csv(file_path=file_path)

        combinations = []

        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                ["restaurant", "pin_code", "delivery_fee", "estimated_delivery_mins"],
                f"delivery zone row {index}",
            )

            restaurant_id = row["restaurant"].strip()
            pin_code = row["pin_code"].strip()

            row["restaurant"] = restaurant_id
            row["pin_code"] = pin_code
            row["delivery_fee"] = float(row["delivery_fee"])
            row["estimated_delivery_mins"] = int(row["estimated_delivery_mins"])

            combinations.append((restaurant_id, pin_code))

        self._validate_duplicate_combinations(combinations)
        self._validate_existing_delivery_zones(combinations)

        delivery_zones_dto = [
            CreateDeliveryZoneDTO(
                restaurant_id=row["restaurant"],
                pin_code=row["pin_code"],
                delivery_fee=row["delivery_fee"],
                estimated_delivery_mins=row["estimated_delivery_mins"],
            )
            for row in rows
        ]

        created_delivery_zones = (
            self.delivery_zone_storage_interface.create_bulk_delivery_zones(
                delivery_zones_dto
            )
        )

        return f"{len(created_delivery_zones)} delivery zones created"

    def _validate_existing_delivery_zones(self, combinations: List[Tuple[str, str]]):
        existing = self.delivery_zone_storage_interface.get_existing_delivery_zones(
            combinations
        )

        if existing:
            raise DuplicateDeliveryZones(combinations=existing)

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
