import graphene


class UserNotFound(graphene.ObjectType):
    user_id = graphene.String(required=True)
