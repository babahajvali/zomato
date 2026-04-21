import graphene

from restaurant.graphql.resolvers.browse_restaurants_resolver import (
    resolve_browse_restaurants,
)
from restaurant.graphql.resolvers.get_cart_items_resolver import get_cart_items_resolver
from restaurant.graphql.resolvers.get_restaurant_timings_resolver import (
    resolve_get_restaurant_timings,
)
from restaurant.graphql.resolvers.restaurant_menu_resolver import (
    resolve_view_restaurant_menu,
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


class BrowseRestaurantsQuery(graphene.ObjectType):
    browse_restaurants = graphene.Field(
        BrowseRestaurantsResponse,
        params=BrowseRestaurantsInputParams(required=True),
        resolver=resolve_browse_restaurants,
    )


class ViewRestaurantMenu(graphene.ObjectType):
    view_restaurant_manu = graphene.Field(
        ViewRestaurantMenuResponse,
        params=ViewRestaurantMenuInputParams(required=True),
        resolver=resolve_view_restaurant_menu,
    )


class GetRestaurantTimingsQuery(graphene.ObjectType):
    get_restaurant_timings = graphene.Field(
        GetRestaurantTimingsResponse,
        params=GetRestaurantTimingsInputParams(required=True),
        resolver=resolve_get_restaurant_timings,
    )


class GetCartItems(graphene.ObjectType):
    get_cart_items = graphene.Field(
        GetCartItemsResponse,
        params=GetCartItemsInputParams(required=True),
        resolver=get_cart_items_resolver,
    )
