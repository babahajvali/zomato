import graphene

from order.exception import custom_exceptions
from order.graphql.types.error_types import (
    PromoCodeMaximumUsed,
    PromoCodeNotEligible,
    InvalidDeliveryZoneFound,
    InvalidAddressFound,
    RestaurantDayTimingNotFound,
    RestaurantClosed,
    PromoCodeNotFound,
    EmptyCartItemsFound,
)
from order.graphql.types.input_types import PlaceOrderInputParams
from order.graphql.types.response_types import PlaceOrderResponse
from order.graphql.types.types import OrderType
from order.interactors.dtos import PlaceOrderDTO
from order.interactors.order.place_order_interactor import PlaceOrderInteractor
from order.storages.order_storage import OrderStorage

from order.storages.promo_code_storage import PromoCodeStorage


class PlaceOrderMutation(graphene.Mutation):
    class Arguments:
        params = PlaceOrderInputParams(required=True)

    Output = PlaceOrderResponse

    @staticmethod
    def mutate(root, info, params):
        interactor = PlaceOrderInteractor(
            promo_code_storage=PromoCodeStorage(),
            order_storage=OrderStorage(),
        )

        place_order_dto = PlaceOrderDTO(
            customer_id=info.context.user_id,
            restaurant_id=params.restaurant_id,
            address_id=params.address_id,
            promo_code_id=params.promo_code_id,
        )

        try:
            order_dto = interactor.place_order(order_data=place_order_dto)
            return _map_order_response(order_dto=order_dto)

        except custom_exceptions.PromoCodeNotFound as exc:
            return PromoCodeNotFound(promo_code_id=exc.promo_code_id)

        except custom_exceptions.PromoCodeMaximumUsed as exc:
            return PromoCodeMaximumUsed(max_usage_count=exc.max_usage_count)

        except custom_exceptions.PromoCodeNotEligible as exc:
            return PromoCodeNotEligible(
                min_order_value=exc.min_order_value,
                items_total=exc.items_total,
            )

        except custom_exceptions.InvalidAddressFound as exc:
            return InvalidAddressFound(address_id=exc.address_id)

        except custom_exceptions.InvalidDeliveryZoneFound as exc:
            return InvalidDeliveryZoneFound(
                restaurant_id=exc.restaurant_id,
                pin_code=exc.pin_code,
            )

        except custom_exceptions.RestaurantDayTimingNotFound as exc:
            return RestaurantDayTimingNotFound(
                restaurant_id=exc.restaurant_id,
                day_of_week=exc.day_of_week,
            )

        except custom_exceptions.RestaurantClosed as exc:
            return RestaurantClosed(restaurant_id=exc.restaurant_id)
        except custom_exceptions.EmptyCartItemsFound as exc:
            return EmptyCartItemsFound(cart_id=exc.cart_id)


def _map_order_response(order_dto) -> OrderType:
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
