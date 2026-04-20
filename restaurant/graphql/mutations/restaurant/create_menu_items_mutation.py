import graphene

from restaurant.enums import Category
from restaurant.exception.custom_exceptions import (
    InvalidCategoriesFound,
    RestaurantNotFound,
    UserIsNotRestaurantOwner,
)
from restaurant.graphql.types.input_types import CreateMenuItemsInputParams
from restaurant.graphql.types.response_types import CreateMenuItemsResponse
from restaurant.graphql.types.error_types import (
    InvalidCategoriesFoundType,
    RestaurantNotFoundType,
    UserIsNotRestaurantOwnerType,
)
from restaurant.graphql.types.types import MenuItemsType, MenuItemType
from restaurant.interactors.dtos import CreateMenuItemDTO
from restaurant.interactors.restaurant.create_menu_item_interactor import (
    CreateMenuItemInteractor,
)
from restaurant.storages.restaurant_storage import RestaurantStorage


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
                restaurant_id=item.restaurant_id,
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

        except RestaurantNotFound as exc:
            return RestaurantNotFoundType(restaurant_id=exc.restaurant_id)
        except InvalidCategoriesFound as exc:
            return InvalidCategoriesFoundType(categories=exc.categories)
        except UserIsNotRestaurantOwner as exc:
            return UserIsNotRestaurantOwnerType(user_id=exc.user_id)

