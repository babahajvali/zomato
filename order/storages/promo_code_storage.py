from typing import List

from order.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)
from order.interactors.dtos import CreatePromoCodeDTO, PromoCodeDTO
from order.models import PromoCode


class PromoCodeStorage(PromoCodeStorageInterface):
    @staticmethod
    def _convert_to_promo_code_dto(promo_code_obj: PromoCode) -> PromoCodeDTO:
        return PromoCodeDTO(
            promo_code_id=promo_code_obj.pk,
            code=promo_code_obj.code,
            discount_type=promo_code_obj.discount_type,
            discount_value=float(promo_code_obj.discount_value),
            min_order_value=float(promo_code_obj.min_order_value),
            max_usage=promo_code_obj.max_usage,
            valid_from=promo_code_obj.valid_from,
            valid_until=promo_code_obj.valid_until,
        )

    def create_bulk_promo_codes(self, promo_codes_dto: List[CreatePromoCodeDTO]):
        promo_codes = [
            PromoCode(
                code=dto.code,
                discount_type=dto.discount_type,
                discount_value=dto.discount_value,
                min_order_value=dto.min_order_value,
                max_usage=dto.max_usage,
                valid_from=dto.valid_from,
                valid_until=dto.valid_until,
            )
            for dto in promo_codes_dto
        ]

        created_promo_codes = PromoCode.objects.bulk_create(promo_codes)

        return created_promo_codes

    def get_existing_codes(self, codes: List[str]) -> List[str]:
        return list(
            PromoCode.objects.filter(code__in=codes).values_list("code", flat=True)
        )

    def get_promo_code_by_id(self, promo_code_id: int) -> PromoCodeDTO | None:
        promo_code_obj = PromoCode.objects.filter(id=promo_code_id).first()

        if promo_code_obj is None:
            return None

        return self._convert_to_promo_code_dto(promo_code_obj=promo_code_obj)
