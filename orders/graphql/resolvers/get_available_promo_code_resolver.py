from orders.graphql.types.types import PromoCodeType, PromoCodesType
from orders.interactors.promo_code.promo_code_interactor import PromoCodeInteractor
from orders.storages.promo_code_storage import PromoCodeStorage


def get_available_promo_code_resolver(root, info):
    promo_code_storage = PromoCodeStorage()

    interactor = PromoCodeInteractor(promo_code_storage=promo_code_storage)

    result = interactor.get_available_promo_codes()
    promo_codes = [
        PromoCodeType(
            promo_code_id=each.promo_code_id,
            code=each.code,
            discount_type=each.discount_type,
            discount_value=each.discount_value,
            min_order_value=each.min_order_value,
            max_usage=each.max_usage,
            valid_from=each.valid_from,
            valid_until=each.valid_until,
        )
        for each in result
    ]

    return PromoCodesType(promo_codes=promo_codes)
