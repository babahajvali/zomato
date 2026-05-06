from contextlib import contextmanager
from datetime import time, timedelta, datetime
from decimal import Decimal
from unittest.mock import MagicMock, create_autospec, patch

import pytest
from django.utils import timezone

from orders.adapter.dtos import (
    AddressDTO,
    CartItemDTO,
    DeliveryZoneDTO,
    RestaurantTimingDTO,
)
from orders.constants.enums import OrderStatus
from orders.exception.custom_exceptions import (
    MenuItemsUnavailable,
    RestaurantNotOpenAtScheduledTime,
    ScheduledTimeTooSoon,
)
from orders.interactors.order.place_scheduled_order_interactor import (
    PlaceScheduledOrderInteractor,
)
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)
from orders.tests.factories.interactor_factories import (
    OrderDTOFactory,
    PlaceScheduledOrderDTOFactory,
    PromoCodeDTOFactory,
)


@contextmanager
def no_op_lock(*args, **kwargs):
    yield


TRANSACTION_ATOMIC = (
    "orders.interactors.order.place_scheduled_order_interactor.transaction.atomic"
)

REDIS_LOCK = "orders.interactors.order.place_scheduled_order_interactor.redis_lock"


class TestPlaceScheduledOrderInteractor:
    def setup_method(self):
        self.promo_code_storage = create_autospec(PromoCodeStorageInterface)
        self.order_storage = create_autospec(OrderStorageInterface)
        self.interactor = PlaceScheduledOrderInteractor(
            promo_code_storage=self.promo_code_storage,
            order_storage=self.order_storage,
        )
        self.interactor.account_adapter = MagicMock()
        self.interactor.restaurant_adapter = MagicMock()

    def _setup_valid_adapters(self, scheduled_for):
        self.interactor.account_adapter.get_address_by_id.return_value = AddressDTO(
            address_id=1,
            full_address="221B Baker Street",
            city="Hyderabad",
            pincode="500001",
            label="home",
            is_default=True,
            user_id="customer-1",
        )
        self.interactor.restaurant_adapter.get_delivery_zone_by_restaurant_id.return_value = DeliveryZoneDTO(
            delivery_zone_id=1,
            restaurant_id="restaurants-1",
            pin_code="500001",
            delivery_fee=30.0,
            estimated_delivery_mins=30,
        )
        self.interactor.restaurant_adapter.get_restaurant_timing.return_value = (
            RestaurantTimingDTO(
                timing_id=1,
                restaurant_id="restaurants-1",
                day_of_week=scheduled_for.isoweekday(),
                open_time=time(0, 0),
                close_time=time(23, 59),
            )
        )
        self.interactor.restaurant_adapter.get_customer_cart_id.return_value = "cart-1"
        self.interactor.restaurant_adapter.get_customer_cart_items.return_value = [
            CartItemDTO(
                cart_item_id=1,
                cart_id="cart-1",
                menu_item_id="item-1",
                quantity=2,
                item_price=Decimal("200.00"),
            )
        ]
        self.interactor.restaurant_adapter.get_unavailable_menu_items.return_value = []

    @patch(TRANSACTION_ATOMIC, no_op_lock)
    @patch(REDIS_LOCK, no_op_lock)
    def test_place_scheduled_order_successfully_without_promo_code(self):
        scheduled_for = timezone.now() + timedelta(hours=2)
        self._setup_valid_adapters(scheduled_for=scheduled_for)
        self.order_storage.create_order.return_value = OrderDTOFactory(
            order_id="orders-1",
            status=OrderStatus.SCHEDULED,
            scheduled_for=scheduled_for,
            items_total=400.0,
            delivery_fee=30.0,
            tax_fee=20.0,
            final_amount=450.0,
        )

        result = self.interactor.place_scheduled_order(
            order_data=PlaceScheduledOrderDTOFactory(
                customer_id="customer-1",
                restaurant_id="restaurants-1",
                scheduled_for=scheduled_for,
            )
        )

        assert result.order_id == "orders-1"
        assert result.status == OrderStatus.SCHEDULED
        assert result.scheduled_for == scheduled_for
        create_order_dto = self.order_storage.create_order.call_args.kwargs[
            "create_order_dto"
        ]
        assert create_order_dto.status == OrderStatus.SCHEDULED
        assert create_order_dto.scheduled_for == scheduled_for
        self.promo_code_storage.get_promo_code_by_id.assert_not_called()
        self.order_storage.create_order_items.assert_called_once()
        self.interactor.restaurant_adapter.clear_customer_cart_items.assert_called_once_with(
            cart_id="cart-1"
        )

    @patch(TRANSACTION_ATOMIC, no_op_lock)
    @patch(REDIS_LOCK, no_op_lock)
    def test_place_scheduled_order_successfully_with_percentage_promo_code(self):
        scheduled_for = timezone.now() + timedelta(hours=2)
        self._setup_valid_adapters(scheduled_for=scheduled_for)
        self.promo_code_storage.get_promo_code_by_id.return_value = PromoCodeDTOFactory(
            promo_code_id=1,
            discount_type="PERCENTAGE",
            discount_value=10.0,
            min_order_value=100.0,
            max_usage=5,
        )
        self.order_storage.get_promo_code_usage.return_value = 0
        self.order_storage.create_order.return_value = OrderDTOFactory(
            order_id="orders-2",
            promo_code_id=1,
            status=OrderStatus.SCHEDULED,
            scheduled_for=scheduled_for,
            items_total=400.0,
            delivery_fee=30.0,
            tax_fee=18.0,
            final_amount=408.0,
        )

        result = self.interactor.place_scheduled_order(
            order_data=PlaceScheduledOrderDTOFactory(
                customer_id="customer-1",
                restaurant_id="restaurants-1",
                scheduled_for=scheduled_for,
                promo_code_id=1,
            )
        )

        assert result.order_id == "orders-2"
        create_order_dto = self.order_storage.create_order.call_args.kwargs[
            "create_order_dto"
        ]
        assert create_order_dto.tax_fee == Decimal("18.00")
        assert create_order_dto.final_amount == Decimal("408.00")

    def test_place_scheduled_order_raises_scheduled_time_too_soon(self):
        scheduled_for = timezone.now() + timedelta(minutes=10)

        with pytest.raises(ScheduledTimeTooSoon) as exc:
            self.interactor.place_scheduled_order(
                order_data=PlaceScheduledOrderDTOFactory(scheduled_for=scheduled_for)
            )

        assert exc.value.scheduled_for == scheduled_for
        self.order_storage.create_order.assert_not_called()

    def test_place_scheduled_order_raises_restaurant_not_open_at_scheduled_time(self):
        scheduled_for = timezone.now() + timedelta(hours=2)
        self._setup_valid_adapters(scheduled_for=scheduled_for)
        self.interactor.restaurant_adapter.get_restaurant_timing.return_value = None

        with pytest.raises(RestaurantNotOpenAtScheduledTime) as exc:
            self.interactor.place_scheduled_order(
                order_data=PlaceScheduledOrderDTOFactory(
                    restaurant_id="restaurants-1",
                    scheduled_for=scheduled_for,
                )
            )

        assert exc.value.restaurant_id == "restaurants-1"
        assert exc.value.scheduled_for == scheduled_for
        self.order_storage.create_order.assert_not_called()

    @patch(REDIS_LOCK, no_op_lock)
    def test_place_scheduled_order_raises_menu_items_unavailable(self):
        scheduled_for = timezone.now() + timedelta(hours=2)
        self._setup_valid_adapters(scheduled_for=scheduled_for)
        self.interactor.restaurant_adapter.get_unavailable_menu_items.return_value = [
            "item-1"
        ]

        with pytest.raises(MenuItemsUnavailable) as exc:
            self.interactor.place_scheduled_order(
                order_data=PlaceScheduledOrderDTOFactory(scheduled_for=scheduled_for)
            )

        assert exc.value.unavailable_item_ids == ["item-1"]
        self.order_storage.create_order.assert_not_called()

    def test_validate_restaurant_timing_for_scheduled_time_raises_when_time_is_outside_window(
        self,
    ):
        scheduled_for = datetime.now() + timedelta(hours=2)
        self.interactor.restaurant_adapter.get_restaurant_timing.return_value = (
            RestaurantTimingDTO(
                timing_id=1,
                restaurant_id="restaurants-1",
                day_of_week=scheduled_for.isoweekday(),
                open_time=time(8, 0),
                close_time=time(9, 0),
            )
        )

        with pytest.raises(RestaurantNotOpenAtScheduledTime):
            self.interactor._validate_restaurant_timing_for_scheduled_time(
                restaurant_id="restaurants-1",
                scheduled_for=scheduled_for,
            )
