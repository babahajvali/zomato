import graphene

from restaurants.exception import custom_exceptions
from restaurants.graphql.types.error_types import CartItemNotFound
from restaurants.graphql.types.input_types import RemoveCartItemInputParams
from restaurants.graphql.types.response_types import RemoveCartItemResponse
from restaurants.graphql.types.types import RemoveCartItemSuccessType
from restaurants.interactors.cart.cart_item_interactor import CartItemInteractor
from restaurants.storages.cart_storage import CartStorage
from restaurants.storages.restaurant_storage import RestaurantStorage


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
