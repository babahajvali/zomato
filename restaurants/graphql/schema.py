import graphene

from restaurants.graphql.mutations import RestaurantMutations
from restaurants.graphql.queries import RestaurantQueries

QUERY_CLASSES = [RestaurantQueries]

MUTATION_CLASSES = [RestaurantMutations]


class Query(*QUERY_CLASSES, graphene.ObjectType):
    pass


class Mutation(*MUTATION_CLASSES, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
