import graphene

from restaurant.graphql.mutations import (
    UpdateRestaurantTiming,
    CreateMenuItems,
    DeleteRestaurantTiming,
    UpdateCartItem,
    RemoveCartItem,
    ClearCartItems,
)
from restaurant.graphql.queries import (
    BrowseRestaurantsQuery,
    ViewRestaurantMenu,
    GetRestaurantTimingsQuery,
    GetCartItems,
)

QUERY_CLASSES = [
    BrowseRestaurantsQuery,
    ViewRestaurantMenu,
    GetRestaurantTimingsQuery,
    GetCartItems,
]

MUTATION_CLASSES = [
    UpdateRestaurantTiming,
    CreateMenuItems,
    DeleteRestaurantTiming,
    UpdateCartItem,
    RemoveCartItem,
    ClearCartItems,
]


class Query(*QUERY_CLASSES, graphene.ObjectType):
    pass


class Mutation(*MUTATION_CLASSES, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
