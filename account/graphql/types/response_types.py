import graphene

from account.graphql.types.error_types import UserNotFound
from account.graphql.types.types import UserAddressesType


class GetUserAddressResponse(graphene.Union):
    class Meta:
        types = (
            UserAddressesType,
            UserNotFound,
        )
