from decimal import Decimal
from typing import List, Optional

from django.utils import timezone

from orders.adapter.account import AccountAdapter
from orders.adapter.dtos import CartItemDTO
from orders.adapter.restaurant import RestaurantAdapter
from orders.exception.custom_exceptions import (
    AddressNotFound,
    CartIsEmpty,
    CustomerCartNotFound,
    DeliveryUnavailableForAddress,
    MenuItemsUnavailable,
    PromoCodeExpired,
    PromoCodeNotEligible,
    PromoCodeNotYetValid,
    PromoCodeUsageLimitReached,
)
from orders.interactors.dtos import (
    CreateOrderItemDTO,
    PromoCodeDTO,
)
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)
from orders.mixin.order_mixin import OrderMixin
from orders.mixin.promocode_mixin import PromoCodeMixin


class OrderPlacementBase(PromoCodeMixin, OrderMixin):
    def __init__(
        self,
        promo_code_storage: PromoCodeStorageInterface,
        order_storage: OrderStorageInterface,
    ):
        super().__init__(
            promo_code_storage=promo_code_storage,
            order_storage=order_storage,
        )
        self.promo_code_storage = promo_code_storage
        self.order_storage = order_storage
        self.account_adapter = AccountAdapter()
        self.restaurant_adapter = RestaurantAdapter()

    def _validate_address_and_get_delivery_fee(
        self, address_id: int, restaurant_id: str, user_id: str
    ) -> Decimal:
        pincode = self._get_validated_pincode(address_id=address_id, user_id=user_id)
        return self._get_validated_delivery_fee(
            restaurant_id=restaurant_id,
            pincode=pincode,
        )

    def _get_validated_pincode(self, address_id: int, user_id: str) -> str:
        address_dto = self.account_adapter.get_address_by_id(
            address_id=address_id, user_id=user_id
        )
        if address_dto is None:
            raise AddressNotFound(address_id=address_id)
        return address_dto.pincode

    def _get_validated_delivery_fee(
        self,
        restaurant_id: str,
        pincode: str,
    ) -> Decimal:
        zone_dto = self.restaurant_adapter.get_delivery_zone_by_restaurant_id(
            restaurant_id=restaurant_id,
            pin_code=pincode,
        )
        if zone_dto is None:
            raise DeliveryUnavailableForAddress(
                restaurant_id=restaurant_id,
                pin_code=pincode,
            )
        return Decimal(str(zone_dto.delivery_fee))

    def _get_validated_cart_id(self, customer_id: str) -> str:
        cart_id = self.restaurant_adapter.get_customer_cart_id(customer_id=customer_id)
        if cart_id is None:
            raise CustomerCartNotFound(customer_id=customer_id)
        return cart_id

    def _get_validated_cart_items(self, cart_id: str) -> List[CartItemDTO]:
        cart_items = self.restaurant_adapter.get_customer_cart_items(cart_id=cart_id)
        if not cart_items:
            raise CartIsEmpty(cart_id=cart_id)
        return cart_items

    def _validate_items_available(self, cart_items: List[CartItemDTO]):
        item_ids = [item.menu_item_id for item in cart_items]
        unavailable = self.restaurant_adapter.get_unavailable_menu_items(
            menu_item_ids=item_ids
        )
        if unavailable:
            raise MenuItemsUnavailable(unavailable_item_ids=unavailable)

    def _validate_promo_code_existence_and_eligibility(
        self,
        promo_code_id: int,
        items_total: Decimal,
    ):
        self.validate_promo_code_exist(promo_code_id=promo_code_id)

        promo_code_dto = self.promo_code_storage.get_promo_code_by_id(
            promo_code_id=promo_code_id
        )
        self._validate_promo_code_expiry(promo_code_dto=promo_code_dto)

        if items_total < Decimal(str(promo_code_dto.min_order_value)):
            raise PromoCodeNotEligible(
                min_order_value=promo_code_dto.min_order_value,
                items_total=items_total,
            )

    @staticmethod
    def _validate_promo_code_expiry(promo_code_dto: PromoCodeDTO):
        now = timezone.now()
        if promo_code_dto.valid_from and now < promo_code_dto.valid_from:
            raise PromoCodeNotYetValid(code=promo_code_dto.code)
        if promo_code_dto.valid_until and now > promo_code_dto.valid_until:
            raise PromoCodeExpired(code=promo_code_dto.code)

    def _get_discount_price(
        self,
        promo_code_id: Optional[int],
        items_total: Decimal,
    ) -> Decimal:
        if not promo_code_id:
            return Decimal("0.00")

        promo_code_dto = self.promo_code_storage.get_promo_code_by_id(
            promo_code_id=promo_code_id
        )
        self._validate_promo_code_usage_limit(
            promo_code_id=promo_code_id,
            max_usage_count=promo_code_dto.max_usage,
        )
        if items_total >= promo_code_dto.min_order_value:
            return self.calculate_discount_price(
                items_total=items_total,
                discount_type=promo_code_dto.discount_type,
                discount_value=Decimal(str(promo_code_dto.discount_value)),
            )
        return Decimal("0.00")

    def _validate_promo_code_usage_limit(
        self,
        promo_code_id: int,
        max_usage_count: int,
    ):
        usage_count = self.order_storage.get_orders_count_for_promo_code(
            promo_code_id=promo_code_id
        )
        if usage_count >= max_usage_count:
            raise PromoCodeUsageLimitReached(max_usage_count=max_usage_count)

    def _save_order_items(self, cart_items: List[CartItemDTO], order_id: str):
        order_items = self._build_order_items(cart_items=cart_items, order_id=order_id)
        self.order_storage.create_order_items(order_item_dtos=order_items)

    @staticmethod
    def _build_order_items(
        cart_items: List[CartItemDTO],
        order_id: str,
    ) -> List[CreateOrderItemDTO]:
        return [
            CreateOrderItemDTO(
                order_id=order_id,
                item_id=cart_item.menu_item_id,
                item_price=cart_item.item_price,
                quantity=cart_item.quantity,
            )
            for cart_item in cart_items
        ]
