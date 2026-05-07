import graphene

from accounts.graphql.types.error_types import (
    UserNotFound,
    InvalidCredentials,
    EmailNotFound,
)
from accounts.graphql.types.types import UserAddressesType, UserLoginType


class GetUserAddressResponse(graphene.Union):
    class Meta:
        types = (
            UserAddressesType,
            UserNotFound,
        )


class UserLoginResponse(graphene.Union):
    class Meta:
        types = (UserLoginType, InvalidCredentials, EmailNotFound)
