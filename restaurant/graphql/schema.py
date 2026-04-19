import graphene

from restaurant.graphql.mutations import UpdateRestaurantTiming, \
    CreateMenuItems
from restaurant.graphql.queries import BrowseRestaurantsQuery, \
    ViewRestaurantMenu

QUERY_CLASSES = [
    BrowseRestaurantsQuery, ViewRestaurantMenu
]

MUTATION_CLASSES = [
    UpdateRestaurantTiming, CreateMenuItems
]


class Query(*QUERY_CLASSES, graphene.ObjectType):
    pass


class Mutation(*MUTATION_CLASSES, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
