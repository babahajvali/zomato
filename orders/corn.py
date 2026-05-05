from datetime import datetime

from django.db import transaction

from orders.adapter.restaurant import RestaurantAdapter
from orders.constants.enums import OrderStatus
from orders.interactors.dtos import OrderDTO
from orders.storages.order_storage import OrderStorage


restaurant_adapter = RestaurantAdapter()
order_storage = OrderStorage()


def release_scheduled_orders():

    with transaction.atomic():
        scheduled_orders = order_storage.get_scheduled_orders_due_for_release()

        for order_dto in scheduled_orders:
            if _should_cancel(order_dto=order_dto):
                _cancel_order(order_id=order_dto.order_id)
                continue
            _release_order(order_id=order_dto.order_id)


def _should_cancel(order_dto: OrderDTO) -> bool:
    return _has_unavailable_items(order_id=order_dto.order_id) or _is_restaurant_closed(
        scheduled_for=order_dto.scheduled_for,
        restaurant_id=order_dto.restaurant_id,
    )


def _has_unavailable_items(order_id) -> bool:
    item_ids = order_storage.get_order_item_ids(order_id=order_id)
    unavailable = restaurant_adapter.get_unavailable_menu_items(menu_item_ids=item_ids)
    return len(unavailable) > 0


def _is_restaurant_closed(scheduled_for: datetime, restaurant_id: str) -> bool:

    day_of_week = scheduled_for.isoweekday()

    timing = restaurant_adapter.get_restaurant_timing(
        restaurant_id=restaurant_id,
        day_of_week=day_of_week,
    )

    if timing is None:
        return True

    return not (timing.open_time <= scheduled_for.time() <= timing.close_time)


def _release_order(order_id: str):
    order_storage.update_order_status(
        order_id=order_id,
        status=OrderStatus.PLACED,
    )


def _cancel_order(order_id: str):
    order_storage.update_order_status(
        order_id=order_id,
        status=OrderStatus.CANCELLED,
    )
