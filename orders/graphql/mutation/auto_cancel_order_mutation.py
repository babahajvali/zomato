import graphene

from orders.exception.custom_exceptions import (
    OrderCannotBeCancelled,
    OrderNotFound,
)
from orders.graphql.types.error_types import (
    OrderCannotBeCancelledType,
    OrderNotFoundType,
)
from orders.graphql.types.input_types import AutoCancelOrderInputParams
from orders.graphql.types.response_types import AutoCancelOrderResponse
from orders.graphql.types.types import OrderType
from orders.interactors.dtos import OrderDTO
from orders.interactors.order.order_interactor import OrderInteractor
from orders.storages.order_storage import OrderStorage


class AutoCancelOrderMutation(graphene.Mutation):
    class Arguments:
        params = AutoCancelOrderInputParams(required=True)

    Output = AutoCancelOrderResponse

    @staticmethod
    def mutate(root, info, params):
        interactor = OrderInteractor(order_storage=OrderStorage())

        try:
            order_dto = interactor.auto_cancel_order(order_id=params.order_id)

            return _map_order_response(order_dto=order_dto)

        except OrderNotFound as exc:
            return OrderNotFoundType(order_id=exc.order_id)

        except OrderCannotBeCancelled as exc:
            return OrderCannotBeCancelledType(order_id=exc.order_id)


def _map_order_response(order_dto: OrderDTO) -> OrderType:
    return OrderType(
        order_id=str(order_dto.order_id),
        customer_id=str(order_dto.customer_id),
        restaurant_id=str(order_dto.restaurant_id),
        promo_code_id=order_dto.promo_code_id,
        status=order_dto.status,
        items_total=float(order_dto.items_total),
        delivery_fee=float(order_dto.delivery_fee),
        tax_fee=float(order_dto.tax_fee),
        final_amount=float(order_dto.final_amount),
        address_id=order_dto.address_id,
        placed_at=order_dto.placed_at,
    )
