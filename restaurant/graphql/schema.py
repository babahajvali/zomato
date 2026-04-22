import graphene

from restaurant.graphql.mutations import RestaurantMutations
from restaurant.graphql.queries import RestaurantQueries

QUERY_CLASSES = [RestaurantQueries]

MUTATION_CLASSES = [RestaurantMutations]


class Query(*QUERY_CLASSES, graphene.ObjectType):
    pass


class Mutation(*MUTATION_CLASSES, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
