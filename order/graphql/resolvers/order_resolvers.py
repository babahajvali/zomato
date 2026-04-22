from order.exception import custom_exceptions
from order.graphql.types.error_types import OrderNotFound
from order.graphql.types.types import OrderType, OrdersType
from order.interactors.order.get_restaurant_order_interactor import (
    GetRestaurantOrderInteractor,
)
from order.interactors.order.order_interactor import OrderInteractor
from order.storages.order_storage import OrderStorage
from utils.graphql_types import UserIsNotRestaurantOwner


def map_order_response(order_dto) -> OrderType:
    return OrderType(
        order_id=str(order_dto.order_id),
        customer_id=str(order_dto.customer_id),
        restaurant_id=str(order_dto.restaurant_id),
        promo_code_id=order_dto.promo_code_id,
        status=order_dto.status.value,
        items_total=float(order_dto.items_total),
        delivery_fee=float(order_dto.delivery_fee),
        tax_fee=float(order_dto.tax_fee),
        final_amount=float(order_dto.final_amount),
        address_id=order_dto.address_id,
        placed_at=order_dto.placed_at,
    )


def map_orders_response(order_dtos) -> OrdersType:
    return OrdersType(
        orders=[map_order_response(order_dto=order_dto) for order_dto in order_dtos]
    )


def resolve_get_order(root, info, params):
    interactor = OrderInteractor(order_storage=OrderStorage())

    try:
        order_dto = interactor.get_order(order_id=params.order_id)
        return map_order_response(order_dto=order_dto)
    except custom_exceptions.OrderNotFound as exc:
        return OrderNotFound(order_id=exc.order_id)


def resolve_user_orders(root, info):
    interactor = OrderInteractor(order_storage=OrderStorage())
    order_dtos = interactor.user_orders(user_id=info.context.user_id)

    return map_orders_response(order_dtos=order_dtos)


def resolve_restaurant_orders(root, info, params):
    interactor = GetRestaurantOrderInteractor(order_storage=OrderStorage())

    try:
        order_dtos = interactor.get_restaurant_order(
            restaurant_id=params.restaurant_id,
            user_id=info.context.user_id,
        )
        return map_orders_response(order_dtos=order_dtos)
    except custom_exceptions.UserIsNotRestaurantOwner as exc:
        return UserIsNotRestaurantOwner(user_id=exc.user_id)
