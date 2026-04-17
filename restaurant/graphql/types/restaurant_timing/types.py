import graphene


class RestaurantTimingType(graphene.ObjectType):
    id = graphene.Int(required=True)
    restaurant_id = graphene.String(required=True)
    day_of_week = graphene.Int(required=True)
    open_time = graphene.Time(required=True)
    close_time = graphene.Time(required=True)

