from datetime import timedelta
from typing import List

from django.utils import timezone

from orders.adapter.restaurant import RestaurantAdapter
from orders.constants.constants import CANCEL_TIME
from orders.interactors.dtos import (
    OrderDTO,
    OrderSummaryDTO,
    OrderItemSummaryDTO,
    OrderItemDTO, ScheduledOrderDTO,
)
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.mixin.order_mixin import OrderMixin


class GetRestaurantOrderInteractor(OrderMixin):
    def __init__(self, order_storage: OrderStorageInterface):
        super().__init__(order_storage=order_storage)
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

        orders = self._filter_orders_after_cancellation_window(orders)

        if not orders:
            return []

        order_ids = [order.order_id for order in orders]

        order_items = self.order_storage.get_orders_items(order_ids=order_ids)

        return self._build_order_summaries(order_items=order_items, orders=orders)

    def get_today_restaurant_scheduled_orders(self, restaurant_id: str, user_id: str, limit: int, offset: int) -> List[ScheduledOrderDTO]:
        owner_id = self.restaurant_adapter.get_restaurant_owner_id(
            restaurant_id=restaurant_id
        )
        self.validate_user_is_restaurant_owner(user_id=user_id,owner_id=owner_id)
        orders = self.order_storage.get_today_restaurant_scheduled_orders(restaurant_id=restaurant_id, limit=limit, offset=offset)

        order_ids = [order.order_id for order in orders]

        order_items = self.order_storage.get_orders_items(order_ids=order_ids)

        return self._build_schedule_order_summaries(
            order_items=order_items,
            orders=orders,
        )

    @staticmethod
    def _build_order_summaries(
        order_items: list[OrderItemDTO], orders: list[OrderDTO]
    ) -> list[OrderSummaryDTO]:
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

    @staticmethod
    def _filter_orders_after_cancellation_window(
        orders: List[OrderDTO],
    ) -> List[OrderDTO]:

        now = timezone.now()
        cancellation_cutoff = now - timedelta(minutes=CANCEL_TIME)

        return [order for order in orders if order.placed_at <= cancellation_cutoff]

    @staticmethod
    def _build_schedule_order_summaries(
            order_items: list[OrderItemDTO], orders: list[OrderDTO]
    ) -> list[ScheduledOrderDTO]:
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
                ScheduledOrderDTO(
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
                    scheduled_for=order.scheduled_for,
                )
            )

        return result
