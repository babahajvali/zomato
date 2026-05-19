from unittest.mock import create_autospec

import pytest

from restaurants.exception.custom_exceptions import (
    CartNotFound,
    CartItemNotFound,
    InvalidQuantity,
    MenuItemNotFound,
)
from restaurants.interactors.cart.cart_item_interactor import CartItemInteractor
from restaurants.interactors.storage_interface.cart_storage_interface import (
    CartStorageInterface,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.tests.factories.interactor_factories import (
    CartDTOFactory,
    CartItemDTOFactory,
    MenuItemDTOFactory,
)


class TestCartItemInteractor:
    def setup_method(self):
        self.cart_storage = create_autospec(CartStorageInterface)
        self.restaurant_storage = create_autospec(RestaurantStorageInterface)
        self.interactor = CartItemInteractor(
            cart_storage=self.cart_storage,
            restaurant_storage=self.restaurant_storage,
        )

    def test_update_cart_item_with_valid_data_success(self):
        menu_item = MenuItemDTOFactory(id="item-123", price=350.0)
        user_id = "user-1"
        cart_item = CartItemDTOFactory(
            cart_id="cart-123",
            menu_item_id="item-123",
            quantity=2,
            item_price=350.0,
        )

        cart = CartDTOFactory(cart_id="cart-123", customer_id=user_id)
        self.cart_storage.get_cart.return_value = cart

        self.restaurant_storage.get_menu_item.return_value = menu_item
        self.cart_storage.create_or_update_cart_item.return_value = cart_item

        result = self.interactor.update_cart_item(
            cart_id="cart-123",
            menu_item_id="item-123",
            quantity=2,
            user_id=user_id,
        )

        assert result.cart_id == "cart-123"
        assert result.menu_item_id == "item-123"
        assert result.quantity == 2
        assert result.item_price == 350.0
        self.cart_storage.create_or_update_cart_item.assert_called_once_with(
            cart_id="cart-123",
            menu_item_id="item-123",
            quantity=2,
            item_price=menu_item.price,
        )

    def test_update_cart_item_with_cart_not_found_raises_error(self):
        self.cart_storage.get_cart.return_value = None

        with pytest.raises(CartNotFound) as exc:
            self.interactor.update_cart_item(
                cart_id="invalid-cart",
                menu_item_id="item-123",
                quantity=2,
                user_id="user_id",
            )

        assert exc.value.cart_id == "invalid-cart"
        self.cart_storage.create_or_update_cart_item.assert_not_called()

    def test_update_cart_item_with_menu_item_not_found_raises_error(self):
        cart = CartDTOFactory(cart_id="cart-123")
        self.cart_storage.get_cart.return_value = cart
        self.restaurant_storage.get_menu_item.return_value = None

        with pytest.raises(MenuItemNotFound):
            self.interactor.update_cart_item(
                cart_id="cart-123",
                menu_item_id="invalid-item",
                quantity=2,
                user_id=cart.customer_id,
            )

        self.cart_storage.create_or_update_cart_item.assert_not_called()

    def test_update_cart_item_with_invalid_quantity_when_zero_raises_error(self):
        cart = CartDTOFactory(cart_id="cart-123")
        self.cart_storage.get_cart.return_value = cart
        self.restaurant_storage.get_menu_item.return_value = MenuItemDTOFactory()

        with pytest.raises(InvalidQuantity) as exc:
            self.interactor.update_cart_item(
                cart_id="cart-123",
                menu_item_id="item-123",
                quantity=0,
                user_id=cart.customer_id,
            )

        assert exc.value.quantity == 0
        self.cart_storage.create_or_update_cart_item.assert_not_called()

    def test_update_cart_item_with_invalid_quantity_when_exceeds_limit_raises_error(self):
        cart = CartDTOFactory(cart_id="cart-123")
        self.cart_storage.get_cart.return_value = cart
        self.restaurant_storage.get_menu_item.return_value = MenuItemDTOFactory()

        with pytest.raises(InvalidQuantity) as exc:
            self.interactor.update_cart_item(
                cart_id="cart-123",
                menu_item_id="item-123",
                quantity=11,
                user_id=cart.customer_id,
            )

        assert exc.value.quantity == 11
        self.cart_storage.create_or_update_cart_item.assert_not_called()

    def test_update_cart_item_with_max_valid_quantity_success(self):
        menu_item = MenuItemDTOFactory(id="item-123", price=350.0)
        cart_item = CartItemDTOFactory(
            cart_id="cart-123",
            menu_item_id="item-123",
            quantity=9,
            item_price=350.0,
        )
        cart = CartDTOFactory(cart_id="cart-123")
        self.cart_storage.get_cart.return_value = cart
        self.restaurant_storage.get_menu_item.return_value = menu_item
        self.cart_storage.create_or_update_cart_item.return_value = cart_item

        result = self.interactor.update_cart_item(
            cart_id="cart-123",
            menu_item_id="item-123",
            quantity=9,
            user_id=cart.customer_id,
        )

        assert result.quantity == 9

    def test_remove_cart_item_with_valid_data_success(self):
        cart = CartDTOFactory(cart_id="cart-123", customer_id="customer_id")
        self.cart_storage.get_cart_item_by_id.return_value = CartItemDTOFactory(
            cart_item_id=1, cart_id=cart.cart_id
        )
        self.cart_storage.get_cart.return_value = cart
        self.cart_storage.remove_cart_item.return_value = None

        self.interactor.remove_cart_item(cart_item_id=1, user_id=cart.customer_id)

        self.cart_storage.remove_cart_item.assert_called_once_with(cart_item_id=1)

    def test_remove_cart_item_with_cart_item_not_found_raises_error(self):
        self.cart_storage.get_cart_item_by_id.return_value = None

        with pytest.raises(CartItemNotFound) as exc:
            self.interactor.remove_cart_item(cart_item_id=999, user_id="Sample1")

        assert exc.value.cart_item_id == 999
        self.cart_storage.remove_cart_item.assert_not_called()

    def test_clear_cart_items_with_valid_data_success(self):
        cart = CartDTOFactory(cart_id="cart-123")
        self.cart_storage.get_cart.return_value = cart
        self.cart_storage.clear_cart_items.return_value = None

        self.interactor.clear_cart_items(cart_id="cart-123", user_id=cart.customer_id)

        self.cart_storage.clear_cart_items.assert_called_once_with(cart_id="cart-123")

    def test_clear_cart_items_with_cart_not_found_raises_error(self):
        self.cart_storage.get_cart.return_value = None

        with pytest.raises(CartNotFound) as exc:
            self.interactor.clear_cart_items(cart_id="invalid-cart", user_id="baba")

        assert exc.value.cart_id == "invalid-cart"
        self.cart_storage.clear_cart_items.assert_not_called()

    def test_update_cart_item_with_min_valid_quantity_success(self):
        menu_item = MenuItemDTOFactory(id="item-123", price=350.0)
        cart_item = CartItemDTOFactory(
            cart_id="cart-123",
            menu_item_id="item-123",
            quantity=1,
            item_price=350.0,
        )
        cart = CartDTOFactory(cart_id="cart-123")
        self.cart_storage.get_cart.return_value = cart
        self.restaurant_storage.get_menu_item.return_value = menu_item
        self.cart_storage.create_or_update_cart_item.return_value = cart_item

        result = self.interactor.update_cart_item(
            cart_id="cart-123",
            menu_item_id="item-123",
            quantity=1,
            user_id=cart.customer_id,
        )

        assert result.quantity == 1
        self.cart_storage.create_or_update_cart_item.assert_called_once_with(
            cart_id="cart-123",
            menu_item_id="item-123",
            quantity=1,
            item_price=menu_item.price,
        )

    def test_update_cart_item_with_max_valid_quantity_10_success(self):
        menu_item = MenuItemDTOFactory(id="item-123", price=350.0)
        cart_item = CartItemDTOFactory(
            cart_id="cart-123",
            menu_item_id="item-123",
            quantity=10,
            item_price=350.0,
        )

        cart = CartDTOFactory(cart_id="cart-123")
        self.cart_storage.get_cart.return_value = cart
        self.restaurant_storage.get_menu_item.return_value = menu_item
        self.cart_storage.create_or_update_cart_item.return_value = cart_item

        result = self.interactor.update_cart_item(
            cart_id="cart-123",
            menu_item_id="item-123",
            quantity=10,
            user_id=cart.customer_id,
        )

        assert result.quantity == 10
        self.cart_storage.create_or_update_cart_item.assert_called_once_with(
            cart_id="cart-123",
            menu_item_id="item-123",
            quantity=10,
            item_price=menu_item.price,
        )

    def test_get_cart_items_with_valid_data_success(self):
        # Test get_cart_items() method
        cart_items = [
            CartItemDTOFactory(
                cart_id="cart-123",
                menu_item_id="item-1",
                quantity=2,
                item_price=350.0,
            ),
            CartItemDTOFactory(
                cart_id="cart-123",
                menu_item_id="item-2",
                quantity=1,
                item_price=200.0,
            ),
        ]

        cart = CartDTOFactory(cart_id="cart-123")
        self.cart_storage.get_cart.return_value = cart
        self.cart_storage.get_cart_items.return_value = cart_items

        result = self.interactor.get_cart_items(
            cart_id="cart-123", user_id=cart.customer_id
        )

        assert len(result) == 2
        assert result[0].menu_item_id == "item-1"
        assert result[0].quantity == 2
        assert result[1].menu_item_id == "item-2"
        assert result[1].quantity == 1
        self.cart_storage.get_cart_items.assert_called_once_with(cart_id="cart-123")

    def test_get_cart_items_with_cart_not_found_raises_error(self):
        self.cart_storage.get_cart.return_value = None

        with pytest.raises(CartNotFound) as exc:
            self.interactor.get_cart_items(cart_id="invalid-cart", user_id="baba")

        assert exc.value.cart_id == "invalid-cart"
        self.cart_storage.get_cart_items.assert_not_called()

    def test_get_customer_cart_id_with_valid_data_success(self):
        self.cart_storage.get_customer_cart_id.return_value = "cart-123"

        result = self.interactor.get_customer_cart_id(customer_id="customer-1")

        assert result == "cart-123"
        self.cart_storage.get_customer_cart_id.assert_called_once_with(
            customer_id="customer-1"
        )
