import graphene

from restaurant.graphql.mutations.restaurant.create_menu_items_mutation import (
    CreateMenuItemsMutation,
)
from restaurant.graphql.mutations.restaurant_timing.update_restaurant_timing_mutation import (
    UpdateRestaurantTimingMutation,
)
from restaurant.graphql.mutations.restaurant_timing.delete_restaurant_timing_mutation import (
    DeleteRestaurantTimingMutation,
)


class RestaurantMutations(graphene.ObjectType):
    update_restaurant_timing = UpdateRestaurantTimingMutation.Field(required=True)
    delete_restaurant_timing = DeleteRestaurantTimingMutation.Field(required=True)
    create_menu_items = CreateMenuItemsMutation.Field(required=True)
