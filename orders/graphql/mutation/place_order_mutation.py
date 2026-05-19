import graphene
from decimal import Decimal

from orders.exception import custom_exceptions, account_exception
from orders.graphql.types.error_types import (
    PromoCodeUsageLimitReached,
    PromoCodeNotEligible,
    DeliveryUnavailableForAddress,
    AddressIdNotFound,
    RestaurantNotOpen,
    RestaurantClosed,
    PromoCodeNotFound,
    CartIsEmpty,
    CustomerCartNotFound,
    MenuItemsUnavailable,
    PromoCodeExpired,
    PromoCodeNotYetValid,
)
from orders.graphql.types.input_types import PlaceOrderInputParams
from orders.graphql.types.response_types import PlaceOrderResponse
from orders.graphql.types.types import OrderSummaryType, OrderItemType
from orders.interactors.dtos import PlaceOrderDTO, OrderSummaryDTO
from orders.interactors.order.place_order_interactor import PlaceOrderInteractor
from orders.storages.order_storage import OrderStorage
from utils.auth_decorators import require_auth

from orders.storages.promo_code_storage import PromoCodeStorage


class PlaceOrderMutation(graphene.Mutation):
    class Arguments:
        params = PlaceOrderInputParams(required=True)

    Output = PlaceOrderResponse

    @staticmethod
    @require_auth
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
            order_summary_dto = interactor.place_order(order_data=place_order_dto)
            return _map_order_response(order_summary_dto=order_summary_dto)

        except custom_exceptions.PromoCodeNotFound as exc:
            return PromoCodeNotFound(promo_code_id=exc.promo_code_id)

        except custom_exceptions.PromoCodeUsageLimitReached as exc:
            return PromoCodeUsageLimitReached(max_usage_count=exc.max_usage_count)

        except custom_exceptions.PromoCodeNotEligible as exc:
            return PromoCodeNotEligible(
                min_order_value=exc.min_order_value,
                items_total=exc.items_total,
            )

        except account_exception.AddressNotFound as exc:
            return AddressIdNotFound(address_id=exc.address_id)

        except custom_exceptions.DeliveryUnavailableForAddress as exc:
            return DeliveryUnavailableForAddress(
                restaurant_id=exc.restaurant_id,
                pin_code=exc.pin_code,
            )

        except custom_exceptions.RestaurantNotOpen as exc:
            return RestaurantNotOpen(
                restaurant_id=exc.restaurant_id,
                day_of_week=exc.day_of_week,
            )

        except custom_exceptions.RestaurantClosed as exc:
            return RestaurantClosed(restaurant_id=exc.restaurant_id)
        except custom_exceptions.CartIsEmpty as exc:
            return CartIsEmpty(cart_id=exc.cart_id)
        except custom_exceptions.CustomerCartNotFound as exc:
            return CustomerCartNotFound(customer_id=exc.customer_id)
        except custom_exceptions.MenuItemsUnavailable as exc:
            return MenuItemsUnavailable(unavailable_item_ids=exc.unavailable_item_ids)
        except custom_exceptions.PromoCodeExpired as exc:
            return PromoCodeExpired(code=exc.code)
        except custom_exceptions.PromoCodeNotYetValid as exc:
            return PromoCodeNotYetValid(code=exc.code)


def _map_order_response(order_summary_dto: OrderSummaryDTO) -> OrderSummaryType:
    order_items = [
        OrderItemType(
            item_id=item.item_id,
            quantity=item.quantity,
            item_price=Decimal(str(item.item_price)),
            subtotal=Decimal(str(item.subtotal)),
        )
        for item in order_summary_dto.items
    ]

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
        items=order_items,
    )
