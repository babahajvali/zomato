import graphene

from accounts.graphql.resolver.get_user_addresses_resolver import (
    get_user_addresses_resolver,
)
from accounts.graphql.types.response_types import GetUserAddressResponse


class AccountQueries(graphene.ObjectType):
    # TODO: field name is singular but returns a list — rename to user_addresses (and drop the get_ prefix, GraphQL convention is noun-based).
    get_user_address = graphene.Field(
        GetUserAddressResponse, resolver=get_user_addresses_resolver
    )
