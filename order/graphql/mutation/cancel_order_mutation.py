import graphene

from order.exception.custom_exceptions import (
    OrderCancellationTimeExceeded,
    OrderCannotBeCancelled,
    OrderNotFound,
    OrderDoesNotBelongToUser,
)
from order.graphql.types.error_types import (
    OrderCancellationTimeExceededType,
    OrderCannotBeCancelledType,
    OrderNotFoundType,
    OrderNotBelongsToUserType,
)
from order.graphql.types.input_types import CancelOrderInputParams
from order.graphql.types.response_types import CancelOrderResponse
from order.graphql.types.types import OrderType
from order.interactors.order.order_interactor import OrderInteractor
from order.storages.order_storage import OrderStorage


class CancelOrderMutation(graphene.Mutation):
    class Arguments:
        params = CancelOrderInputParams(required=True)

    Output = CancelOrderResponse

    def mutate(self, root, info, params):
        interactor = OrderInteractor(order_storage=OrderStorage())

        try:
            order_dto = interactor.cancel_order(
                order_id=params.order_id, user_id=info.context.user_id
            )

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

        except OrderNotFound as exc:
            return OrderNotFoundType(order_id=exc.order_id)

        except OrderDoesNotBelongToUser as exc:
            return OrderNotBelongsToUserType(order_id=exc.order_id)

        except OrderCancellationTimeExceeded as exc:
            return OrderCancellationTimeExceededType(order_id=exc.order_id)

        except OrderCannotBeCancelled as exc:
            return OrderCannotBeCancelledType(order_id=exc.order_id)
