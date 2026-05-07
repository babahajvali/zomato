import graphene

from restaurants.graphql.resolvers.browse_restaurants_resolver import (
    get_browse_restaurants_resolver,
)
from restaurants.graphql.resolvers.get_cart_items_resolver import (
    get_cart_items_resolver,
)
from restaurants.graphql.resolvers.get_customer_cart_id_resolver import (
    get_customer_cart_id_resolver,
)
from restaurants.graphql.resolvers.get_restaurant_dashboard_resolver import (
    get_restaurant_dashboard_resolver,
)
from restaurants.graphql.resolvers.get_restaurant_timings_resolver import (
    get_restaurant_timings_resolver,
)
from restaurants.graphql.resolvers.get_user_restaurant_review_resolver import (
    get_user_restaurant_review_resolver,
)
from restaurants.graphql.resolvers.get_owner_restaurants_resolver import (
    get_owner_restaurants_resolver,
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
    GetUserRestaurantReviewInputParams,
)
from restaurants.graphql.types.response_types import (
    BrowseRestaurantsResponse,
    ViewRestaurantMenuResponse,
    GetRestaurantTimingsResponse,
    GetCartItemsResponse,
    GetRestaurantDashboardResponse,
    GetUserRestaurantReviewResponse,
    GetOwnerRestaurantsResponse,
    GetCustomerCartIdResponse,
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

    get_user_restaurant_review = graphene.Field(
        GetUserRestaurantReviewResponse,
        params=GetUserRestaurantReviewInputParams(required=True),
        resolver=get_user_restaurant_review_resolver,
    )

    get_owner_restaurants = graphene.Field(
        GetOwnerRestaurantsResponse,
        resolver=get_owner_restaurants_resolver,
    )

    get_customer_cart_id = graphene.Field(
        GetCustomerCartIdResponse, resolver=get_customer_cart_id_resolver
    )
