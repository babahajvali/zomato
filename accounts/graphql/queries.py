import graphene

from accounts.graphql.resolver.get_user_addresses_resolver import (
    get_user_addresses_resolver,
)
from accounts.graphql.types.response_types import GetUserAddressResponse


class AccountQueries(graphene.ObjectType):
    get_user_address = graphene.Field(
        GetUserAddressResponse, resolver=get_user_addresses_resolver
    )
