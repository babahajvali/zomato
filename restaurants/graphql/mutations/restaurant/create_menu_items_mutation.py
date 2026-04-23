import graphene

from restaurants.constants.enums import Category
from restaurants.exception import custom_exceptions

from restaurants.graphql.types.input_types import CreateMenuItemsInputParams
from restaurants.graphql.types.response_types import CreateMenuItemsResponse
from restaurants.graphql.types.error_types import (
    InvalidCategoriesFound,
    RestaurantNotFound,
)
from restaurants.graphql.types.types import MenuItemsType, MenuItemType
from restaurants.interactors.dtos import CreateMenuItemDTO
from restaurants.interactors.restaurant.create_menu_item_interactor import (
    CreateMenuItemInteractor,
)
from restaurants.storages.restaurant_storage import RestaurantStorage
from utils.graphql_types import UserIsNotRestaurantOwner


class CreateMenuItemsMutation(graphene.Mutation):
    class Arguments:
        params = CreateMenuItemsInputParams(required=True)

    Output = CreateMenuItemsResponse

    @staticmethod
    def mutate(root, info, params):
        restaurant_storage = RestaurantStorage()
        interactor = CreateMenuItemInteractor(
            restaurant_storage=restaurant_storage,
        )

        create_items_dto = [
            CreateMenuItemDTO(
                name=item.name,
                description=item.description,
                price=item.price,
                category=Category(item.category),
                is_veg=item.is_veg,
                is_available=item.is_available,
                preparation_time_in_minutes=item.preparation_time_in_minutes,
                tags=item.tags or [],
            )
            for item in params.menu_items
        ]

        try:
            created_items = interactor.create_menu_item(
                create_items_dto=create_items_dto,
                user_id=info.context.user_id,
                restaurant_id=params.restaurant_id,
            )

            menu_items = [
                MenuItemType(
                    item_id=item.id,
                    restaurant_id=item.restaurant_id,
                    name=item.name,
                    description=item.description,
                    price=float(item.price),
                    category=item.category,
                    is_veg=item.is_veg,
                    is_available=item.is_available,
                    preparation_time_in_minutes=item.preparation_time_in_minutes,
                    tags=item.tags,
                )
                for item in created_items
            ]
            return MenuItemsType(menu_items=menu_items)

        except custom_exceptions.RestaurantNotFound as exc:
            return RestaurantNotFound(restaurant_id=exc.restaurant_id)
        except custom_exceptions.InvalidCategoriesFound as exc:
            return InvalidCategoriesFound(categories=exc.categories)
        except custom_exceptions.UserIsNotRestaurantOwner as exc:
            return UserIsNotRestaurantOwner(user_id=exc.user_id)
