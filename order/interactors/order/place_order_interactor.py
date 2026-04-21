from order.adapter.account import AccountAdapter
from order.adapter.restaurant import RestaurantAdapter
from order.constants.constants import Tax_percentage
from order.constants.enums import PromoCodeType
from order.exception.custom_exceptions import (
    PromoCodeMaximumUsed,
    PromoCodeNotEligible,
    InvalidDeliveryZoneFound,
    InvalidAddressFound,
)
from order.interactors.dtos import PlaceOrderDTO, OrderDTO
from order.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from order.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)
from order.mixin.promocode_mixin import PromoCodeMixin


class PlaceOrderInteractor(PromoCodeMixin):
    def __init__(
        self,
        promo_code_storage: PromoCodeStorageInterface,
        order_storage: OrderStorageInterface,
    ):
        super().__init__(promo_code_storage=promo_code_storage)
        self.promo_code_storage = promo_code_storage
        self.order_storage = order_storage
        self.account_adapter = AccountAdapter()
        self.restaurant_adapter = RestaurantAdapter()

    def place_order(self, order_data: PlaceOrderDTO) -> OrderDTO:
        self.validate_promo_code_exist(promo_code_id=order_data.promo_code_id)
        promo_code_dto = self.promo_code_storage.get_promo_code_by_id(
            promo_code_id=order_data.promo_code_id
        )
        self._validate_promo_code_available(
            promo_code_id=promo_code_dto.promo_code_id,
            max_usage_count=promo_code_dto.max_usage,
        )
        self._validate_promo_code_eligibility(
            items_total=order_data.items_total,
            min_order_value=promo_code_dto.min_order_value,
        )
        discount_price = self._calculate_discount_price(
            items_total=order_data.items_total,
            discount_type=promo_code_dto.discount_type,
            discount_value=promo_code_dto.discount_value,
        )
        tax_fee = self._calculate_tax_fee(
            items_total=order_data.items_total, discount_price=discount_price
        )

        delivery_fee = self._validate_address_and_get_delivery_fee(
            address_id=order_data.address_id, restaurant_id=order_data.restaurant_id
        )

    def _validate_promo_code_available(self, promo_code_id: int, max_usage_count: int):

        usage_count = self.order_storage.get_promo_code_usage(
            promo_code_id=promo_code_id
        )

        if usage_count >= max_usage_count:
            raise PromoCodeMaximumUsed(max_usage_count=usage_count)

    @staticmethod
    def _validate_promo_code_eligibility(items_total: float, min_order_value: float):

        if items_total < min_order_value:
            raise PromoCodeNotEligible(
                min_order_value=min_order_value, items_total=items_total
            )

    @staticmethod
    def _calculate_discount_price(
        items_total: float, discount_type: str, discount_value: float
    ) -> float:

        if discount_type == PromoCodeType.PERCENTAGE.value:
            return items_total * (discount_value / 100)

        return discount_value

    @staticmethod
    def _calculate_tax_fee(items_total: float, discount_price: float) -> float:
        return (items_total - discount_price) * (Tax_percentage / 100)

    def _validate_address_and_get_delivery_fee(
        self, address_id: int, restaurant_id: str
    ) -> float:

        pincode = self._validate_address_and_get_pincode(address_id=address_id)
        delivery_fee = self._validate_delivery_zone(
            restaurant_id=restaurant_id, pincode=pincode
        )

        return delivery_fee

    def _validate_delivery_zone(self, restaurant_id: str, pincode: str) -> float:
        zone_dto = self.restaurant_adapter.get_delivery_zone_by_restaurant_id(
            restaurant_id=restaurant_id, pin_code=pincode
        )

        if zone_dto is None:
            raise InvalidDeliveryZoneFound(
                restaurant_id=restaurant_id, pin_code=pincode
            )

        return zone_dto.delivery_fee

    def _validate_address_and_get_pincode(self, address_id: int) -> str:
        address_dto = self.account_adapter.get_address_by_id(address_id=address_id)
        if address_dto is None:
            raise InvalidAddressFound(address_id=address_id)

        return address_dto.pincode
