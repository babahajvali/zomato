from contextlib import contextmanager
from datetime import time
from decimal import Decimal
from unittest.mock import MagicMock, create_autospec, patch

import pytest

from orders.adapter.dtos import (
    AddressDTO,
    CartItemDTO,
    DeliveryZoneDTO,
    RestaurantTimingDTO,
)
from orders.exception.custom_exceptions import (
    AddressNotFound,
    CustomerCartNotFound,
    DeliveryUnavailableForAddress,
    CartIsEmpty,
    MenuItemsUnavailable,
    PromoCodeUsageLimitReached,
    PromoCodeNotEligible,
    PromoCodeNotFound,
    PromoCodeExpired,
    PromoCodeNotYetValid,
    RestaurantClosed,
    RestaurantNotOpen,
)
from orders.interactors.order.place_order_interactor import PlaceOrderInteractor
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.interactors.storage_interface.promo_code_storage_interface import (
    PromoCodeStorageInterface,
)
from orders.tests.factories.interactor_factories import (
    OrderDTOFactory,
    PlaceOrderDTOFactory,
    PromoCodeDTOFactory,
)


@contextmanager
def no_op_lock(*args, **kwargs):
    yield


class TestPlaceOrderInteractor:
    def setup_method(self):
        self.promo_code_storage = create_autospec(PromoCodeStorageInterface)
        self.order_storage = create_autospec(OrderStorageInterface)
        self.interactor = PlaceOrderInteractor(
            promo_code_storage=self.promo_code_storage,
            order_storage=self.order_storage,
        )
        self.interactor.account_adapter = MagicMock()
        self.interactor.restaurant_adapter = MagicMock()

    def _setup_valid_adapters(self):
        self.interactor.restaurant_adapter.get_customer_cart_id.return_value = "cart-1"
        self.interactor.restaurant_adapter.get_customer_cart_items.return_value = [
            CartItemDTO(
                cart_item_id=1,
                cart_id="cart-1",
                menu_item_id="item-1",
                quantity=2,
                item_price=Decimal(200.0),
            )
        ]
        self.interactor.restaurant_adapter.get_restaurant_timing.return_value = (
            RestaurantTimingDTO(
                timing_id=1,
                restaurant_id="restaurants-1",
                day_of_week=1,
                open_time=time(0, 0),
                close_time=time(23, 59),
            )
        )
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
        self.interactor.restaurant_adapter.get_unavailable_menu_items.return_value = []

    @patch(
        "orders.interactors.order.place_order_interactor.transaction.atomic",
        no_op_lock,
    )
    @patch("orders.interactors.order.place_order_interactor.redis_lock", no_op_lock)
    def test_place_order_successfully_with_flat_promo_code(self):
        self._setup_valid_adapters()
        promo_code = PromoCodeDTOFactory(
            promo_code_id=1,
            discount_type="FLAT",
            discount_value=50.0,
            min_order_value=100.0,
            max_usage=10,
        )
        order_dto = OrderDTOFactory(
            order_id="orders-1",
            promo_code_id=1,
            items_total=400.0,
            delivery_fee=30.0,
            tax_fee=17.5,
            final_amount=397.5,
        )
        self.promo_code_storage.get_promo_code_by_id.return_value = promo_code
        self.order_storage.get_promo_code_usage.return_value = 0
        self.order_storage.create_order.return_value = order_dto

        result = self.interactor.place_order(
            order_data=PlaceOrderDTOFactory(
                customer_id="customer-1",
                restaurant_id="restaurants-1",
                address_id=1,
                promo_code_id=1,
            )
        )

        assert result.order_id == "orders-1"
        create_order_dto = self.order_storage.create_order.call_args.kwargs[
            "create_order_dto"
        ]
        assert create_order_dto.items_total == 400.0
        assert create_order_dto.delivery_fee == 30.0
        assert create_order_dto.tax_fee == 17.5
        assert create_order_dto.final_amount == 397.5
        self.order_storage.create_order_items.assert_called_once()
        self.interactor.restaurant_adapter.clear_customer_cart_items.assert_called_once_with(
            cart_id="cart-1"
        )

    @patch(
        "orders.interactors.order.place_order_interactor.transaction.atomic",
        no_op_lock,
    )
    @patch("orders.interactors.order.place_order_interactor.redis_lock", no_op_lock)
    def test_place_order_successfully_without_promo_code(self):
        self._setup_valid_adapters()
        self.order_storage.create_order.return_value = OrderDTOFactory(
            order_id="orders-1",
            promo_code_id=None,
            items_total=400.0,
            delivery_fee=30.0,
            tax_fee=20.0,
            final_amount=450.0,
        )

        result = self.interactor.place_order(
            order_data=PlaceOrderDTOFactory(
                customer_id="customer-1",
                restaurant_id="restaurants-1",
                address_id=1,
                promo_code_id=None,
            )
        )

        assert result.order_id == "orders-1"
        self.promo_code_storage.get_promo_code_by_id.assert_not_called()
        create_order_dto = self.order_storage.create_order.call_args.kwargs[
            "create_order_dto"
        ]
        assert create_order_dto.tax_fee == 20.0
        assert create_order_dto.final_amount == 450.0
        assert create_order_dto.scheduled_for is None

    @patch("orders.interactors.order.place_order_interactor.redis_lock", no_op_lock)
    def test_place_order_raises_promo_code_not_found(self):
        self._setup_valid_adapters()
        self.promo_code_storage.get_promo_code_by_id.return_value = None

        with pytest.raises(PromoCodeNotFound) as exc:
            self.interactor.place_order(
                order_data=PlaceOrderDTOFactory(promo_code_id=99)
            )

        assert exc.value.promo_code_id == 99
        self.order_storage.create_order.assert_not_called()

    @patch("orders.interactors.order.place_order_interactor.redis_lock", no_op_lock)
    def test_place_order_raises_promo_code_not_eligible(self):
        self._setup_valid_adapters()
        self.promo_code_storage.get_promo_code_by_id.return_value = PromoCodeDTOFactory(
            promo_code_id=1,
            min_order_value=500.0,
        )

        with pytest.raises(PromoCodeNotEligible) as exc:
            self.interactor.place_order(
                order_data=PlaceOrderDTOFactory(promo_code_id=1)
            )

        assert exc.value.min_order_value == 500.0
        assert exc.value.items_total == 400.0
        self.order_storage.create_order.assert_not_called()

    @patch(
        "orders.interactors.order.place_order_interactor.transaction.atomic",
        no_op_lock,
    )
    @patch("orders.interactors.order.place_order_interactor.redis_lock", no_op_lock)
    def test_place_order_raises_promo_code_maximum_used(self):
        self._setup_valid_adapters()
        self.promo_code_storage.get_promo_code_by_id.return_value = PromoCodeDTOFactory(
            promo_code_id=1,
            max_usage=2,
        )
        self.order_storage.get_promo_code_usage.return_value = 2

        with pytest.raises(PromoCodeUsageLimitReached) as exc:
            self.interactor.place_order(
                order_data=PlaceOrderDTOFactory(promo_code_id=1)
            )

        assert exc.value.max_usage_count == 2
        self.order_storage.create_order.assert_not_called()

    @patch("orders.interactors.order.place_order_interactor.redis_lock", no_op_lock)
    def test_place_order_raises_customer_cart_not_found(self):
        self._setup_valid_adapters()
        self.interactor.restaurant_adapter.get_customer_cart_id.return_value = None

        with pytest.raises(CustomerCartNotFound) as exc:
            self.interactor.place_order(
                order_data=PlaceOrderDTOFactory(customer_id="customer-404")
            )

        assert exc.value.customer_id == "customer-404"
        self.order_storage.create_order.assert_not_called()

    @patch("orders.interactors.order.place_order_interactor.redis_lock", no_op_lock)
    def test_place_order_raises_empty_cart_items_found(self):
        self._setup_valid_adapters()
        self.interactor.restaurant_adapter.get_customer_cart_items.return_value = []

        with pytest.raises(CartIsEmpty) as exc:
            self.interactor.place_order(
                order_data=PlaceOrderDTOFactory(customer_id="customer-1")
            )

        assert exc.value.cart_id == "cart-1"
        self.order_storage.create_order.assert_not_called()

    @patch("orders.interactors.order.place_order_interactor.redis_lock", no_op_lock)
    def test_place_order_raises_menu_items_unavailable(self):
        self._setup_valid_adapters()
        self.interactor.restaurant_adapter.get_unavailable_menu_items.return_value = [
            "item-1"
        ]

        with pytest.raises(MenuItemsUnavailable) as exc:
            self.interactor.place_order(order_data=PlaceOrderDTOFactory())

        assert exc.value.unavailable_item_ids == ["item-1"]
        self.order_storage.create_order.assert_not_called()

    def test_place_order_raises_restaurant_day_timing_not_found(self):
        self._setup_valid_adapters()
        self.interactor.restaurant_adapter.get_restaurant_timing.return_value = None

        with pytest.raises(RestaurantNotOpen):
            self.interactor.place_order(order_data=PlaceOrderDTOFactory())

        self.order_storage.create_order.assert_not_called()

    def test_place_order_raises_restaurant_closed(self):
        self._setup_valid_adapters()
        self.interactor.restaurant_adapter.get_restaurant_timing.return_value = (
            RestaurantTimingDTO(
                timing_id=1,
                restaurant_id="restaurants-1",
                day_of_week=1,
                open_time=time(0, 0),
                close_time=time(0, 1),
            )
        )

        with pytest.raises(RestaurantClosed):
            self.interactor.place_order(order_data=PlaceOrderDTOFactory())

        self.order_storage.create_order.assert_not_called()

    def test_place_order_raises_invalid_address_found(self):
        self._setup_valid_adapters()
        self.interactor.account_adapter.get_address_by_id.return_value = None

        with pytest.raises(AddressNotFound) as exc:
            self.interactor.place_order(order_data=PlaceOrderDTOFactory(address_id=999))

        assert exc.value.address_id == 999
        self.order_storage.create_order.assert_not_called()

    @pytest.mark.django_db
    def test_place_order_raises_invalid_delivery_zone_found(self):
        self._setup_valid_adapters()
        self.interactor.restaurant_adapter.get_delivery_zone_by_restaurant_id.return_value = None

        with pytest.raises(DeliveryUnavailableForAddress) as exc:
            self.interactor.place_order(
                order_data=PlaceOrderDTOFactory(restaurant_id="restaurants-1")
            )

        assert exc.value.restaurant_id == "restaurants-1"
        assert exc.value.pin_code == "500001"
        self.order_storage.create_order.assert_not_called()

    def test_build_order_items(self):
        result = self.interactor._build_order_items(
            cart_items=[
                CartItemDTO(
                    cart_item_id=1,
                    cart_id="cart-1",
                    menu_item_id="item-1",
                    quantity=2,
                    item_price=200.0,
                )
            ],
            order_id="orders-1",
        )

        assert len(result) == 1
        assert result[0].order_id == "orders-1"
        assert result[0].item_id == "item-1"
        assert result[0].quantity == 2
        assert result[0].item_price == 200.0

    @patch(
        "orders.interactors.order.place_order_interactor.transaction.atomic",
        no_op_lock,
    )
    @patch("orders.interactors.order.place_order_interactor.redis_lock", no_op_lock)
    def test_place_order_raises_promo_code_expired(self):
        self._setup_valid_adapters()
        from django.utils import timezone
        from datetime import timedelta

        expired_promo = PromoCodeDTOFactory(
            promo_code_id=1,
            valid_until=timezone.now() - timedelta(days=1),  # Expired yesterday
        )
        self.promo_code_storage.get_promo_code_by_id.return_value = expired_promo

        with pytest.raises(PromoCodeExpired) as exc:
            self.interactor.place_order(
                order_data=PlaceOrderDTOFactory(promo_code_id=1)
            )

        assert exc.value.code == expired_promo.code
        self.order_storage.create_order.assert_not_called()

    @patch(
        "orders.interactors.order.place_order_interactor.transaction.atomic",
        no_op_lock,
    )
    @patch("orders.interactors.order.place_order_interactor.redis_lock", no_op_lock)
    def test_place_order_raises_promo_code_not_yet_valid(self):
        self._setup_valid_adapters()
        from django.utils import timezone
        from datetime import timedelta

        future_promo = PromoCodeDTOFactory(
            promo_code_id=1,
            valid_from=timezone.now() + timedelta(days=1),  # Valid tomorrow
        )
        self.promo_code_storage.get_promo_code_by_id.return_value = future_promo

        with pytest.raises(PromoCodeNotYetValid) as exc:
            self.interactor.place_order(
                order_data=PlaceOrderDTOFactory(promo_code_id=1)
            )

        assert exc.value.code == future_promo.code
        self.order_storage.create_order.assert_not_called()

    def test_place_order_percentage_discount_calculation(self):
        # Test the percentage discount calculation directly
        from decimal import Decimal
        from orders.constants.enums import PromoCodeType

        items_total = Decimal("400.00")
        discount_type = PromoCodeType.PERCENTAGE.value
        discount_value = Decimal("10.00")  # 10%

        result = self.interactor._calculate_discount_price(
            items_total=items_total,
            discount_type=discount_type,
            discount_value=discount_value,
        )

        # 10% of 400 = 40.00
        assert result == Decimal("40.00")

    @patch(
        "orders.interactors.order.place_order_interactor.transaction.atomic",
        no_op_lock,
    )
    @patch("orders.interactors.order.place_order_interactor.redis_lock", no_op_lock)
    def test_place_order_usage_at_limit_minus_one_should_succeed(self):
        self._setup_valid_adapters()
        promo_code = PromoCodeDTOFactory(
            promo_code_id=1,
            max_usage=5,
        )
        order_dto = OrderDTOFactory(order_id="orders-1")

        self.promo_code_storage.get_promo_code_by_id.return_value = promo_code
        self.order_storage.get_promo_code_usage.return_value = (
            4  # usage_count == max_usage - 1
        )
        self.order_storage.create_order.return_value = order_dto

        result = self.interactor.place_order(
            order_data=PlaceOrderDTOFactory(promo_code_id=1)
        )

        assert result.order_id == "orders-1"
