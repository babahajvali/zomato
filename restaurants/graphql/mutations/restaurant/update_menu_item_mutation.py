from decimal import Decimal

import graphene

from restaurants.exception import custom_exceptions
from restaurants.graphql.types.error_types import MenuItemNotFound
from restaurants.graphql.types.input_types import UpdateMenuItemInputParams
from restaurants.graphql.types.response_types import UpdateMenuItemResponse
from restaurants.graphql.types.types import MenuItemType
from restaurants.interactors.dtos import UpdateMenuItemDTO
from restaurants.interactors.restaurant.menu_item_interactor import MenuItemInteractor
from restaurants.storages.restaurant_storage import RestaurantStorage
from utils.graphql_types import UserNotRestaurantOwner


class UpdateMenuItemMutation(graphene.Mutation):
    class Arguments:
        params = UpdateMenuItemInputParams(required=True)

    Output = UpdateMenuItemResponse

    @staticmethod
    def mutate(root, info, params):

        restaurant_storage = RestaurantStorage()
        interactor = MenuItemInteractor(restaurant_storage=restaurant_storage)

        update_item_dto = UpdateMenuItemDTO(
            menu_item_id=params.menu_item_id,
            name=params.name,
            price=params.price,
            preparation_time_in_minutes=params.preparation_time_in_minutes,
            is_available=params.is_available,
            tags=params.tags,
        )

        try:
            result = interactor.update_menu_item(
                update_menu_item_dto=update_item_dto, user_id=info.context.user_id
            )

            return MenuItemType(
                item_id=result.id,
                restaurant_id=result.restaurant_id,
                name=result.name,
                description=result.description,
                price=Decimal(result.price),
                category=result.category,
                is_veg=result.is_veg,
                is_available=result.is_available,
                preparation_time_in_minutes=result.preparation_time_in_minutes,
                tags=result.tags,
            )
        except custom_exceptions.UserNotRestaurantOwner as e:
            return UserNotRestaurantOwner(user_id=e.user_id)
        except custom_exceptions.MenuItemNotFound as e:
            return MenuItemNotFound(menu_item_id=e.menu_item_id)
