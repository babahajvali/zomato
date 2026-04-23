from restaurant.exception import custom_exceptions
from restaurant.graphql.types.error_types import RestaurantNotFound
from restaurant.graphql.types.types import (
    CategoryMenuType,
    MenuItemType,
    RestaurantMenuType,
)
from restaurant.interactors.restaurant.view_restaurant_menu import (
    ViewRestaurantMenuInteractor,
)
from restaurant.storages.restaurant_storage import RestaurantStorage


def _map_menu_response(menu_dto) -> RestaurantMenuType:
    return RestaurantMenuType(
        restaurant_id=menu_dto.restaurant_id,
        categories=[
            CategoryMenuType(
                category=each_category.category.value,
                items=[
                    MenuItemType(
                        item_id=each_item.item_id,
                        name=each_item.name,
                        description=each_item.description,
                        price=each_item.price,
                        category=each_item.category.value,
                        is_veg=each_item.is_veg,
                        is_available=each_item.is_available,
                        preparation_time_in_minutes=each_item.preparation_time_in_minutes,
                        tags=each_item.tags,
                    )
                    for each_item in each_category.items
                ],
            )
            for each_category in menu_dto.categories
        ],
    )


def get_restaurant_menu_resolver(root, info, params):
    interactor = ViewRestaurantMenuInteractor(
        restaurant_storage=RestaurantStorage(),
    )

    try:
        menu = interactor.view_restaurant_menu(
            restaurant_id=params.restaurant_id,
        )
        return _map_menu_response(menu_dto=menu)
    except custom_exceptions.RestaurantNotFound as exc:
        return RestaurantNotFound(restaurant_id=str(exc.restaurant_id))
