import graphene

from order.graphql.mutation import OrderMutation
from order.graphql.queries import OrderQueries

QUERY_CLASSES = [OrderQueries]

MUTATION_CLASSES = [OrderMutation]


class Query(*QUERY_CLASSES, graphene.ObjectType):
    pass


class Mutation(*MUTATION_CLASSES, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
