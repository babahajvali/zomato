import graphene

from restaurant.graphql.mutations.restaurant_timing.update_restaurant_timing_mutation import \
    UpdateRestaurantTimingMutation


class UpdateRestaurantTiming(graphene.ObjectType):
    update_restaurant_timing = UpdateRestaurantTimingMutation.Field(
        required=True
    )
