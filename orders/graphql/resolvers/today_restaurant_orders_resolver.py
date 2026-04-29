from decimal import Decimal

from orders.exception import custom_exceptions
from utils.graphql_types import UserNotRestaurantOwner
from orders.graphql.types.types import (
    OrderSummaryType,
    OrderItemType,
    OrderSummariesType,
)
from orders.interactors.order.get_restaurant_order_interactor import (
    GetRestaurantOrderInteractor,
)
from orders.storages.order_storage import OrderStorage


def map_order_response(order_dto) -> OrderSummaryType:

    return OrderSummaryType(
        order_id=str(order_dto.order_id),
        customer_id=str(order_dto.customer_id),
        restaurant_id=str(order_dto.restaurant_id),
        promo_code_id=order_dto.promo_code_id,
        status=order_dto.status.value,
        items=[
            OrderItemType(
                item_id=item.item_id,
                quantity=item.quantity,
                item_price=Decimal(str(item.item_price)),
                subtotal=Decimal(str(item.subtotal)),
            )
            for item in order_dto.items
        ],
        items_total=Decimal(order_dto.items_total),
        delivery_fee=Decimal(order_dto.delivery_fee),
        tax_fee=Decimal(order_dto.tax_fee),
        final_amount=Decimal(order_dto.final_amount),
        address_id=order_dto.address_id,
        placed_at=order_dto.placed_at,
    )


def map_orders_response(order_dtos) -> OrderSummariesType:
    return OrderSummariesType(
        order_summaries=[
            map_order_response(order_dto=order_dto) for order_dto in order_dtos
        ]
    )


def get_today_restaurant_orders_resolver(root, info, params):
    interactor = GetRestaurantOrderInteractor(order_storage=OrderStorage())

    try:
        order_dtos = interactor.get_today_restaurant_orders(
            restaurant_id=params.restaurant_id,
            user_id=info.context.user_id,
            limit=params.limit,
            offset=params.offset,
        )
        return map_orders_response(order_dtos=order_dtos)
    except custom_exceptions.UserNotRestaurantOwner as exc:
        return UserNotRestaurantOwner(user_id=exc.user_id)
