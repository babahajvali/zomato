from contextlib import contextmanager
from datetime import datetime, time, timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone

from accounts.tests.factories.storage_factories import AddressFactory, UserFactory
from orders.models import Order
from orders.tests.api_tests.order import BasePlaceOrderTestCase
from orders.tests.factories.storage_factories import PromoCodeFactory
from restaurants.tests.factories.storage_factories import (
    CartFactory,
    CartItemFactory,
    DeliveryZoneFactory,
    MenuItemFactory,
    RestaurantFactory,
    RestaurantTimingFactory,
)

import factory.random

factory.random.reseed_random(123)


@contextmanager
def no_op_lock(*args, **kwargs):
    yield


def patch_created_order(order_id: str, placed_at, monkeypatch):
    order_id_field = Order._meta.get_field("id")
    monkeypatch.setattr(order_id_field, "default", lambda order_id=order_id: order_id)
    monkeypatch.setattr(timezone, "now", lambda: placed_at)


@pytest.mark.django_db
class TestPlaceOrderApi(BasePlaceOrderTestCase):
    def _create_customer_cart(self, user_id, restaurant):
        cart = CartFactory(
            id="49bb508e-c6d1-4882-95fd-1991d103f7dd",
            customer_id=user_id,
        )
        menu_item = MenuItemFactory(
            id="49bb508e-c6d1-4882-95fd-1991d103f7de",
            restaurant=restaurant,
            price=200.0,
        )
        CartItemFactory(
            id=1,
            cart=cart,
            menu_item=menu_item,
            quantity=2,
            item_price=200.0,
        )
        return cart

    def _create_open_restaurant_timing(self, restaurant):
        RestaurantTimingFactory(
            id=1,
            restaurant=restaurant,
            day_of_week=datetime.now().isoweekday(),
            open_time=time(0, 0),
            close_time=time(23, 59),
        )

    @patch("orders.interactors.order.place_order_interactor.redis_lock", no_op_lock)
    def test_place_order_with_flat_promo_code_successfully(self, snapshot, monkeypatch):
        placed_at = datetime.fromisoformat("2026-04-27T04:00:07.483027+00:00")
        patch_created_order(
            order_id="2a174989-0c91-4ccd-ad46-cacebe226e1d",
            placed_at=placed_at,
            monkeypatch=monkeypatch,
        )
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        user = UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        address = AddressFactory(id=1, user=user, pin_code="500001")
        DeliveryZoneFactory(
            id=1,
            restaurant=restaurant,
            pin_code="500001",
            delivery_fee=30.0,
        )
        self._create_open_restaurant_timing(restaurant=restaurant)
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
                "promoCodeId": promo_code.id,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch("orders.interactors.order.place_order_interactor.redis_lock", no_op_lock)
    def test_place_order_with_percentage_promo_code_successfully(
        self, snapshot, monkeypatch
    ):
        placed_at = datetime.fromisoformat("2026-04-27T04:00:07.508492+00:00")
        patch_created_order(
            order_id="780a5a46-0bad-4459-b166-d1da57c2a5c6",
            placed_at=placed_at,
            monkeypatch=monkeypatch,
        )
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        user = UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        address = AddressFactory(id=1, user=user, pin_code="500001")
        DeliveryZoneFactory(
            id=1,
            restaurant=restaurant,
            pin_code="500001",
            delivery_fee=30.0,
        )
        self._create_open_restaurant_timing(restaurant=restaurant)
        self._create_customer_cart(user_id=user_id, restaurant=restaurant)

        promo_code = PromoCodeFactory(
            id=1,
            discount_type="PERCENTAGE",
            discount_value=10.0,
            min_order_value=100.0,
            max_usage=10,
            valid_from=placed_at - timedelta(days=1),
            valid_until=placed_at + timedelta(days=1),
        )

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "addressId": address.id,
                "promoCodeId": promo_code.id,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch("orders.interactors.order.place_order_interactor.redis_lock", no_op_lock)
    def test_promo_code_not_eligible_min_order_value(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        user = UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        address = AddressFactory(id=1, user=user, pin_code="500001")
        DeliveryZoneFactory(
            id=1,
            restaurant=restaurant,
            pin_code="500001",
            delivery_fee=30.0,
        )
        self._create_open_restaurant_timing(restaurant=restaurant)

        cart = CartFactory(
            id="49bb508e-c6d1-4882-95fd-1991d103f7dd",
            customer_id=user_id,
        )
        menu_item = MenuItemFactory(
            id="49bb508e-c6d1-4882-95fd-1991d103f7de",
            restaurant=restaurant,
            price=50.0,
        )
        CartItemFactory(
            id=1,
            cart=cart,
            menu_item=menu_item,
            quantity=1,
            item_price=50.0,
        )

        promo_code = PromoCodeFactory(
            id=1,
            discount_type="FLAT",
            discount_value=10.0,
            min_order_value=200.0,
            max_usage=10,
        )

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "addressId": address.id,
                "promoCodeId": promo_code.id,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_empty_cart_items_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        self._create_open_restaurant_timing(restaurant=restaurant)

        CartFactory(
            id="49bb508e-c6d1-4882-95fd-1991d103f7dd",
            customer_id=user_id,
        )

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "addressId": 1,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch("orders.interactors.order.place_order_interactor.redis_lock", no_op_lock)
    def test_place_order_with_multiple_items_successfully(self, snapshot, monkeypatch):
        patch_created_order(
            order_id="454a5524-cf0a-4a67-be1a-16b4dea2ae91",
            placed_at=datetime.fromisoformat("2026-04-27T04:00:07.562308+00:00"),
            monkeypatch=monkeypatch,
        )
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        user = UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        address = AddressFactory(id=1, user=user, pin_code="500001")
        DeliveryZoneFactory(
            id=1,
            restaurant=restaurant,
            pin_code="500001",
            delivery_fee=30.0,
        )
        self._create_open_restaurant_timing(restaurant=restaurant)

        cart = CartFactory(
            id="49bb508e-c6d1-4882-95fd-1991d103f7dd",
            customer_id=user_id,
        )
        menu_item1 = MenuItemFactory(
            id="49bb508e-c6d1-4882-95fd-1991d103f7de",
            restaurant=restaurant,
            price=200.0,
        )
        menu_item2 = MenuItemFactory(
            id="49bb508e-c6d1-4882-95fd-1991d103f7df",
            restaurant=restaurant,
            price=150.0,
        )
        CartItemFactory(
            id=1,
            cart=cart,
            menu_item=menu_item1,
            quantity=2,
            item_price=200.0,
        )
        CartItemFactory(
            id=2,
            cart=cart,
            menu_item=menu_item2,
            quantity=1,
            item_price=150.0,
        )

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "addressId": address.id,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
