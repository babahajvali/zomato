import graphene

from restaurant.graphql.mutations.restaurant.create_menu_items_mutation import \
    CreateMenuItemsMutation
from restaurant.graphql.mutations.restaurant_timing.update_restaurant_timing_mutation import \
    UpdateRestaurantTimingMutation


class UpdateRestaurantTiming(graphene.ObjectType):
    update_restaurant_timing = UpdateRestaurantTimingMutation.Field(
        required=True
    )


class CreateMenuItems(graphene.ObjectType):
    create_menu_items = CreateMenuItemsMutation.Field(required=True)