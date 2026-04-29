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

    def test_update_cart_item_successfully(self):
        menu_item = MenuItemDTOFactory(id="item-123", price=350.0)
        cart_item = CartItemDTOFactory(
            cart_id="cart-123",
            menu_item_id="item-123",
            quantity=2,
            item_price=350.0,
        )

        self.cart_storage.get_cart.return_value = CartDTOFactory(cart_id="cart-123")
        self.restaurant_storage.get_menu_item.return_value = menu_item
        self.cart_storage.create_or_update_cart_item.return_value = cart_item

        result = self.interactor.update_cart_item(
            cart_id="cart-123",
            menu_item_id="item-123",
            quantity=2,
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

    def test_update_cart_item_raises_cart_not_found(self):
        self.cart_storage.get_cart.return_value = None

        with pytest.raises(CartNotFound) as exc:
            self.interactor.update_cart_item(
                cart_id="invalid-cart",
                menu_item_id="item-123",
                quantity=2,
            )

        assert exc.value.cart_id == "invalid-cart"
        self.cart_storage.create_or_update_cart_item.assert_not_called()

    def test_update_cart_item_raises_menu_item_not_found(self):
        self.cart_storage.get_cart.return_value = CartDTOFactory(cart_id="cart-123")
        self.restaurant_storage.get_menu_item.return_value = None

        with pytest.raises(MenuItemNotFound):
            self.interactor.update_cart_item(
                cart_id="cart-123",
                menu_item_id="invalid-item",
                quantity=2,
            )

        self.cart_storage.create_or_update_cart_item.assert_not_called()

    def test_update_cart_item_raises_invalid_quantity_when_zero(self):
        self.cart_storage.get_cart.return_value = CartDTOFactory(cart_id="cart-123")
        self.restaurant_storage.get_menu_item.return_value = MenuItemDTOFactory()

        with pytest.raises(InvalidQuantity) as exc:
            self.interactor.update_cart_item(
                cart_id="cart-123",
                menu_item_id="item-123",
                quantity=0,
            )

        assert exc.value.quantity == 0
        self.cart_storage.create_or_update_cart_item.assert_not_called()

    def test_update_cart_item_raises_invalid_quantity_when_exceeds_limit(self):
        self.cart_storage.get_cart.return_value = CartDTOFactory(cart_id="cart-123")
        self.restaurant_storage.get_menu_item.return_value = MenuItemDTOFactory()

        with pytest.raises(InvalidQuantity) as exc:
            self.interactor.update_cart_item(
                cart_id="cart-123",
                menu_item_id="item-123",
                quantity=11,
            )

        assert exc.value.quantity == 11
        self.cart_storage.create_or_update_cart_item.assert_not_called()

    def test_update_cart_item_with_max_valid_quantity(self):
        menu_item = MenuItemDTOFactory(id="item-123", price=350.0)
        cart_item = CartItemDTOFactory(
            cart_id="cart-123",
            menu_item_id="item-123",
            quantity=9,
            item_price=350.0,
        )

        self.cart_storage.get_cart.return_value = CartDTOFactory(cart_id="cart-123")
        self.restaurant_storage.get_menu_item.return_value = menu_item
        self.cart_storage.create_or_update_cart_item.return_value = cart_item

        result = self.interactor.update_cart_item(
            cart_id="cart-123",
            menu_item_id="item-123",
            quantity=9,
        )

        assert result.quantity == 9

    def test_remove_cart_item_successfully(self):
        self.cart_storage.get_cart_item_by_id.return_value = CartItemDTOFactory(
            cart_item_id=1
        )
        self.cart_storage.remove_cart_item.return_value = None

        self.interactor.remove_cart_item(cart_item_id=1)

        self.cart_storage.remove_cart_item.assert_called_once_with(cart_item_id=1)

    def test_remove_cart_item_raises_cart_item_not_found(self):
        self.cart_storage.get_cart_item_by_id.return_value = None

        with pytest.raises(CartItemNotFound) as exc:
            self.interactor.remove_cart_item(cart_item_id=999)

        assert exc.value.cart_item_id == 999
        self.cart_storage.remove_cart_item.assert_not_called()

    def test_clear_cart_items_successfully(self):
        self.cart_storage.get_cart.return_value = CartDTOFactory(cart_id="cart-123")
        self.cart_storage.clear_cart_items.return_value = None

        self.interactor.clear_cart_items(cart_id="cart-123")

        self.cart_storage.clear_cart_items.assert_called_once_with(cart_id="cart-123")

    def test_clear_cart_items_raises_cart_not_found(self):
        self.cart_storage.get_cart.return_value = None

        with pytest.raises(CartNotFound) as exc:
            self.interactor.clear_cart_items(cart_id="invalid-cart")

        assert exc.value.cart_id == "invalid-cart"
        self.cart_storage.clear_cart_items.assert_not_called()
