import graphene


class CreateAccount(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, username):
        return CreateAccount(success=True, message=f"Account '{username}' created")
