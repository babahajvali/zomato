from typing import List


from orders.adapter.restaurant import RestaurantAdapter
from orders.interactors.dtos import (
    OrderDTO,
    OrderSummaryDTO,
    OrderItemSummaryDTO,
    OrderItemDTO,
)
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.mixin.order_mixin import OrderMixin


class GetRestaurantOrderInteractor(OrderMixin):
    def __init__(self, order_storage: OrderStorageInterface):
        self.order_storage = order_storage
        self.restaurant_adapter = RestaurantAdapter()

    def get_restaurant_orders(
        self, restaurant_id: str, user_id: str, limit: int, offset: int
    ) -> List[OrderDTO]:
        owner_id = self.restaurant_adapter.get_restaurant_owner_id(
            restaurant_id=restaurant_id
        )
        self.validate_user_is_restaurant_owner(owner_id=owner_id, user_id=user_id)

        return self.order_storage.get_restaurant_orders(
            restaurant_id=restaurant_id, limit=limit, offset=offset
        )

    def get_today_restaurant_orders(
        self, restaurant_id: str, user_id: str, limit: int, offset: int
    ) -> List[OrderSummaryDTO]:
        owner_id = self.restaurant_adapter.get_restaurant_owner_id(
            restaurant_id=restaurant_id
        )

        self.validate_user_is_restaurant_owner(
            owner_id=owner_id,
            user_id=user_id,
        )

        orders = self.order_storage.get_today_restaurant_orders(
            restaurant_id=restaurant_id,
            limit=limit,
            offset=offset,
        )

        if not orders:
            return []

        order_ids = [order.order_id for order in orders]

        order_items = self.order_storage.get_orders_items(order_ids=order_ids)

        return self._build_order_summaries(order_items=order_items, orders=orders)

    @staticmethod
    def _build_order_summaries(
        order_items: List[OrderItemDTO], orders: List[OrderDTO]
    ) -> List[OrderSummaryDTO]:
        items_by_order = {}
        for item in order_items:
            items_by_order.setdefault(item.order_id, []).append(item)

        result = []

        for order in orders:
            items = items_by_order.get(order.order_id, [])

            item_dtos = [
                OrderItemSummaryDTO(
                    item_id=i.item_id,
                    quantity=i.quantity,
                    item_price=i.item_price,
                    subtotal=i.subtotal,
                )
                for i in items
            ]

            result.append(
                OrderSummaryDTO(
                    order_id=order.order_id,
                    customer_id=order.customer_id,
                    restaurant_id=order.restaurant_id,
                    promo_code_id=order.promo_code_id,
                    status=order.status,
                    items=item_dtos,
                    items_total=order.items_total,
                    delivery_fee=order.delivery_fee,
                    tax_fee=order.tax_fee,
                    final_amount=order.final_amount,
                    placed_at=order.placed_at,
                    address_id=order.address_id,
                )
            )

        return result
