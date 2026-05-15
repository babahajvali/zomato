import graphene

from accounts.graphql.types.error_types import (
    UserNotFound,
    InvalidCredentials,
    EmailNotFound,
    EmailAlreadyExists,
    EmptyUserNameFound,
    NothingToUpdateUserProperties,
)
from accounts.graphql.types.types import UserAddressesType, UserLoginType, UserType
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


class UpdateUserResponse(graphene.Union):
    class Meta:
        types = (
            UserType,
            UserNotFound,
            EmptyUserNameFound,
            NothingToUpdateUserProperties,
            UnauthorizedFound,
        )
