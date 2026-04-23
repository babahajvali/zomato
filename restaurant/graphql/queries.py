import graphene

from restaurant.graphql.resolvers.browse_restaurants_resolver import (
    get_browse_restaurants_resolver,
)
from restaurant.graphql.resolvers.get_cart_items_resolver import get_cart_items_resolver
from restaurant.graphql.resolvers.get_restaurant_timings_resolver import (
    get_restaurant_timings_resolver,
)
from restaurant.graphql.resolvers.restaurant_menu_resolver import (
    get_restaurant_menu_resolver,
)
from restaurant.graphql.types.input_types import (
    BrowseRestaurantsInputParams,
    ViewRestaurantMenuInputParams,
    GetRestaurantTimingsInputParams,
    GetCartItemsInputParams,
)
from restaurant.graphql.types.response_types import (
    BrowseRestaurantsResponse,
    ViewRestaurantMenuResponse,
    GetRestaurantTimingsResponse,
    GetCartItemsResponse,
)


class RestaurantQueries(graphene.ObjectType):
    browse_restaurants = graphene.Field(
        BrowseRestaurantsResponse,
        params=BrowseRestaurantsInputParams(required=True),
        resolver=get_browse_restaurants_resolver,
    )
    view_restaurant_manu = graphene.Field(
        ViewRestaurantMenuResponse,
        params=ViewRestaurantMenuInputParams(required=True),
        resolver=get_restaurant_menu_resolver,
    )
    get_restaurant_timings = graphene.Field(
        GetRestaurantTimingsResponse,
        params=GetRestaurantTimingsInputParams(required=True),
        resolver=get_restaurant_timings_resolver,
    )
    get_cart_items = graphene.Field(
        GetCartItemsResponse,
        params=GetCartItemsInputParams(required=True),
        resolver=get_cart_items_resolver,
    )
