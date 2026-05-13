from decimal import Decimal
from typing import List, Optional

from django.utils import timezone

from orders.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)
from orders.interactors.dtos import (
    CreatePromoCodeDTO,
    PromoCodeDTO,
    UpdatePromoCodeDTO,
)
from orders.models import PromoCode


class PromoCodeStorage(PromoCodeStorageInterface):
    @staticmethod
    def _convert_to_promo_code_dto(promo_code_obj: PromoCode) -> PromoCodeDTO:
        return PromoCodeDTO(
            promo_code_id=promo_code_obj.pk,
            code=promo_code_obj.code,
            discount_type=promo_code_obj.discount_type,
            discount_value=Decimal(promo_code_obj.discount_value),
            min_order_value=Decimal(promo_code_obj.min_order_value),
            max_usage=promo_code_obj.max_usage,
            valid_from=promo_code_obj.valid_from,
            valid_until=promo_code_obj.valid_until,
        )

    def create_bulk_promo_codes(self, promo_code_dtos: List[CreatePromoCodeDTO]):
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
            for dto in promo_code_dtos
        ]

        created_promo_codes = PromoCode.objects.bulk_create(promo_codes)

        return created_promo_codes

    def update_bulk_promo_codes(
        self, promo_code_dtos: List[UpdatePromoCodeDTO]
    ) -> List[PromoCode]:
        promo_codes = [
            PromoCode(
                id=dto.promo_code_id,
                code=dto.code,
                discount_type=dto.discount_type,
                discount_value=dto.discount_value,
                min_order_value=dto.min_order_value,
                max_usage=dto.max_usage,
                valid_from=dto.valid_from,
                valid_until=dto.valid_until,
            )
            for dto in promo_code_dtos
        ]

        PromoCode.objects.bulk_update(
            promo_codes,
            [
                "code",
                "discount_type",
                "discount_value",
                "min_order_value",
                "max_usage",
                "valid_from",
                "valid_until",
            ],
        )

        return promo_codes

    def get_existing_codes(self, codes: List[str]) -> List[str]:
        return list(
            PromoCode.objects.filter(code__in=codes).values_list("code", flat=True)
        )

    def get_existing_promo_codes(self, codes: List[str]) -> List[PromoCodeDTO]:
        promo_code_objs = PromoCode.objects.filter(code__in=codes)

        return [
            self._convert_to_promo_code_dto(promo_code_obj=each)
            for each in promo_code_objs
        ]

    def get_promo_code_by_id(self, promo_code_id: int) -> Optional[PromoCodeDTO]:
        promo_code_obj = PromoCode.objects.filter(id=promo_code_id).first()
        if promo_code_obj is None:
            return None

        return self._convert_to_promo_code_dto(promo_code_obj=promo_code_obj)

    def get_available_promo_codes(self) -> List[PromoCodeDTO]:
        now = timezone.now()

        promo_code_objs = PromoCode.objects.filter(
            valid_from__lte=now, valid_until__gte=now
        )

        return [
            self._convert_to_promo_code_dto(promo_code_obj=each)
            for each in promo_code_objs
        ]
