from decimal import Decimal

from orders.exception import custom_exceptions
from orders.graphql.types.error_types import OrderNotFound
from orders.graphql.types.types import (
    OrderType,
    OrdersType,
    OrderSummaryType,
    OrderItemType,
)
from orders.interactors.order.get_restaurant_order_interactor import (
    GetRestaurantOrderInteractor,
)
from orders.interactors.order.order_interactor import OrderInteractor
from orders.storages.order_storage import OrderStorage
from utils.graphql_types import UserNotRestaurantOwner


def map_order_response(order_dto) -> OrderType:
    return OrderType(
        order_id=str(order_dto.order_id),
        customer_id=str(order_dto.customer_id),
        restaurant_id=str(order_dto.restaurant_id),
        promo_code_id=order_dto.promo_code_id,
        status=order_dto.status.value,
        items_total=Decimal(order_dto.items_total),
        delivery_fee=Decimal(order_dto.delivery_fee),
        tax_fee=Decimal(order_dto.tax_fee),
        final_amount=Decimal(order_dto.final_amount),
        address_id=order_dto.address_id,
        placed_at=order_dto.placed_at,
    )


def map_orders_response(order_dtos) -> OrdersType:
    return OrdersType(
        orders=[map_order_response(order_dto=order_dto) for order_dto in order_dtos]
    )


def map_order_summary_response(order_summary_dto) -> OrderSummaryType:
    return OrderSummaryType(
        order_id=str(order_summary_dto.order_id),
        customer_id=str(order_summary_dto.customer_id),
        restaurant_id=str(order_summary_dto.restaurant_id),
        promo_code_id=order_summary_dto.promo_code_id,
        status=order_summary_dto.status.value,
        items_total=Decimal(order_summary_dto.items_total),
        delivery_fee=Decimal(order_summary_dto.delivery_fee),
        tax_fee=Decimal(order_summary_dto.tax_fee),
        final_amount=Decimal(order_summary_dto.final_amount),
        address_id=order_summary_dto.address_id,
        placed_at=order_summary_dto.placed_at,
        items=[
            OrderItemType(
                item_id=item.item_id,
                quantity=item.quantity,
                item_price=Decimal(str(item.item_price)),
                subtotal=Decimal(str(item.subtotal)),
            )
            for item in order_summary_dto.items
        ],
    )


def get_order_resolver(root, info, params):
    interactor = OrderInteractor(order_storage=OrderStorage())

    try:
        order_summary_dto = interactor.get_order(order_id=params.order_id)
        return map_order_summary_response(order_summary_dto=order_summary_dto)
    except custom_exceptions.OrderNotFound as exc:
        return OrderNotFound(order_id=exc.order_id)


def get_user_order_resolver(root, info, params):
    interactor = OrderInteractor(order_storage=OrderStorage())
    order_dtos = interactor.get_user_orders(
        user_id=info.context.user_id, limit=params.limit, offset=params.offset
    )

    return map_orders_response(order_dtos=order_dtos)


def get_restaurant_order_resolver(root, info, params):
    interactor = GetRestaurantOrderInteractor(order_storage=OrderStorage())

    try:
        order_dtos = interactor.get_restaurant_orders(
            restaurant_id=params.restaurant_id,
            user_id=info.context.user_id,
            limit=params.limit,
            offset=params.offset,
        )
        return map_orders_response(order_dtos=order_dtos)
    except custom_exceptions.UserNotRestaurantOwner as exc:
        return UserNotRestaurantOwner(user_id=exc.user_id)
