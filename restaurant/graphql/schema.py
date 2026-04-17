import graphene

from restaurant.graphql.mutations import UpdateRestaurantTiming
from restaurant.graphql.queries import Query as BaseQuery

QUERY_CLASSES = [
    BaseQuery,
]

MUTATION_CLASSES = [
    UpdateRestaurantTiming,
]


class Query(*QUERY_CLASSES, graphene.ObjectType):
    pass


class Mutation(*MUTATION_CLASSES, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
