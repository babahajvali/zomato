from typing import List

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
                 promo_code_storage_interface: PromoCodeStorageInterface):
        self.promo_code_storage_interface = promo_code_storage_interface

    def import_promo_codes(self, file_path="./sample_data/promo_codes.csv"):
        rows = read_csv(file_path=file_path)

        codes = []

        for index, row in enumerate(rows, start=1):
            self._validate_date_range(
                valid_from=row.get('valid_from'),
                valid_until=row.get('valid_until'),
                code=row['code'],
            )
            codes.append(row['code'])

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

        return self.promo_code_storage_interface.create_bulk_promo_codes(
            promo_codes_dto)

    def _check_existing_codes(self, codes: List[str]):
        existing_codes = self.promo_code_storage_interface.get_existing_codes(
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
    def check_empty_promo_codes(promo_codes: List[str]):
        empty_promo_codes = [1 for each_promo in promo_codes if not each_promo]

        if empty_promo_codes:
            raise EmptyPromoCodeFound(
                message=f"{len(empty_promo_codes)} Empty promo codes found")

    @staticmethod
    def _validate_date_range(valid_from, valid_until, code):
        if not valid_from or not valid_until:
            return

        parsed_valid_from = parse_datetime(valid_from)
        parsed_valid_until = parse_datetime(valid_until)

        if not parsed_valid_from or not parsed_valid_until:
            return

        if parsed_valid_until <= parsed_valid_from:
            raise InvalidPromoCodeDateRange(
                message=(
                    f"valid_until should be greater than valid_from in row "
                    f"{code}"
                )
            )
