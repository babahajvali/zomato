import graphene


class UpdateRestaurantTimingInputParams(graphene.InputObjectType):
    id = graphene.Int(required=True)
    open_time = graphene.Time()
    close_time = graphene.Time()

