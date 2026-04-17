import graphene


class RestaurantTimingNoFoundTpe(graphene.ObjectType):
    id = graphene.Int(required=True)


class OpenTimeGreaterThanCloseTimeType(graphene.ObjectType):
    open_time = graphene.Time(required=True)
    close_time = graphene.Time(required=True)


class UserIsNotRestaurantOwnerType(graphene.ObjectType):
    user_id = graphene.String(required=True)
