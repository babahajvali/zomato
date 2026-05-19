from decimal import Decimal
from typing import List, Any, Dict

from django.db import transaction  # noqa: F401
from django.utils.dateparse import parse_datetime

from orders.interactors.dtos import CreatePromoCodeDTO
from orders.interactors.promo_code.promo_code_interactor import PromoCodeInteractor
from orders.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)
from utils.read_csv_util import read_csv, validate_row


class ImportPromoCodes:
    def __init__(self, promo_code_storage: PromoCodeStorageInterface):
        self.promo_code_storage = promo_code_storage

    def import_promo_codes(self, file_path="./sample_data/promo_codes.csv"):
        rows = list(read_csv(file_path=file_path))

        self._validate_rows(rows=rows)

        promo_codes_dto = self._build_promo_code_dtos(rows=rows)

        interactor = PromoCodeInteractor(promo_code_storage=self.promo_code_storage)

        return interactor.create_or_update_promo_codes(promo_code_dtos=promo_codes_dto)

    @staticmethod
    def _build_promo_code_dtos(rows: List[Dict[str, Any]]) -> List[CreatePromoCodeDTO]:
        return [
            CreatePromoCodeDTO(
                code=row["code"],
                discount_type=row["discount_type"],
                discount_value=Decimal(row["discount_value"]),
                min_order_value=Decimal(row["min_order_value"]),
                max_usage=int(row["max_usage"]),
                valid_from=parse_datetime(row["valid_from"]),
                valid_until=parse_datetime(row["valid_until"]),
            )
            for row in rows
        ]

    @staticmethod
    def _validate_rows(rows: List[Dict[str, Any]]) -> None:
        for index, row in enumerate(rows, start=1):
            validate_row(
                row,
                [
                    "code",
                    "discount_type",
                    "discount_value",
                    "min_order_value",
                    "max_usage",
                    "valid_from",
                    "valid_until",
                ],
                f"promo code row {index}",
            )

            row["code"] = row["code"].strip()
            row["discount_type"] = row["discount_type"].strip()
            row["discount_value"] = row["discount_value"].strip()
            row["min_order_value"] = row["min_order_value"].strip()
            row["max_usage"] = row["max_usage"].strip()
            row["valid_from"] = row["valid_from"].strip()
            row["valid_until"] = row["valid_until"].strip()

    @staticmethod
    def _validate_empty_promo_codes(promo_codes: List[str]):
        return PromoCodeInteractor._validate_empty_promo_codes(promo_codes=promo_codes)
