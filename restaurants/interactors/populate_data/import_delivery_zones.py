from decimal import Decimal
from typing import List

from restaurants.interactors.delivery_zone.delivery_zone_interactor import (
    DeliveryZoneInteractor,
)
from restaurants.interactors.dtos import CreateDeliveryZoneDTO
from restaurants.interactors.storage_interface.delivery_zone_storage_interface import (
    DeliveryZoneStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportDeliveryZones:
    def __init__(self, delivery_zone_storage_interface: DeliveryZoneStorageInterface):
        self.delivery_zone_storage_interface = delivery_zone_storage_interface

    def import_delivery_zones(self, file_path="./sample_data/delivery_zones.csv"):
        rows = list(read_csv(file_path=file_path))

        self._validate_rows(rows)

        delivery_zones_dto = self._build_delivery_zone_dtos(rows)

        interactor = DeliveryZoneInteractor(
            delivery_zone_storage=self.delivery_zone_storage_interface
        )

        return interactor.create_or_update_delivery_zones(
            delivery_zone_dtos=delivery_zones_dto
        )

    @staticmethod
    def _validate_rows(rows):
        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                ["restaurant", "pin_code", "delivery_fee", "estimated_delivery_mins"],
                f"delivery zone row {index}",
            )
            row["restaurant"] = row["restaurant"].strip()
            row["pin_code"] = row["pin_code"].strip()
            row["delivery_fee"] = Decimal(row["delivery_fee"])
            row["estimated_delivery_mins"] = int(row["estimated_delivery_mins"])

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
