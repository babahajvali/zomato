from restaurants.exception.custom_exceptions import CartNotFound, CartItemNotFound
from restaurants.interactors.storage_interface.cart_storage_interface import (
    CartStorageInterface,
)


class CartMixin:
    def __init__(self, cart_storage: CartStorageInterface, **kwargs):
        self.cart_storage = cart_storage
        super().__init__(**kwargs)

    def validate_cart_exists(self, cart_id: str):

        cart_dto = self.cart_storage.get_cart(cart_id=cart_id)

        if not cart_dto:
            raise CartNotFound(cart_id=cart_id)

        return cart_dto

    def validate_cart_item_exists(self, cart_item_id: int):

        cart_item_dto = self.cart_storage.get_cart_item_by_id(cart_item_id=cart_item_id)

        if not cart_item_dto:
            raise CartItemNotFound(cart_item_id=cart_item_id)

        return cart_item_dto
