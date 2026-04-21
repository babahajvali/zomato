import graphene

from restaurant.graphql.resolvers import resolve_browse_restaurants
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
)
from restaurant.graphql.types.response_types import (
    BrowseRestaurantsResponse,
    ViewRestaurantMenuResponse,
    GetRestaurantTimingsResponse,
)


class RestaurantQueries(graphene.ObjectType):
    browse_restaurants = graphene.Field(
        BrowseRestaurantsResponse,
        params=BrowseRestaurantsInputParams(required=True),
        resolver=resolve_browse_restaurants,
    )
    view_restaurant_manu = graphene.Field(
        ViewRestaurantMenuResponse,
        params=ViewRestaurantMenuInputParams(required=True),
        resolver=resolve_view_restaurant_menu,
    )
    get_restaurant_timings = graphene.Field(
        GetRestaurantTimingsResponse,
        params=GetRestaurantTimingsInputParams(required=True),
        resolver=resolve_get_restaurant_timings,
    )
