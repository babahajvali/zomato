from typing import List, Any, Dict

from django.utils.dateparse import parse_datetime

from order.exception.custom_exceptions import (
    AlreadyExistsPromoCode,
    DuplicatePromoCodes, EmptyPromoCodeFound, InvalidPromoCodeDateRange,
)
from order.interactors.dtos import CreatePromoCodeDTO
from order.interactors.storage_interface.promo_code_storage_interface import \
    PromoCodeStorageInterface
from utils.read_csv_util import read_csv


class ImportPromoCodes:

    def __init__(self,
                 promo_code_storage: PromoCodeStorageInterface):
        self.promo_code_storage = promo_code_storage

    def import_promo_codes(self, file_path="./sample_data/promo_codes.csv"):
        rows = read_csv(file_path=file_path)

        codes = self._validate_promo_date_ranges(rows=rows)
        self._check_empty_promo_codes(codes)
        self._check_duplicate_codes(codes)
        self._check_existing_codes(codes)
            

        promo_codes_dto = [CreatePromoCodeDTO(
            code=row['code'],
            discount_type=row['discount_type'],
            discount_value=float(row['discount_value']),
            min_order_value=float(row['min_order_value']),
            max_usage=int(row['max_usage']),
            valid_from=row.get('valid_from'),
            valid_until=row.get('valid_until')
        )
            for row in rows]

        created_promos = self.promo_code_storage.create_bulk_promo_codes(
            promo_codes_dto)

        return f"imported {len(created_promos)} promo codes"

    def _check_existing_codes(self, codes: List[str]):
        existing_codes = self.promo_code_storage.get_existing_codes(
            codes)

        if existing_codes:
            raise AlreadyExistsPromoCode(codes=existing_codes)

    @staticmethod
    def _check_duplicate_codes(codes: List[str]):
        seen = set()
        duplicates = []

        for code in codes:
            if code in seen:
                duplicates.append(code)
            seen.add(code)

        if duplicates:
            raise DuplicatePromoCodes(codes=duplicates)

    @staticmethod
    def _check_empty_promo_codes(promo_codes: List[str]):
        empty_promo_codes = [1 for each_promo in promo_codes if not each_promo]

        if empty_promo_codes:
            raise EmptyPromoCodeFound(
                message=f"{len(empty_promo_codes)} Empty promo codes found")

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
                invalid_codes.append(f"Missing valid_from or valid_until in row {index} (code: {code})")
                continue

            parsed_valid_from = parse_datetime(valid_from)
            parsed_valid_until = parse_datetime(valid_until)

            if not parsed_valid_from or not parsed_valid_until:
                invalid_codes.append(f"Invalid date format in row {index} (code: {code})")
                continue

            if parsed_valid_until <= parsed_valid_from:
                    invalid_codes.append(
                        f"valid_until should be greater than valid_from "
                        f"in row {index} (code: {code})")

        if invalid_codes:
            raise InvalidPromoCodeDateRange(
                message="; ".join(invalid_codes)
            )


        return codes
