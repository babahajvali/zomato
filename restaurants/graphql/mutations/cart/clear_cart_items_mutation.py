import graphene

from restaurants.exception import custom_exceptions
from restaurants.graphql.types.error_types import CartNotFound
from restaurants.graphql.types.input_types import ClearCartItemsInputParams
from restaurants.graphql.types.response_types import ClearCartItemsResponse
from restaurants.graphql.types.types import ClearCartItemsSuccessType
from restaurants.interactors.cart.cart_item_interactor import CartItemInteractor
from restaurants.storages.cart_storage import CartStorage
from restaurants.storages.restaurant_storage import RestaurantStorage


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
            # TODO: cart_id is client-supplied with no ownership check — any user can clear any cart.
            interactor.clear_cart_items(cart_id=params.cart_id)

            return ClearCartItemsSuccessType(cart_id=params.cart_id, success=True)
        except custom_exceptions.CartNotFound as e:
            return CartNotFound(cart_id=e.cart_id)
