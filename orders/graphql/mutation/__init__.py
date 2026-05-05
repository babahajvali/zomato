import graphene

from orders.graphql.mutation.place_order_mutation import PlaceOrderMutation
from orders.graphql.mutation.place_scheduled_order_mutation import (
    PlaceScheduledOrderMutation,
)
from orders.graphql.mutation.cancel_scheduled_order_mutation import (
    CancelScheduledOrderMutation,
)
from orders.graphql.mutation.update_order_status_mutation import (
    UpdateOrderStatusMutation,
)
from orders.graphql.mutation.cancel_order_mutation import CancelOrderMutation


class OrderMutation(graphene.ObjectType):
    place_order = PlaceOrderMutation.Field(required=True)
    place_scheduled_order = PlaceScheduledOrderMutation.Field(required=True)
    cancel_scheduled_order = CancelScheduledOrderMutation.Field(required=True)
    update_order_status = UpdateOrderStatusMutation.Field(required=True)
    cancel_order = CancelOrderMutation.Field(required=True)
