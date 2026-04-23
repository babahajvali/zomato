import graphene

from restaurant.graphql.schema import Mutation as RestaurantMutation
from restaurant.graphql.schema import Query as RestaurantQuery
from order.graphql.schema import Query as OrderQuery
from order.graphql.schema import Mutation as OrderMutation
from account.graphql.schema import Query as AccountQuery
from account.graphql.schema import Mutation as AccountMutation


class Query(RestaurantQuery, OrderQuery, AccountQuery, graphene.ObjectType):
    pass


class Mutation(RestaurantMutation, OrderMutation, AccountMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
