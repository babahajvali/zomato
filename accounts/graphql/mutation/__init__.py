import graphene

from accounts.graphql.mutation.create_address_mutation import CreateAddressMutation
from accounts.graphql.mutation.create_user_mutation import CreateUserMutation
from accounts.graphql.mutation.update_user_mutation import UpdateUserMutation
from accounts.graphql.mutation.user_login_mutation import UserLoginMutation


class AccountMutations(graphene.ObjectType):
    create_user = CreateUserMutation.Field(required=True)
    update_user = UpdateUserMutation.Field(required=True)
    user_login = UserLoginMutation.Field(required=True)
    create_address = CreateAddressMutation.Field(required=True)
