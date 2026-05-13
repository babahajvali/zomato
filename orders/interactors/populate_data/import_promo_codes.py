from decimal import Decimal
from typing import List, Any, Dict

from django.db import transaction
from django.utils.dateparse import parse_datetime

from orders.exception.custom_exceptions import (
    DuplicatePromoCodes,
    EmptyPromoCode,
    InvalidPromoCodeDateRange,
)
from orders.interactors.dtos import CreatePromoCodeDTO, UpdatePromoCodeDTO
from orders.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)
from utils.read_csv_util import read_csv


class ImportPromoCodes:
    def __init__(self, promo_code_storage: PromoCodeStorageInterface):
        self.promo_code_storage = promo_code_storage

    def import_promo_codes(self, file_path="./sample_data/promo_codes.csv"):
        rows = read_csv(file_path=file_path)

        codes = self._validate_promo_date_ranges(rows=rows)
        self._validate_empty_promo_codes(codes)
        self._validate_duplicate_codes(codes)

        promo_codes_dto = self._build_promo_code_dtos(rows=rows)

        to_create, to_update = self._split_new_and_existing(
            promo_code_dtos=promo_codes_dto,
            codes=codes,
        )
        with transaction.atomic():
            created_promos = (
                self.promo_code_storage.create_bulk_promo_codes(to_create)
                if to_create
                else []
            )
            updated_promos = (
                self.promo_code_storage.update_bulk_promo_codes(to_update)
                if to_update
                else []
            )

        return (
            f"{len(created_promos)} promo codes created, "
            f"{len(updated_promos)} promo codes updated"
        )

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

    def _split_new_and_existing(
        self,
        promo_code_dtos: List[CreatePromoCodeDTO],
        codes: List[str],
    ) -> tuple[List[CreatePromoCodeDTO], List[UpdatePromoCodeDTO]]:
        existing_promo_codes = self.promo_code_storage.get_existing_promo_codes(codes)

        existing_lookup = {
            promo_code.code: promo_code.promo_code_id
            for promo_code in existing_promo_codes
        }

        to_create = []
        to_update = []

        for dto in promo_code_dtos:
            if dto.code in existing_lookup:
                to_update.append(
                    UpdatePromoCodeDTO(
                        promo_code_id=existing_lookup[dto.code],
                        code=dto.code,
                        discount_type=dto.discount_type,
                        discount_value=dto.discount_value,
                        min_order_value=dto.min_order_value,
                        max_usage=dto.max_usage,
                        valid_from=dto.valid_from,
                        valid_until=dto.valid_until,
                    )
                )
            else:
                to_create.append(dto)

        return to_create, to_update

    @staticmethod
    def _validate_duplicate_codes(codes: List[str]):
        seen = set()
        duplicates = []

        for code in codes:
            if code in seen:
                duplicates.append(code)
            seen.add(code)

        if duplicates:
            raise DuplicatePromoCodes(codes=duplicates)

    @staticmethod
    def _validate_empty_promo_codes(promo_codes: List[str]):
        empty_promo_codes = [1 for each_promo in promo_codes if not each_promo]

        if empty_promo_codes:
            raise EmptyPromoCode(
                message=f"{len(empty_promo_codes)} Empty promo codes found"
            )

    @staticmethod
    def _validate_promo_date_ranges(rows: List[Dict[str, Any]]) -> List[str]:
        codes = []
        invalid_codes = []

        for index, row in enumerate(rows, start=1):
            valid_from = row.get("valid_from")
            valid_until = row.get("valid_until")
            code = row.get("code")

            codes.append(code)

            if not valid_from or not valid_until:
                invalid_codes.append(
                    f"Missing valid_from or valid_until in row {index} (code: {code})"
                )
                continue

            parsed_valid_from = parse_datetime(valid_from)
            parsed_valid_until = parse_datetime(valid_until)

            if not parsed_valid_from or not parsed_valid_until:
                invalid_codes.append(
                    f"Invalid date format in row {index} (code: {code})"
                )
                continue

            if parsed_valid_until <= parsed_valid_from:
                invalid_codes.append(
                    f"valid_until should be greater than valid_from "
                    f"in row {index} (code: {code})"
                )

        if invalid_codes:
            raise InvalidPromoCodeDateRange(message="; ".join(invalid_codes))
        return codes
