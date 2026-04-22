from restaurant.exception.custom_exceptions import InvalidQuantityFound
from restaurant.interactors.dtos import CartItemDTO
from restaurant.interactors.storage_interface.cart_storage_interface import (
    CartStorageInterface,
)
from restaurant.interactors.storage_interface.restaurant_storage_interface import (
    RestaurantStorageInterface,
)
from restaurant.mixins.cart_mixin import CartMixin
from restaurant.mixins.restaurant_mixin import RestaurantMixin


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

        self.check_cart_exists(cart_id=cart_id)
        self.validate_menu_item_exists(menu_item_id=menu_item_id)
        self._check_quantity(quantity=quantity)

        menu_item_dto = self.restaurant_storage.get_menu_item(menu_item_id=menu_item_id)

        return self.cart_storage.create_or_update_cart_item(
            cart_id=cart_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            item_price=menu_item_dto.price,
        )

    def remove_cart_item(self, cart_item_id: int):

        self.check_cart_item_exists(cart_item_id=cart_item_id)

        return self.cart_storage.remove_cart_item(cart_item_id=cart_item_id)

    def clear_cart_items(self, cart_id: str):
        self.check_cart_exists(cart_id=cart_id)

        return self.cart_storage.clear_cart_items(cart_id=cart_id)

    def get_cart_items(self, cart_id: str):
        self.check_cart_exists(cart_id=cart_id)

        return self.cart_storage.get_cart_items(cart_id=cart_id)

    @staticmethod
    def _check_quantity(quantity: int):
        if quantity <= 0 or quantity > 9:
            raise InvalidQuantityFound(quantity=quantity)
