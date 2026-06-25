import graphene

from accounts.graphql.types.error_types import (
    AddressAlreadyExists,
    UserNotFound,
    InvalidCredentials,
    EmailNotFound,
    EmailAlreadyExists,
    EmptyUserNameFound,
    NothingToUpdateUserProperties,
)
from accounts.graphql.types.types import (
    AddressType,
    UserAddressesType,
    UserLoginType,
    UserType,
)
from utils.graphql_types import UnauthorizedFound


class GetUserAddressResponse(graphene.Union):
    class Meta:
        types = (UserAddressesType, UserNotFound, UnauthorizedFound)


class UserLoginResponse(graphene.Union):
    class Meta:
        types = (UserLoginType, InvalidCredentials, EmailNotFound)


class CreateUserResponse(graphene.Union):
    class Meta:
        types = (UserType, EmailAlreadyExists, EmptyUserNameFound)


class CreateAddressResponse(graphene.Union):
    class Meta:
        types = (AddressType, UserNotFound, AddressAlreadyExists, UnauthorizedFound)


class UpdateUserResponse(graphene.Union):
    class Meta:
        types = (
            UserType,
            UserNotFound,
            EmptyUserNameFound,
            NothingToUpdateUserProperties,
            UnauthorizedFound,
        )
