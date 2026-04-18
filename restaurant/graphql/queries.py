import graphene

from restaurant.graphql.resolvers import resolve_browse_restaurants
from restaurant.graphql.types.input_types import BrowseRestaurantsInputParams
from restaurant.graphql.types.response_types import BrowseRestaurantsResponse


class BrowseRestaurantsQuery(graphene.ObjectType):
    browse_restaurants = graphene.Field(
        BrowseRestaurantsResponse,
        params=BrowseRestaurantsInputParams(required=False),
        resolver=resolve_browse_restaurants,
    )

