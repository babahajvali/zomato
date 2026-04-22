import graphene

from order.graphql.resolvers.order_resolvers import (
    resolve_get_order,
    resolve_restaurant_orders,
    resolve_user_orders,
)
from order.graphql.resolvers.today_restaurant_orders_resolver import \
    resolve_today_restaurant_orders
from order.graphql.types.input_types import (
    GetOrderInputParams,
    GetRestaurantOrdersInputParams,
    GetTodayRestaurantOrdersInputParams,
)
from order.graphql.types.response_types import (
    GetOrderResponse,
    RestaurantOrdersResponse,
    TodayRestaurantOrdersResponse,
    UserOrdersResponse,
)


class OrderQueries(graphene.ObjectType):
    get_order = graphene.Field(
        GetOrderResponse,
        params=GetOrderInputParams(required=True),
        resolver=resolve_get_order,
    )
    user_orders = graphene.Field(
        UserOrdersResponse,
        params=GetRestaurantOrdersInputParams(required=True),
        resolver=resolve_user_orders,
    )
    restaurant_orders = graphene.Field(
        RestaurantOrdersResponse,
        params=GetRestaurantOrdersInputParams(required=True),
        resolver=resolve_restaurant_orders,
    )
    today_restaurant_orders = graphene.Field(
        TodayRestaurantOrdersResponse,
        params=GetTodayRestaurantOrdersInputParams(required=True),
        resolver=resolve_today_restaurant_orders,
    )

    
