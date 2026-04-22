import graphene


class UserIsNotRestaurantOwner(graphene.ObjectType):
    user_id = graphene.String(required=True)
