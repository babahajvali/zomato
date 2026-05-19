import pytest

from accounts.tests.factories.storage_factories import UserFactory
from restaurants.tests.api_tests.cart import BaseGetCartItemsTestCase
from restaurants.tests.factories.storage_factories import (
    CartFactory,
    RestaurantFactory,
    MenuItemFactory,
    CartItemFactory,
)


@pytest.mark.django_db
class TestGetCartItems(BaseGetCartItemsTestCase):
    def test_get_cart_items_with_valid_data_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        cart_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        CartFactory(id=cart_id, customer_id=user_id)
        menu_item_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id)
        MenuItemFactory(id=menu_item_id, restaurant_id=restaurant_id)
        CartItemFactory(id=1, cart_id=cart_id, menu_item_id=menu_item_id)

        variables = {"params": {"cartId": cart_id}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_cart_items_with_cart_not_found_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        cart_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        menu_item_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id)
        MenuItemFactory(id=menu_item_id, restaurant_id=restaurant_id)

        variables = {"params": {"cartId": cart_id}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_cart_items_with_cart_not_belongs_to_user_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)
        cart_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        CartFactory(id=cart_id)
        menu_item_id = "49bb508e-c6d1-4882-95fd-1991d103f7de"
        restaurant_id = "49bb508e-c6d1-4882-95fd-1991d103f7df"
        RestaurantFactory(id=restaurant_id)
        MenuItemFactory(id=menu_item_id, restaurant_id=restaurant_id)
        CartItemFactory(id=1, cart_id=cart_id, menu_item_id=menu_item_id)

        variables = {"params": {"cartId": cart_id}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id=user_id,
        )
