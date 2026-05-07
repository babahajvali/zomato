import graphene

from accounts.graphql.mutation.user_login_mutation import UserLoginMutation


class AccountMutations(graphene.ObjectType):
    user_login = UserLoginMutation.Field(required=True)
