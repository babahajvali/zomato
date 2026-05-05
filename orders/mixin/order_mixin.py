from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, List

from orders.constants.constants import TAX_PERCENTAGE
from orders.constants.enums import OrderStatus, PromoCodeType
from orders.exception.custom_exceptions import (
    InvalidOrderStatusTransition,
    OrderNotFound,
    OrderNotOwnedByUser,
    UserNotRestaurantOwner,
)
from orders.interactors.dtos import (
    OrderDTO,
    OrderSummaryDTO,
    OrderItemSummaryDTO,
    ScheduledOrderDTO,
)
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from restaurants.interactors.dtos import CartItemDTO

VALID_TRANSITIONS = {
    OrderStatus.PLACED: [OrderStatus.CONFIRMED],
    OrderStatus.CONFIRMED: [OrderStatus.PREPARING],
    OrderStatus.PREPARING: [OrderStatus.OUT_OF_DELIVERY],
    OrderStatus.OUT_OF_DELIVERY: [OrderStatus.DELIVERED],
    OrderStatus.DELIVERED: [],
    OrderStatus.CANCELLED: [],
}


class OrderMixin:
    def __init__(self, order_storage: OrderStorageInterface, **kwargs):
        self.order_storage = order_storage
        super().__init__(**kwargs)

    def validate_order_exists(self, order_id: str, user_id: Optional[str]) -> OrderDTO:

        order_dto = self.order_storage.get_order(order_id=order_id)

        if order_dto is None:
            raise OrderNotFound(order_id=order_id)

        if order_dto.customer_id != user_id and user_id is not None:
            raise OrderNotOwnedByUser(order_id=order_id, user_id=user_id)

        return order_dto

    @staticmethod
    def validate_order_status_transition(
        current_status: OrderStatus,
        new_status: OrderStatus,
    ):
        if isinstance(current_status, str):
            current_status = OrderStatus(current_status)
        if isinstance(new_status, str):
            new_status = OrderStatus(new_status)

        allowed = VALID_TRANSITIONS.get(current_status, [])
        if new_status not in allowed:
            raise InvalidOrderStatusTransition(
                current_status=current_status.value,
                new_status=new_status.value,
                allowed=[status.value for status in allowed],
            )

    @staticmethod
    def validate_user_is_restaurant_owner(user_id: str, owner_id: str):

        if owner_id != user_id:
            raise UserNotRestaurantOwner(user_id=user_id)

    @staticmethod
    def build_order_summary_dto(
        cart_items: List[CartItemDTO],
        order_dto: OrderDTO,
    ) -> OrderSummaryDTO:

        return OrderSummaryDTO(
            order_id=order_dto.order_id,
            customer_id=order_dto.customer_id,
            restaurant_id=order_dto.restaurant_id,
            status=order_dto.status,
            items=[
                OrderItemSummaryDTO(
                    item_id=item.menu_item_id,
                    quantity=item.quantity,
                    item_price=Decimal(str(item.item_price)),
                    subtotal=Decimal(str(item.item_price)) * item.quantity,
                )
                for item in cart_items
            ],
            items_total=order_dto.items_total,
            delivery_fee=order_dto.delivery_fee,
            tax_fee=order_dto.tax_fee,
            final_amount=order_dto.final_amount,
            address_id=order_dto.address_id,
            promo_code_id=order_dto.promo_code_id,
            placed_at=order_dto.placed_at,
        )

    @staticmethod
    def build_schedule_order_summary_dto(
        order_dto: OrderDTO,
        cart_items: List[CartItemDTO],
    ) -> ScheduledOrderDTO:
        return ScheduledOrderDTO(
            order_id=order_dto.order_id,
            customer_id=order_dto.customer_id,
            restaurant_id=order_dto.restaurant_id,
            status=order_dto.status,
            items=[
                OrderItemSummaryDTO(
                    item_id=item.menu_item_id,
                    quantity=item.quantity,
                    item_price=Decimal(str(item.item_price)),
                    subtotal=Decimal(str(item.item_price)) * item.quantity,
                )
                for item in cart_items
            ],
            items_total=order_dto.items_total,
            delivery_fee=order_dto.delivery_fee,
            tax_fee=order_dto.tax_fee,
            final_amount=order_dto.final_amount,
            address_id=order_dto.address_id,
            promo_code_id=order_dto.promo_code_id,
            placed_at=order_dto.placed_at,
            scheduled_for=order_dto.scheduled_for,
        )

    @staticmethod
    def calculate_items_total(
        cart_items: List[CartItemDTO],
    ) -> Decimal:
        return Decimal(
            sum(
                Decimal(str(item.item_price)) * Decimal(str(item.quantity))
                for item in cart_items
            )
        )

    @staticmethod
    def calculate_tax_fee(
        items_total: Decimal,
        discount_price: Decimal,
    ) -> Decimal:
        return (
            (items_total - discount_price)
            * Decimal(str(TAX_PERCENTAGE))
            / Decimal("100")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    def calculate_discount_price(
        items_total: Decimal,
        discount_type: str,
        discount_value: Decimal,
    ) -> Decimal:
        if discount_type == PromoCodeType.PERCENTAGE.value:
            return (items_total * discount_value / Decimal("100")).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        return discount_value
