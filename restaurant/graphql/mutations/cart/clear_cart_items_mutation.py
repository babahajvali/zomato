import graphene

from restaurant.exception import custom_exceptions
from restaurant.graphql.types.error_types import CartNotFound
from restaurant.graphql.types.input_types import ClearCartItemsInputParams
from restaurant.graphql.types.response_types import ClearCartItemsResponse
from restaurant.graphql.types.types import ClearCartItemsSuccessType
from restaurant.interactors.cart.cart_item_interactor import CartItemInteractor
from restaurant.storages.cart_storage import CartStorage
from restaurant.storages.restaurant_storage import RestaurantStorage


class ClearCartItemsMutation(graphene.Mutation):
    class Arguments:
        params = ClearCartItemsInputParams(required=True)

    Output = ClearCartItemsResponse

    @staticmethod
    def mutate(root, info, params):
        cart_storage = CartStorage()
        restaurant_storage = RestaurantStorage()

        interactor = CartItemInteractor(
            cart_storage=cart_storage,
            restaurant_storage=restaurant_storage,
        )

        try:
            interactor.clear_cart_items(cart_id=params.cart_id)

            return ClearCartItemsSuccessType(
                cart_id=params.cart_id,
                success=True
            )
        except custom_exceptions.CartNotFound as e:
            return CartNotFound(cart_id=e.cart_id)