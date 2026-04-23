from contextlib import contextmanager
from datetime import datetime, time
from unittest.mock import patch

import pytest

from accounts.tests.factories.storage_factories import AddressFactory, UserFactory
from orders.tests.api_tests.order import BasePlaceOrderTestCase
from orders.tests.factories.storage_factories import OrderFactory, PromoCodeFactory
from restaurants.tests.factories.storage_factories import (
    CartFactory,
    CartItemFactory,
    DeliveryZoneFactory,
    MenuItemFactory,
    RestaurantFactory,
    RestaurantTimingFactory,
)


@contextmanager
def no_op_lock(*args, **kwargs):
    yield


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

    @patch("orders.interactors.orders.place_order_interactor.redis_lock", no_op_lock)
    def test_place_order_successfully(self, snapshot):
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

    def test_promo_code_not_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        self._create_customer_cart(user_id=user_id, restaurant=restaurant)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "addressId": 1,
                "promoCodeId": 999,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    @patch("orders.interactors.orders.place_order_interactor.redis_lock", no_op_lock)
    def test_promo_code_maximum_used(self, snapshot):
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
            max_usage=1,
        )
        OrderFactory(promo_code=promo_code, status="PLACED")

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

    def test_invalid_address_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        self._create_open_restaurant_timing(restaurant=restaurant)
        self._create_customer_cart(user_id=user_id, restaurant=restaurant)

        variables = {
            "params": {
                "restaurantId": restaurant_id,
                "addressId": 999,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_invalid_delivery_zone_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        user = UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        address = AddressFactory(id=1, user=user, pin_code="500001")
        self._create_open_restaurant_timing(restaurant=restaurant)
        self._create_customer_cart(user_id=user_id, restaurant=restaurant)

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

    def test_restaurant_day_timing_not_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        self._create_customer_cart(user_id=user_id, restaurant=restaurant)

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

    def test_restaurant_closed(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        restaurant = RestaurantFactory(id=restaurant_id)
        RestaurantTimingFactory(
            id=1,
            restaurant=restaurant,
            day_of_week=datetime.now().isoweekday(),
            open_time=time(0, 0),
            close_time=time(0, 1),
        )
        self._create_customer_cart(user_id=user_id, restaurant=restaurant)

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
