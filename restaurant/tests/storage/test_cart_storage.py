import pytest
from restaurant.storages.cart_storage import CartStorage
from restaurant.tests.factories.storage_factories import (
    CartFactory,
    CartItemFactory,
    MenuItemFactory,
)


@pytest.mark.django_db
class TestCartStorage:
    def setup_method(self):
        self.storage = CartStorage()

    def test_create_carts_successfully(self):
        customer_ids = [
            "00000000-0000-0000-0000-000000000001",
            "00000000-0000-0000-0000-000000000002",
        ]

        result = self.storage.create_carts(customer_ids=customer_ids)

        assert len(result) == 2
        assert result[0].customer_id == customer_ids[0]
        assert result[1].customer_id == customer_ids[1]

    def test_create_carts_returns_cart_dto(self):
        customer_ids = ["00000000-0000-0000-0000-000000000001"]

        result = self.storage.create_carts(customer_ids=customer_ids)

        assert result[0].cart_id is not None
        assert result[0].customer_id == customer_ids[0]

    def test_get_cart_successfully(self):
        cart = CartFactory()

        result = self.storage.get_cart(cart_id=str(cart.id))

        assert result is not None
        assert result.cart_id == str(cart.id)
        assert result.customer_id == cart.customer_id

    def test_get_cart_returns_none_when_not_found(self):
        result = self.storage.get_cart(cart_id="invalid-cart-id")

        assert result is None

    def test_create_cart_item_when_not_exists(self):
        cart = CartFactory()
        menu_item = MenuItemFactory()

        result = self.storage.create_or_update_cart_item(
            cart_id=str(cart.id),
            menu_item_id=str(menu_item.id),
            quantity=2,
            item_price=199.0,
        )

        assert result.cart_id == str(cart.id)
        assert result.menu_item_id == str(menu_item.id)
        assert result.quantity == 2
        assert result.item_price == 199.0

    def test_update_cart_item_when_already_exists(self):
        cart_item = CartItemFactory(quantity=2, item_price=199.0)

        result = self.storage.create_or_update_cart_item(
            cart_id=str(cart_item.cart.id),
            menu_item_id=str(cart_item.menu_item.id),
            quantity=5,
            item_price=299.0,
        )

        assert result.quantity == 5
        assert result.item_price == 299.0

    def test_create_or_update_does_not_create_duplicate(self):
        from restaurant.models import CartItem

        cart_item = CartItemFactory(quantity=2)

        self.storage.create_or_update_cart_item(
            cart_id=str(cart_item.cart.id),
            menu_item_id=str(cart_item.menu_item.id),
            quantity=5,
            item_price=199.0,
        )

        count = CartItem.objects.filter(
            cart_id=cart_item.cart.id,
            menu_item_id=cart_item.menu_item.id,
        ).count()
        assert count == 1

    def test_get_cart_item_by_id_successfully(self):
        cart_item = CartItemFactory()

        result = self.storage.get_cart_item_by_id(cart_item_id=cart_item.pk)

        assert result is not None
        assert result.cart_item_id == cart_item.pk
        assert result.quantity == cart_item.quantity

    def test_get_cart_item_by_id_returns_none_when_not_found(self):
        result = self.storage.get_cart_item_by_id(cart_item_id=9999)

        assert result is None

    def test_remove_cart_item_successfully(self):
        from restaurant.models import CartItem

        cart_item = CartItemFactory()

        self.storage.remove_cart_item(cart_item_id=cart_item.pk)

        exists = CartItem.objects.filter(pk=cart_item.pk).exists()
        assert exists is False

    def test_remove_cart_item_non_existing_does_not_raise(self):
        self.storage.remove_cart_item(cart_item_id=9999)

    def test_clear_cart_items_successfully(self):
        from restaurant.models import CartItem

        cart = CartFactory()
        CartItemFactory(cart=cart)
        CartItemFactory(cart=cart)
        CartItemFactory(cart=cart)

        self.storage.clear_cart_items(cart_id=str(cart.id))

        count = CartItem.objects.filter(cart_id=cart.id).count()
        assert count == 0

    def test_clear_cart_items_only_clears_given_cart(self):
        from restaurant.models import CartItem

        cart_1 = CartFactory()
        cart_2 = CartFactory()

        CartItemFactory(cart=cart_1)
        CartItemFactory(cart=cart_1)
        CartItemFactory(cart=cart_2)

        self.storage.clear_cart_items(cart_id=str(cart_1.id))

        cart_1_count = CartItem.objects.filter(cart_id=cart_1.id).count()
        assert cart_1_count == 0

        cart_2_count = CartItem.objects.filter(cart_id=cart_2.id).count()
        assert cart_2_count == 1

    def test_clear_cart_items_empty_cart_does_not_raise(self):
        cart = CartFactory()

        self.storage.clear_cart_items(cart_id=str(cart.id))
