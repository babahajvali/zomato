from restaurants.exception.custom_exceptions import CartNotFound, CartItemNotFound
from restaurants.interactors.storage_interface.cart_storage_interface import (
    CartStorageInterface,
)


class CartMixin:
    @staticmethod
    def validate_cart_exists(cart_id: str, cart_storage: CartStorageInterface):

        cart_dto = cart_storage.get_cart(cart_id=cart_id)

        if not cart_dto:
            raise CartNotFound(cart_id=cart_id)

        return cart_dto

    @staticmethod
    def validate_cart_item_exists(
        cart_item_id: int, cart_storage: CartStorageInterface
    ):

        cart_item_dto = cart_storage.get_cart_item_by_id(cart_item_id=cart_item_id)

        if not cart_item_dto:
            raise CartItemNotFound(cart_item_id=cart_item_id)

        return cart_item_dto
