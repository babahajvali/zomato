from typing import List

from order.interactors.storage_interface.promo_code_storage_interface import PromoCodeStorageInterface
from order.interactors.dtos import CreatePromoCodeDTO
from order.models import PromoCode


class PromoCodeStorage(PromoCodeStorageInterface):

    def create_bulk_promo_codes(self, promo_codes_dto: List[CreatePromoCodeDTO]):
        promo_codes = [PromoCode(
            code=dto.code,
            discount_type=dto.discount_type,
            discount_value=dto.discount_value,
            min_order_value=dto.min_order_value,
            max_usage=dto.max_usage,
            valid_from=dto.valid_from,
            valid_until=dto.valid_until
        ) for dto in promo_codes_dto]

        created_promo_codes = PromoCode.objects.bulk_create(promo_codes)

        return created_promo_codes

    def get_existing_codes(self, codes: List[str]) -> List[str]:
        return list(PromoCode.objects.filter(code__in=codes)
                    .values_list('code', flat=True))
