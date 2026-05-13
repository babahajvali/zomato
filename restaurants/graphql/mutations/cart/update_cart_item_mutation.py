import graphene

from restaurants.exception import custom_exceptions
from restaurants.graphql.types.error_types import (
    CartNotFound,
    MenuItemNotFound,
    InvalidQuantity,
)
from restaurants.graphql.types.input_types import UpdateCartItemInputParams
from restaurants.graphql.types.response_types import UpdateCartItemResponse
from restaurants.graphql.types.types import CartItemType
from restaurants.interactors.cart.cart_item_interactor import CartItemInteractor
from restaurants.storages.cart_storage import CartStorage
from restaurants.storages.restaurant_storage import RestaurantStorage


class UpdateCartItemMutation(graphene.Mutation):
    class Arguments:
        params = UpdateCartItemInputParams(required=True)

    Output = UpdateCartItemResponse

    @staticmethod
    def mutate(root, info, params):
        cart_storage = CartStorage()
        restaurant_storage = RestaurantStorage()

        interactor = CartItemInteractor(
            cart_storage=cart_storage,
            restaurant_storage=restaurant_storage,
        )

        try:
            # TODO: cart_id is client-supplied with no ownership check — any user can mutate any cart.
            result = interactor.update_cart_item(
                cart_id=params.cart_id,
                menu_item_id=params.menu_item_id,
                quantity=params.quantity,
            )

            return CartItemType(
                cart_item_id=result.cart_item_id,
                cart_id=result.cart_id,
                menu_item_id=result.menu_item_id,
                quantity=result.quantity,
                item_price=result.item_price,
            )

        except custom_exceptions.CartNotFound as e:
            return CartNotFound(cart_id=e.cart_id)
        except custom_exceptions.MenuItemNotFound as e:
            return MenuItemNotFound(menu_item_id=e.menu_item_id)
        except custom_exceptions.InvalidQuantity as e:
            return InvalidQuantity(quantity=e.quantity)
