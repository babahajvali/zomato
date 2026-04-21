import graphene

from restaurant.exception import custom_exceptions
from restaurant.graphql.types.error_types import CartItemNotFound
from restaurant.graphql.types.input_types import RemoveCartItemInputParams
from restaurant.graphql.types.response_types import RemoveCartItemResponse
from restaurant.graphql.types.types import RemoveCartItemSuccessType
from restaurant.interactors.cart.cart_item_interactor import CartItemInteractor
from restaurant.storages.cart_storage import CartStorage
from restaurant.storages.restaurant_storage import RestaurantStorage


class RemoveCartItemMutation(graphene.Mutation):
    class Arguments:
        params = RemoveCartItemInputParams(required=True)

    Output = RemoveCartItemResponse

    @staticmethod
    def mutate(root, info, params):
        cart_storage = CartStorage()
        restaurant_storage = RestaurantStorage()

        interactor = CartItemInteractor(
            cart_storage=cart_storage,
            restaurant_storage=restaurant_storage,
        )

        try:
            interactor.remove_cart_item(cart_item_id=params.cart_item_id)

            return RemoveCartItemSuccessType(
                success=True, cart_item_id=params.cart_item_id
            )
        except custom_exceptions.CartItemNotFound as e:
            return CartItemNotFound(cart_item_id=e.cart_item_id)
