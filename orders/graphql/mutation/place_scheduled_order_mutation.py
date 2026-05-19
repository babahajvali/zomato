import graphene
from decimal import Decimal

from django.utils import timezone

from accounts.exception import custom_exceptions
from orders.exception import custom_exceptions, account_exception
from orders.graphql.types.error_types import (
    PromoCodeUsageLimitReached,
    PromoCodeNotEligible,
    DeliveryUnavailableForAddress,
    AddressIdNotFound,
    ScheduledTimeTooSoon,
    RestaurantNotOpenAtScheduledTime,
    PromoCodeNotFound,
    CartIsEmpty,
    CustomerCartNotFound,
    MenuItemsUnavailable,
    PromoCodeExpired,
    PromoCodeNotYetValid,
)
from orders.graphql.types.input_types import PlaceScheduledOrderInputParams
from orders.graphql.types.response_types import PlaceScheduledOrderResponse
from orders.graphql.types.types import ScheduledOrderSummaryType, OrderItemType
from orders.interactors.dtos import PlaceScheduledOrderDTO, ScheduledOrderDTO
from orders.interactors.order.place_scheduled_order_interactor import (
    PlaceScheduledOrderInteractor,
)
from orders.storages.order_storage import OrderStorage
from orders.storages.promo_code_storage import PromoCodeStorage
from utils.auth_decorators import require_auth


class PlaceScheduledOrderMutation(graphene.Mutation):
    class Arguments:
        params = PlaceScheduledOrderInputParams(required=True)

    Output = PlaceScheduledOrderResponse

    @staticmethod
    @require_auth
    def mutate(root, info, params):
        interactor = PlaceScheduledOrderInteractor(
            promo_code_storage=PromoCodeStorage(),
            order_storage=OrderStorage(),
        )

        scheduled_for = params.scheduled_for
        if timezone.is_naive(scheduled_for):
            scheduled_for = timezone.make_aware(scheduled_for)

        place_scheduled_order_dto = PlaceScheduledOrderDTO(
            customer_id=info.context.user_id,
            restaurant_id=params.restaurant_id,
            address_id=params.address_id,
            scheduled_for=scheduled_for,
            promo_code_id=params.promo_code_id,
        )

        try:
            scheduled_order_dto = interactor.place_scheduled_order(
                order_data=place_scheduled_order_dto
            )
            return _map_scheduled_order_response(
                scheduled_order_dto=scheduled_order_dto
            )

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

        except custom_exceptions.ScheduledTimeTooSoon as exc:
            return ScheduledTimeTooSoon(scheduled_for=exc.scheduled_for)

        except custom_exceptions.RestaurantNotOpenAtScheduledTime as exc:
            return RestaurantNotOpenAtScheduledTime(
                restaurant_id=exc.restaurant_id,
                scheduled_for=exc.scheduled_for,
            )

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


def _map_scheduled_order_response(
    scheduled_order_dto: ScheduledOrderDTO,
) -> ScheduledOrderSummaryType:
    order_items = [
        OrderItemType(
            item_id=item.item_id,
            quantity=item.quantity,
            item_price=Decimal(str(item.item_price)),
            subtotal=Decimal(str(item.subtotal)),
        )
        for item in scheduled_order_dto.items
    ]

    return ScheduledOrderSummaryType(
        order_id=str(scheduled_order_dto.order_id),
        customer_id=str(scheduled_order_dto.customer_id),
        restaurant_id=str(scheduled_order_dto.restaurant_id),
        promo_code_id=scheduled_order_dto.promo_code_id,
        status=scheduled_order_dto.status.value,
        items_total=Decimal(scheduled_order_dto.items_total),
        delivery_fee=Decimal(scheduled_order_dto.delivery_fee),
        tax_fee=Decimal(scheduled_order_dto.tax_fee),
        final_amount=Decimal(scheduled_order_dto.final_amount),
        address_id=scheduled_order_dto.address_id,
        placed_at=scheduled_order_dto.placed_at,
        scheduled_for=scheduled_order_dto.scheduled_for,
        items=order_items,
    )
