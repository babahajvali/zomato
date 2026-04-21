import graphene

from restaurant.exception import custom_exceptions
from restaurant.graphql.types.error_types import (
    CartNotFound,
    MenuItemNotFound,
    InvalidQuantity,
)
from restaurant.graphql.types.input_types import UpdateCartItemInputParams
from restaurant.graphql.types.response_types import UpdateCartItemResponse
from restaurant.graphql.types.types import CartItemType
from restaurant.interactors.cart.cart_item_interactor import CartItemInteractor
from restaurant.storages.cart_storage import CartStorage
from restaurant.storages.restaurant_storage import RestaurantStorage


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
        except custom_exceptions.InvalidQuantityFound as e:
            return InvalidQuantity(quantity=e.quantity)
