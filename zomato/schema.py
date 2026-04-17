import graphene

from restaurant.graphql.schema import Mutation as RestaurantMutation
from restaurant.graphql.schema import Query as RestaurantQuery


class Query(RestaurantQuery, graphene.ObjectType):
    pass


class Mutation(RestaurantMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
