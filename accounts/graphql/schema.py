import graphene

from accounts.graphql.mutation import AccountMutations
from accounts.graphql.queries import AccountQueries

QUERY_CLASSES = [AccountQueries]

MUTATION_CLASSES = [AccountMutations]


class Query(*QUERY_CLASSES, graphene.ObjectType):
    pass


class Mutation(*MUTATION_CLASSES, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
