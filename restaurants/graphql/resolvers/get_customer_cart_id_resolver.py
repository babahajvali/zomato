from restaurants.graphql.types.types import CustomerCartIdType
from restaurants.interactors.cart.cart_item_interactor import CartItemInteractor
from restaurants.storages.cart_storage import CartStorage
from restaurants.storages.restaurant_storage import RestaurantStorage


def get_customer_cart_id_resolver(root, info):

    user_id = info.context.user_id

    cart_storage = CartStorage()
    restaurant_storage = RestaurantStorage()

    interactor = CartItemInteractor(
        restaurant_storage=restaurant_storage, cart_storage=cart_storage
    )

    cart_id = interactor.get_customer_cart_id(customer_id=user_id)

    return CustomerCartIdType(cart_id=cart_id)
