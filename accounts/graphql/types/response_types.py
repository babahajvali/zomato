import graphene

from accounts.graphql.types.error_types import UserNotFound
from accounts.graphql.types.types import UserAddressesType


class GetUserAddressResponse(graphene.Union):
    class Meta:
        types = (
            UserAddressesType,
            UserNotFound,
        )
