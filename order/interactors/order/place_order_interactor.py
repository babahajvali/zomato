from datetime import datetime
from typing import List

from django.db import transaction


from order.adapter.account import AccountAdapter
from order.adapter.dtos import CartItemDTO
from order.adapter.restaurant import RestaurantAdapter
from order.constants.constants import Tax_percentage
from order.constants.enums import PromoCodeType, OrderStatus
from order.exception.custom_exceptions import (
    PromoCodeMaximumUsed,
    PromoCodeNotEligible,
    InvalidDeliveryZoneFound,
    InvalidAddressFound,
    RestaurantDayTimingNotFound,
    RestaurantClosed,
    EmptyCartItemsFound,
)
from order.interactors.dtos import (
    PlaceOrderDTO,
    OrderDTO,
    CreateOrderDTO,
    CreateOrderItemDTO,
)
from order.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from order.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)
from order.mixin.promocode_mixin import PromoCodeMixin
from utils.redis_util import redis_lock


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

        discount_price = 0.0
        cart_id = self.restaurant_adapter.get_customer_cart_id(
            customer_id=order_data.customer_id
        )

        cart_items = self._validate_cart_items_and_get_items(cart_id=cart_id)

        items_total = self._calculate_items_total(cart_items=cart_items)
        if order_data.promo_code_id:
            self.validate_promo_code_exist(promo_code_id=order_data.promo_code_id)
            promo_code_dto = self.promo_code_storage.get_promo_code_by_id(
                promo_code_id=order_data.promo_code_id
            )
            self._validate_promo_code_eligibility(
                items_total=items_total,
                min_order_value=promo_code_dto.min_order_value,
            )

        self._validate_restaurant_timing(restaurant_id=order_data.restaurant_id)
        delivery_fee = self._validate_address_and_get_delivery_fee(
            address_id=order_data.address_id,
            restaurant_id=order_data.restaurant_id,
        )

        lock_key = (
            f"promo_{order_data.promo_code_id}"
            if order_data.promo_code_id
            else f"order_{order_data.customer_id}"
        )

        with redis_lock(lock_key=lock_key, timeout=10):
            with transaction.atomic():
                if order_data.promo_code_id:
                    promo_code_dto = self.promo_code_storage.get_promo_code_by_id(
                        promo_code_id=order_data.promo_code_id
                    )
                    self._validate_promo_code_available(
                        promo_code_id=order_data.promo_code_id,
                        max_usage_count=promo_code_dto.max_usage,
                    )
                    discount_price = self._calculate_discount_price(
                        items_total=items_total,
                        discount_type=promo_code_dto.discount_type,
                        discount_value=promo_code_dto.discount_value,
                    )

                tax_fee = self._calculate_tax_fee(
                    items_total=items_total,
                    discount_price=discount_price,
                )
                total_amount = (items_total + tax_fee + delivery_fee) - discount_price

                create_order_dto = CreateOrderDTO(
                    customer_id=order_data.customer_id,
                    restaurant_id=order_data.restaurant_id,
                    items_total=items_total,
                    promo_code_id=order_data.promo_code_id,
                    address_id=order_data.address_id,
                    status=OrderStatus.PLACED,
                    delivery_fee=delivery_fee,
                    tax_fee=tax_fee,
                    final_amount=total_amount,
                )

                order_dto = self.order_storage.create_order(
                    create_order_dto=create_order_dto
                )
                order_items = self._build_order_items(
                    cart_items=cart_items,
                    order_id=order_dto.order_id,
                )
                self.order_storage.create_order_items(order_item_dtos=order_items)
                self.restaurant_adapter.clear_customer_cart_items(cart_id=cart_id)

        return order_dto

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
                min_order_value=min_order_value,
                items_total=items_total,
            )

    @staticmethod
    def _calculate_discount_price(
        items_total: float,
        discount_type: str,
        discount_value: float,
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
            restaurant_id=restaurant_id,
            pincode=pincode,
        )
        return delivery_fee

    def _validate_delivery_zone(self, restaurant_id: str, pincode: str) -> float:
        zone_dto = self.restaurant_adapter.get_delivery_zone_by_restaurant_id(
            restaurant_id=restaurant_id,
            pin_code=pincode,
        )
        if zone_dto is None:
            raise InvalidDeliveryZoneFound(
                restaurant_id=restaurant_id,
                pin_code=pincode,
            )
        return zone_dto.delivery_fee

    def _validate_address_and_get_pincode(self, address_id: int) -> str:
        address_dto = self.account_adapter.get_address_by_id(address_id=address_id)
        if address_dto is None:
            raise InvalidAddressFound(address_id=address_id)
        return address_dto.pincode

    def _validate_restaurant_timing(self, restaurant_id: str):
        now = datetime.now()
        day_of_week = now.isoweekday()
        current_time = now.time()

        restaurant_day_timing = self.restaurant_adapter.get_restaurant_timing(
            restaurant_id=restaurant_id,
            day_of_week=day_of_week,
        )
        if restaurant_day_timing is None:
            raise RestaurantDayTimingNotFound(
                restaurant_id=restaurant_id,
                day_of_week=day_of_week,
            )

        if not (
            restaurant_day_timing.open_time
            <= current_time
            <= restaurant_day_timing.close_time
        ):
            raise RestaurantClosed(restaurant_id=restaurant_id)

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

    @staticmethod
    def _calculate_items_total(cart_items: List[CartItemDTO]) -> float:
        return sum(float(item.item_price) * float(item.quantity) for item in cart_items)

    def _validate_cart_items_and_get_items(self, cart_id: str) -> List[CartItemDTO]:
        cart_items = self.restaurant_adapter.get_customer_cart_items(cart_id=cart_id)

        if cart_items is None or len(cart_items) == 0:
            raise EmptyCartItemsFound(cart_id=cart_id)

        return cart_items
