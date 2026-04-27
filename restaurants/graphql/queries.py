import graphene

from restaurants.graphql.resolvers.browse_restaurants_resolver import (
    get_browse_restaurants_resolver,
)
from restaurants.graphql.resolvers.get_cart_items_resolver import (
    get_cart_items_resolver,
)
from restaurants.graphql.resolvers.get_restaurant_dashboard_resolver import (
    get_restaurant_dashboard_resolver,
)
from restaurants.graphql.resolvers.get_restaurant_timings_resolver import (
    get_restaurant_timings_resolver,
)
from restaurants.graphql.resolvers.restaurant_menu_resolver import (
    get_restaurant_menu_resolver,
)
from restaurants.graphql.types.input_types import (
    BrowseRestaurantsInputParams,
    ViewRestaurantMenuInputParams,
    GetRestaurantTimingsInputParams,
    GetCartItemsInputParams,
    GetRestaurantDashboardInputParams,
)
from restaurants.graphql.types.response_types import (
    BrowseRestaurantsResponse,
    ViewRestaurantMenuResponse,
    GetRestaurantTimingsResponse,
    GetCartItemsResponse,
    GetRestaurantDashboardResponse,
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

    get_restaurant_dashboard = graphene.Field(
        GetRestaurantDashboardResponse,
        params=GetRestaurantDashboardInputParams(required=True),
        resolver=get_restaurant_dashboard_resolver,
    )
