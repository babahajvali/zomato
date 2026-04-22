from typing import List


from order.constants.enums import OrderStatus
from order.interactors.dtos import (
    CreateOrderDTO,
    CreateOrderItemDTO,
    OrderDTO,
)
from order.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from order.models import Order, OrderItem


class OrderStorage(OrderStorageInterface):
    @staticmethod
    def _convert_to_order_dto(order_obj: Order) -> OrderDTO:
        return OrderDTO(
            order_id=str(order_obj.id),
            customer_id=str(order_obj.customer_id),
            restaurant_id=str(order_obj.restaurant_id),
            promo_code_id=order_obj.promo_code.id if order_obj.promo_code else None,
            status=order_obj.status,
            items_total=float(order_obj.items_total),
            delivery_fee=float(order_obj.delivery_fee),
            tax_fee=float(order_obj.tax_fee),
            final_amount=float(order_obj.final_amount),
            address_id=order_obj.address_id,
        )

    def get_order(self, order_id: str) -> OrderDTO | None:
        order_obj = Order.objects.filter(id=order_id).first()

        if order_obj is None:
            return None

        return self._convert_to_order_dto(order_obj=order_obj)

    def get_promo_code_usage(self, promo_code_id: int) -> int:
        return (
            Order.objects.filter(
                promo_code_id=promo_code_id,
            )
            .exclude(status=OrderStatus.CANCELLED.value)
            .count()
        )

    def create_order(self, create_order_dto: CreateOrderDTO) -> OrderDTO:
        order_obj = Order.objects.create(
            customer_id=create_order_dto.customer_id,
            restaurant_id=create_order_dto.restaurant_id,
            promo_code_id=create_order_dto.promo_code_id,
            status=create_order_dto.status.value,
            items_total=create_order_dto.items_total,
            delivery_fee=create_order_dto.delivery_fee,
            tax_fee=create_order_dto.tax_fee,
            final_amount=create_order_dto.final_amount,
            address_id=create_order_dto.address_id,
        )

        return self._convert_to_order_dto(order_obj=order_obj)

    def create_order_items(self, order_item_dtos: List[CreateOrderItemDTO]):
        order_items = [
            OrderItem(
                order_id=each.order_id,
                item_id=each.item_id,
                quantity=each.quantity,
                item_price=each.item_price,
            )
            for each in order_item_dtos
        ]

        OrderItem.objects.bulk_create(order_items)

    def update_order_status(
        self, order_id: str, status: OrderStatus
    ) -> OrderDTO | None:
        Order.objects.filter(id=order_id).update(status=status)

        return self.get_order(order_id=order_id)
