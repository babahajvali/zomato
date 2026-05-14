import graphene


class UserNotRestaurantOwner(graphene.ObjectType):
    user_id = graphene.String(required=True)


class UnauthorizedFound(graphene.ObjectType):
    context_user_id = graphene.String()
