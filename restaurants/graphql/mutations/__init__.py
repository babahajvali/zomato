import graphene

from restaurants.graphql.mutations.cart.clear_cart_items_mutation import (
    ClearCartItemsMutation,
)
from restaurants.graphql.mutations.cart.remove_cart_item_mutation import (
    RemoveCartItemMutation,
)
from restaurants.graphql.mutations.cart.update_cart_item_mutation import (
    UpdateCartItemMutation,
)
from restaurants.graphql.mutations.restaurant.create_menu_items_mutation import (
    CreateMenuItemsMutation,
)
from restaurants.graphql.mutations.restaurant_timing.update_restaurant_timing_mutation import (
    UpdateRestaurantTimingMutation,
)
from restaurants.graphql.mutations.restaurant_timing.delete_restaurant_timing_mutation import (
    DeleteRestaurantTimingMutation,
)
from restaurants.graphql.mutations.review.create_review_mutation import (
    CreateReviewMutation,
)


class RestaurantMutations(graphene.ObjectType):
    update_restaurant_timing = UpdateRestaurantTimingMutation.Field(required=True)
    delete_restaurant_timing = DeleteRestaurantTimingMutation.Field(required=True)
    create_menu_items = CreateMenuItemsMutation.Field(required=True)
    clear_cart_items = ClearCartItemsMutation.Field(required=True)
    remove_cart_item = RemoveCartItemMutation.Field(required=True)
    update_cart_item = UpdateCartItemMutation.Field(required=True)
    create_review = CreateReviewMutation.Field(required=True)
