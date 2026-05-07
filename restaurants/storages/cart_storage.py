from decimal import Decimal
from typing import List

from restaurants.interactors.dtos import CartDTO, CartItemDTO
from restaurants.interactors.storage_interface.cart_storage_interface import (
    CartStorageInterface,
)
from restaurants.models import Cart, CartItem


class CartStorage(CartStorageInterface):
    @staticmethod
    def _convert_to_cart_dto(cart_obj: Cart) -> CartDTO:
        return CartDTO(
            cart_id=cart_obj.id,
            customer_id=cart_obj.customer_id,
        )

    @staticmethod
    def _convert_to_cart_item_dto(cart_item_obj: CartItem) -> CartItemDTO:
        return CartItemDTO(
            cart_item_id=cart_item_obj.pk,
            cart_id=str(cart_item_obj.cart_id),
            menu_item_id=str(cart_item_obj.menu_item_id),
            quantity=cart_item_obj.quantity,
            item_price=Decimal(cart_item_obj.item_price),
        )

    def create_carts(self, customer_ids: list[str]) -> List[CartDTO]:
        carts = [
            Cart(
                customer_id=customer_id,
            )
            for customer_id in customer_ids
        ]

        created_carts = Cart.objects.bulk_create(carts)

        return [self._convert_to_cart_dto(cart_obj=each) for each in created_carts]

    def get_cart(self, cart_id: str) -> CartDTO | None:

        cart_dto = Cart.objects.filter(id=cart_id).first()
        if cart_dto is None:
            return None

        return self._convert_to_cart_dto(cart_obj=cart_dto)

    def create_or_update_cart_item(
        self, cart_id: str, menu_item_id: str, quantity: int, item_price=float
    ) -> CartItemDTO:

        cart_item, _ = CartItem.objects.update_or_create(
            cart_id=cart_id,
            menu_item_id=menu_item_id,
            defaults={
                "quantity": quantity,
                "item_price": item_price,
            },
        )

        return self._convert_to_cart_item_dto(cart_item_obj=cart_item)

    def get_cart_item_by_id(self, cart_item_id: int) -> CartItemDTO | None:

        cart_item_obj = CartItem.objects.filter(id=cart_item_id).first()

        if cart_item_obj is None:
            return None

        return self._convert_to_cart_item_dto(cart_item_obj=cart_item_obj)

    def remove_cart_item(self, cart_item_id: int):
        return CartItem.objects.filter(id=cart_item_id).delete()

    def clear_cart_items(self, cart_id: str):
        return CartItem.objects.filter(cart_id=cart_id).delete()

    def get_cart_items(self, cart_id: str) -> List[CartItemDTO]:
        cart_items = CartItem.objects.filter(cart_id=cart_id)

        return [
            self._convert_to_cart_item_dto(cart_item_obj=each) for each in cart_items
        ]

    def get_customer_cart_id(self, customer_id: str) -> str:
        cart = Cart.objects.filter(customer_id=customer_id).first()
        if cart is None:
            cart = Cart.objects.create(customer_id=customer_id)
        return cart.id
