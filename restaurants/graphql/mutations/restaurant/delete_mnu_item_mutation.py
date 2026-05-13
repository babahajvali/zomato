# TODO: filename typo "delete_mnu_item_mutation.py" — should be "delete_menu_item_mutation.py".
import graphene

from restaurants.exception import custom_exceptions
from restaurants.graphql.types.error_types import MenuItemNotFound
from restaurants.graphql.types.input_types import DeleteMenuItemInputParams
from restaurants.graphql.types.response_types import DeleteMenuItemResponse
from restaurants.graphql.types.types import DeleteMenuItemSuccessType
from restaurants.interactors.restaurant.menu_item_interactor import MenuItemInteractor
from restaurants.storages.restaurant_storage import RestaurantStorage
from utils.graphql_types import UserNotRestaurantOwner


class DeleteMenuItemMutation(graphene.Mutation):
    class Arguments:
        params = DeleteMenuItemInputParams(required=True)

    Output = DeleteMenuItemResponse

    @staticmethod
    def mutate(root, info, params):

        restaurant_storage = RestaurantStorage()
        interactor = MenuItemInteractor(restaurant_storage=restaurant_storage)

        try:
            interactor.delete_menu_item(
                menu_item_id=params.menu_item_id, user_id=info.context.user_id
            )

            return DeleteMenuItemSuccessType(
                success=True, menu_item_id=params.menu_item_id
            )
        except custom_exceptions.MenuItemNotFound as e:
            return MenuItemNotFound(menu_item_id=e.menu_item_id)
        except custom_exceptions.UserNotRestaurantOwner as e:
            return UserNotRestaurantOwner(user_id=e.user_id)
