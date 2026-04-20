import graphene

from restaurant.graphql.mutations import UpdateRestaurantTiming, \
    CreateMenuItems, DeleteRestaurantTiming
from restaurant.graphql.queries import BrowseRestaurantsQuery, \
    ViewRestaurantMenu, GetRestaurantTimingsQuery

QUERY_CLASSES = [
    BrowseRestaurantsQuery, ViewRestaurantMenu, GetRestaurantTimingsQuery
]

MUTATION_CLASSES = [
    UpdateRestaurantTiming, CreateMenuItems, DeleteRestaurantTiming
]


class Query(*QUERY_CLASSES, graphene.ObjectType):
    pass


class Mutation(*MUTATION_CLASSES, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
