import graphene


class UserNotFound(graphene.ObjectType):
    user_id = graphene.String(required=True)


class InvalidCredentials(graphene.ObjectType):
    email = graphene.String(required=True)


class EmailNotFound(graphene.ObjectType):
    email = graphene.String(required=True)
