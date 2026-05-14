from contextlib import contextmanager
from datetime import datetime, time, timedelta
from unittest.mock import patch

import factory.random
import pytest
from django.core.cache import cache
from django.utils import timezone

from accounts.tests.factories.storage_factories import AddressFactory, UserFactory
from orders.models import Order
from orders.tests.api_tests.order import BasePlaceScheduledOrderTestCase
from orders.tests.factories.storage_factories import PromoCodeFactory
from restaurants.tests.factories.storage_factories import (
    CartFactory,
    CartItemFactory,
    DeliveryZoneFactory,
    MenuItemFactory,
    RestaurantFactory,
    RestaurantTimingFactory,
)

factory.random.reseed_random(123)


@contextmanager
def no_op_lock(*args, **kwargs):
    yield


def patch_created_order(order_id: str, placed_at, monkeypatch):
    order_id_field = Order._meta.get_field("id")
    monkeypatch.setattr(order_id_field, "default", lambda order_id=order_id: order_id)
    monkeypatch.setattr(timezone, "now", lambda: placed_at)


@pytest.mark.django_db
class TestPlaceScheduledOrderApi(BasePlaceScheduledOrderTestCase):
    def setup_method(self):
        cache.clear()

    def _create_customer_cart(self, user_id, restaurant, is_available=True):
        cart = CartFactory(
            id="49bb508e-c6d1-4882-95fd-1991d103f7dd",
            customer_id=user_id,
        )
        menu_item = MenuItemFactory(
            id="49bb508e-c6d1-4882-95fd-1991d103f7de",
            restaurant=restaurant,
            price=200.0,
            is_available=is_available,
        )
        CartItemFactory(
            id=1,
            cart=cart,
            menu_item=menu_item,
            quantity=2,
            item_price=200.0,
        )
        return cart

    def _create_restaurant_timing(self, restaurant, scheduled_for):
        RestaurantTimingFactory(
            id=1,
            restaurant=restaurant,
            day_of_week=scheduled_for.isoweekday(),
            open_time=time(0, 0),
            close_time=time(23, 59),
        )

    @patch(
        "orders.interactors.order.place_scheduled_order_interactor.redis_lock",
        no_op_lock,
    )
    def test_place_scheduled_order_successfully(self, snapshot, monkeypatch):
        placed_at = datetime.fromisoformat("2026-05-05T10:00:00+00:00")
        scheduled_for = datetime.fromisoformat("2026-05-05T12:00:00+00:00")
        patch_created_order(
            order_id="fa8b56e4-6af4-4c44-982f-6dad6b10f7ef",
            placed_at=placed_at,
            monkeypatch=monkeypatch,
        )
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        user = UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        address = AddressFactory(id=1, user=user, pincode="500001")
        DeliveryZoneFactory(
            id=1,
            restaurant=restaurant,
            pin_code="500001",
            delivery_fee=30.0,
        )
        self._create_restaurant_timing(
            restaurant=restaurant, scheduled_for=scheduled_for
        )
        self._create_customer_cart(user_id=user_id, restaurant=restaurant)

        promo_code = PromoCodeFactory(
            id=1,
            discount_type="FLAT",
            discount_value=50.0,
            min_order_value=100.0,
            max_usage=10,
            valid_from=placed_at - timedelta(days=1),
            valid_until=placed_at + timedelta(days=1),
        )

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "addressId": address.id,
                "scheduledFor": scheduled_for.isoformat(),
                "promoCodeId": promo_code.id,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_place_scheduled_order_time_too_soon(self, snapshot, monkeypatch):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        placed_at = datetime.fromisoformat("2026-05-05T10:00:00+00:00")
        monkeypatch.setattr(timezone, "now", lambda: placed_at)
        scheduled_for = placed_at + timedelta(minutes=10)

        variables = {
            "params": {
                "restaurantId": "49bb508e-c6d1-4882-95fd-1991d103f7df",
                "addressId": 1,
                "scheduledFor": scheduled_for.isoformat(),
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_place_scheduled_order_restaurant_not_open_at_scheduled_time(
        self, snapshot
    ):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        scheduled_for = datetime.fromisoformat("2026-05-05T12:00:00+00:00")

        variables = {
            "params": {
                "restaurantId": "49bb508e-c6d1-4882-95fd-1991d103f7df",
                "addressId": 1,
                "scheduledFor": scheduled_for.isoformat(),
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch(
        "orders.interactors.order.place_scheduled_order_interactor.redis_lock",
        no_op_lock,
    )
    def test_place_scheduled_order_menu_items_unavailable(self, snapshot, monkeypatch):
        placed_at = datetime.fromisoformat("2026-05-05T10:00:00+00:00")
        scheduled_for = datetime.fromisoformat("2026-05-05T12:00:00+00:00")
        patch_created_order(
            order_id="0eb1ee11-2d95-4021-b66f-4a06b33d3c8c",
            placed_at=placed_at,
            monkeypatch=monkeypatch,
        )
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        user = UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        address = AddressFactory(id=1, user=user, pincode="500001")
        DeliveryZoneFactory(
            id=1,
            restaurant=restaurant,
            pin_code="500001",
            delivery_fee=30.0,
        )
        self._create_restaurant_timing(
            restaurant=restaurant, scheduled_for=scheduled_for
        )
        self._create_customer_cart(
            user_id=user_id, restaurant=restaurant, is_available=False
        )

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "addressId": address.id,
                "scheduledFor": scheduled_for.isoformat(),
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
