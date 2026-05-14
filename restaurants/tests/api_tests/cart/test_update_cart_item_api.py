import pytest

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.cart import BaseUpdateCartItemTestCase
from restaurants.tests.factories.storage_factories import (
    CartFactory,
    MenuItemFactory,
    RestaurantFactory,
)


@pytest.mark.django_db
class TestUpdateCartItemApi(BaseUpdateCartItemTestCase):
    def test_update_cart_item(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        cart_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        CartFactory(id=cart_id, customer_id=user_id)
        menu_item_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id)
        MenuItemFactory(id=menu_item_id, restaurant_id=restaurant_id)

        variables = {
            "params": {
                "cartId": cart_id,
                "menuItemId": menu_item_id,
                "quantity": 1,
            }
        }
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_cart_not_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        cart_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        menu_item_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id)
        MenuItemFactory(id=menu_item_id, restaurant_id=restaurant_id)

        variables = {
            "params": {
                "cartId": cart_id,
                "menuItemId": menu_item_id,
                "quantity": 1,
            }
        }
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_menu_item_not_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        cart_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        CartFactory(id=cart_id, customer_id=user_id)
        menu_item_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id)

        variables = {
            "params": {
                "cartId": cart_id,
                "menuItemId": menu_item_id,
                "quantity": 1,
            }
        }
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_invalid_quantity_found(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        cart_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        CartFactory(id=cart_id, customer_id=user_id)
        menu_item_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id)
        MenuItemFactory(id=menu_item_id, restaurant_id=restaurant_id)

        variables = {
            "params": {
                "cartId": cart_id,
                "menuItemId": menu_item_id,
                "quantity": 0,
            }
        }
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_cart_not_belongs_to_user(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        cart_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        CartFactory(id=cart_id)
        menu_item_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id)
        MenuItemFactory(id=menu_item_id, restaurant_id=restaurant_id)

        variables = {
            "params": {
                "cartId": cart_id,
                "menuItemId": menu_item_id,
                "quantity": 0,
            }
        }
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
