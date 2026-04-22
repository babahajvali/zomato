import graphene

from restaurant.graphql.schema import Mutation as RestaurantMutation
from restaurant.graphql.schema import Query as RestaurantQuery
from order.graphql.schema import Query as OrderQuery
from order.graphql.schema import Mutation as OrderMutation


class Query(RestaurantQuery, OrderQuery, graphene.ObjectType):
    pass


class Mutation(RestaurantMutation, OrderMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
