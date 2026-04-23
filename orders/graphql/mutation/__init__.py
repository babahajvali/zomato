import graphene

from orders.graphql.mutation.place_order_mutation import PlaceOrderMutation
from orders.graphql.mutation.update_order_status_mutation import (
    UpdateOrderStatusMutation,
)
from orders.graphql.mutation.cancel_order_mutation import CancelOrderMutation
from orders.graphql.mutation.auto_cancel_order_mutation import AutoCancelOrderMutation


class OrderMutation(graphene.ObjectType):
    place_order = PlaceOrderMutation.Field(required=True)
    update_order_status = UpdateOrderStatusMutation.Field(required=True)
    cancel_order = CancelOrderMutation.Field(required=True)
    auto_cancel_order = AutoCancelOrderMutation.Field(required=True)
