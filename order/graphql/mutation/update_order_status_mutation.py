import graphene

from order.constants.enums import OrderStatus
from order.exception import custom_exceptions
from order.exception.custom_exceptions import UserIsNotRestaurantOwner
from order.graphql.types.error_types import (
    InvalidOrderStatusTransition,
    OrderNotFound,
)
from order.graphql.types.input_types import UpdateOrderStatusInputParams
from order.graphql.types.response_types import UpdateOrderStatusResponse
from order.graphql.types.types import OrderType
from order.interactors.order.update_order_interactor import UpdateOrderStatusInteractor
from order.storages.order_storage import OrderStorage


def _map_order_response(order_dto) -> OrderType:
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


class UpdateOrderStatusMutation(graphene.Mutation):
    class Arguments:
        params = UpdateOrderStatusInputParams(required=True)

    Output = UpdateOrderStatusResponse

    @staticmethod
    def mutate(root, info, params):
        interactor = UpdateOrderStatusInteractor(order_storage=OrderStorage())

        try:
            order_dto = interactor.update_order_status(
                order_id=params.order_id,
                status=OrderStatus(params.status),
                user_id=info.context.user_id,
            )
            return _map_order_response(order_dto=order_dto)

        except custom_exceptions.OrderNotFound as exc:
            return OrderNotFound(order_id=exc.order_id)

        except custom_exceptions.UserIsNotRestaurantOwnerInOrder as exc:
            return UserIsNotRestaurantOwner(user_id=exc.user_id)

        except custom_exceptions.InvalidOrderStatusTransition as exc:
            return InvalidOrderStatusTransition(
                current_status=exc.current_status,
                new_status=exc.new_status,
                allowed=exc.allowed,
            )
