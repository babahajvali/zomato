import graphene

from accounts.graphql.mutation.sample_mutation import CreateAccount


class AccountMutations(graphene.ObjectType):
    create_account = CreateAccount.Field(required=True)
