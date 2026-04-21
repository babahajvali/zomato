from restaurant.exception import custom_exceptions
from restaurant.graphql.types.error_types import CartNotFound
from restaurant.graphql.types.types import CartItemsType, CartItemType
from restaurant.interactors.cart.cart_item_interactor import CartItemInteractor
from restaurant.storages.cart_storage import CartStorage
from restaurant.storages.restaurant_storage import RestaurantStorage


def get_cart_items_resolver(root, info, params):
    cart_storage = CartStorage()
    restaurant_storage = RestaurantStorage()

    interactor = CartItemInteractor(
        cart_storage=cart_storage,
        restaurant_storage=restaurant_storage,
    )

    try:
        cart_items = interactor.get_cart_items(cart_id=params.cart_id)

        items = [
            CartItemType(
                cart_item_id=item.cart_item_id,
                cart_id=item.cart_id,
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
                item_price=item.item_price,
            )
            for item in cart_items
        ]

        return CartItemsType(cart_items=items)
    except custom_exceptions.CartNotFound as e:
        return CartNotFound(cart_id=e.cart_id)
