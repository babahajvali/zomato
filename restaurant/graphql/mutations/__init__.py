import graphene

from restaurant.graphql.mutations.cart.clear_cart_items_mutation import \
    ClearCartItemsMutation
from restaurant.graphql.mutations.cart.remove_cart_item_mutation import (
    RemoveCartItemMutation,
)
from restaurant.graphql.mutations.cart.update_cart_item_mutation import (
    UpdateCartItemMutation,
)
from restaurant.graphql.mutations.restaurant.create_menu_items_mutation import (
    CreateMenuItemsMutation,
)
from restaurant.graphql.mutations.restaurant_timing.update_restaurant_timing_mutation import (
    UpdateRestaurantTimingMutation,
)
from restaurant.graphql.mutations.restaurant_timing.delete_restaurant_timing_mutation import (
    DeleteRestaurantTimingMutation,
)


class UpdateRestaurantTiming(graphene.ObjectType):
    update_restaurant_timing = UpdateRestaurantTimingMutation.Field(required=True)


class DeleteRestaurantTiming(graphene.ObjectType):
    delete_restaurant_timing = DeleteRestaurantTimingMutation.Field(required=True)


class CreateMenuItems(graphene.ObjectType):
    create_menu_items = CreateMenuItemsMutation.Field(required=True)


class UpdateCartItem(graphene.ObjectType):
    update_cart_item = UpdateCartItemMutation.Field(required=True)


class RemoveCartItem(graphene.ObjectType):
    remove_cart_item = RemoveCartItemMutation.Field(required=True)


class ClearCartItems(graphene.ObjectType):
    clear_cart_items = ClearCartItemsMutation.Field(required=True)

