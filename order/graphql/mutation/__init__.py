import graphene

from order.graphql.mutation.place_order_mutation import PlaceOrderMutation


class OrderMutation(graphene.ObjectType):
    place_order = PlaceOrderMutation.Field(required=True)


