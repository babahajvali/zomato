import graphene

from orders.graphql.resolvers.get_available_promo_code_resolver import (
    get_available_promo_code_resolver,
)
from orders.graphql.resolvers.order_resolvers import (
    get_order_resolver,
    get_restaurant_order_resolver,
    get_user_order_resolver,
)
from orders.graphql.resolvers.today_restaurant_orders_resolver import (
    get_today_restaurant_orders_resolver,
)
from orders.graphql.types.input_types import (
    GetOrderInputParams,
    GetRestaurantOrdersInputParams,
    GetTodayRestaurantOrdersInputParams,
    GetUserOrdersInputParams,
)
from orders.graphql.types.response_types import (
    GetOrderResponse,
    RestaurantOrdersResponse,
    TodayRestaurantOrdersResponse,
    UserOrdersResponse,
    GetAvailablePromoCodesResponse,
)


class OrderQueries(graphene.ObjectType):
    get_order = graphene.Field(
        GetOrderResponse,
        params=GetOrderInputParams(required=True),
        resolver=get_order_resolver,
    )
    user_orders = graphene.Field(
        UserOrdersResponse,
        params=GetUserOrdersInputParams(required=True),
        resolver=get_user_order_resolver,
    )
    restaurant_orders = graphene.Field(
        RestaurantOrdersResponse,
        params=GetRestaurantOrdersInputParams(required=True),
        resolver=get_restaurant_order_resolver,
    )
    today_restaurant_orders = graphene.Field(
        TodayRestaurantOrdersResponse,
        params=GetTodayRestaurantOrdersInputParams(required=True),
        resolver=get_today_restaurant_orders_resolver,
    )
    get_available_promo_codes = graphene.Field(
        GetAvailablePromoCodesResponse, resolver=get_available_promo_code_resolver
    )
