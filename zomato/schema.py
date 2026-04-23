import graphene

from restaurants.graphql.schema import Mutation as RestaurantMutation
from restaurants.graphql.schema import Query as RestaurantQuery
from orders.graphql.schema import Query as OrderQuery
from orders.graphql.schema import Mutation as OrderMutation
from accounts.graphql.schema import Query as AccountQuery
from accounts.graphql.schema import Mutation as AccountMutation


class Query(RestaurantQuery, OrderQuery, AccountQuery, graphene.ObjectType):
    pass


class Mutation(RestaurantMutation, OrderMutation, AccountMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
