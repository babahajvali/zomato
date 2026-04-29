import graphene


class UserNotRestaurantOwner(graphene.ObjectType):
    user_id = graphene.String(required=True)
