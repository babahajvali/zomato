from restaurants.exception.custom_exceptions import InvalidQuantity
from restaurants.interactors.dtos import CartItemDTO
from restaurants.interactors.storage_interface.cart_storage_interface import (
    CartStorageInterface,
)
from restaurants.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurants.mixins.cart_mixin import CartMixin
from restaurants.mixins.restaurant_mixin import RestaurantMixin


class CartItemInteractor(CartMixin, RestaurantMixin):
    def __init__(
        self,
        cart_storage: CartStorageInterface,
        restaurant_storage: RestaurantStorageInterface,
    ):
        super().__init__(
            cart_storage=cart_storage, restaurant_storage=restaurant_storage
        )
        self.cart_storage = cart_storage
        self.restaurant_storage = restaurant_storage

    def update_cart_item(
        self, cart_id: str, menu_item_id: str, quantity: int
    ) -> CartItemDTO:

        self.validate_cart_exists(cart_id=cart_id)
        self.validate_menu_item_exists(menu_item_id=menu_item_id)
        self._validate_quantity(quantity=quantity)

        menu_item_dto = self.restaurant_storage.get_menu_item(menu_item_id=menu_item_id)

        return self.cart_storage.create_or_update_cart_item(
            cart_id=cart_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            item_price=menu_item_dto.price,
        )

    def remove_cart_item(self, cart_item_id: int):
        self.validate_cart_item_exists(cart_item_id=cart_item_id)

        return self.cart_storage.remove_cart_item(cart_item_id=cart_item_id)

    def clear_cart_items(self, cart_id: str):
        self.validate_cart_exists(cart_id=cart_id)

        return self.cart_storage.clear_cart_items(cart_id=cart_id)

    def get_cart_items(self, cart_id: str):
        self.validate_cart_exists(cart_id=cart_id)

        return self.cart_storage.get_cart_items(cart_id=cart_id)

    def get_customer_cart_id(self, customer_id: str) -> str:

        return self.cart_storage.get_customer_cart_id(customer_id=customer_id)

    @staticmethod
    def _validate_quantity(quantity: int):
        if quantity <= 0 or quantity > 10:
            raise InvalidQuantity(quantity=quantity)
