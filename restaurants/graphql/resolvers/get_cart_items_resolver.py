from restaurants.exception import custom_exceptions
from restaurants.graphql.types.error_types import CartNotFound
from restaurants.graphql.types.types import CartItemsType, CartItemType
from restaurants.interactors.cart.cart_item_interactor import CartItemInteractor
from restaurants.storages.cart_storage import CartStorage
from restaurants.storages.restaurant_storage import RestaurantStorage


def get_cart_items_resolver(root, info, params):
    cart_storage = CartStorage()
    restaurant_storage = RestaurantStorage()

    interactor = CartItemInteractor(
        cart_storage=cart_storage,
        restaurant_storage=restaurant_storage,
    )

    try:
        # TODO: cart_id is client-supplied with no ownership check — any user can read any cart.
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
