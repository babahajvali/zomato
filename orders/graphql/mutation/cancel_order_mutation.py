import graphene
from decimal import Decimal

from orders.exception import custom_exceptions

from orders.graphql.types.error_types import (
    OrderCannotBeCancelled,
    OrderNotFound,
    OrderNotBelongsToUser,
    OrderCancellationTimeExceeded,
)
from orders.graphql.types.input_types import CancelOrderInputParams
from orders.graphql.types.response_types import CancelOrderResponse
from orders.graphql.types.types import OrderType
from orders.interactors.dtos import OrderDTO
from orders.interactors.order.order_interactor import OrderInteractor
from orders.storages.order_storage import OrderStorage


class CancelOrderMutation(graphene.Mutation):
    class Arguments:
        params = CancelOrderInputParams(required=True)

    Output = CancelOrderResponse

    @staticmethod
    def mutate(root, info, params):
        interactor = OrderInteractor(order_storage=OrderStorage())

        try:
            order_dto = interactor.cancel_order(
                order_id=params.order_id, user_id=info.context.user_id
            )

            return _map_order_response(order_dto=order_dto)

        except custom_exceptions.OrderNotFound as exc:
            return OrderNotFound(order_id=exc.order_id)

        except custom_exceptions.OrderDoesNotBelongToUser as exc:
            return OrderNotBelongsToUser(order_id=exc.order_id)

        except custom_exceptions.OrderCancellationTimeExceeded as exc:
            return OrderCancellationTimeExceeded(
                order_id=exc.order_id, minutes=exc.minutes
            )

        except custom_exceptions.OrderCannotBeCancelled as exc:
            return OrderCannotBeCancelled(order_id=exc.order_id)


def _map_order_response(order_dto: OrderDTO) -> OrderType:
    return OrderType(
        order_id=str(order_dto.order_id),
        customer_id=str(order_dto.customer_id),
        restaurant_id=str(order_dto.restaurant_id),
        promo_code_id=order_dto.promo_code_id,
        status=order_dto.status,
        items_total=Decimal(order_dto.items_total),
        delivery_fee=Decimal(order_dto.delivery_fee),
        tax_fee=Decimal(order_dto.tax_fee),
        final_amount=Decimal(order_dto.final_amount),
        address_id=order_dto.address_id,
        placed_at=order_dto.placed_at,
    )
