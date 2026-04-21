import graphene


class RestaurantTimingNotFound(graphene.ObjectType):
    id = graphene.Int(required=True)


class OpenTimeGreaterThanCloseTime(graphene.ObjectType):
    open_time = graphene.Time(required=True)
    close_time = graphene.Time(required=True)


class UserIsNotRestaurantOwner(graphene.ObjectType):
    user_id = graphene.String(required=True)


class RestaurantNotFound(graphene.ObjectType):
    restaurant_id = graphene.String(required=True)


class InvalidCategoriesFound(graphene.ObjectType):
    categories = graphene.List(graphene.String, required=True)


class InvalidCuisineTypeExceptionType(graphene.ObjectType):
    cuisine_type = graphene.String(required=True)


class InvalidMinRatingExceptionType(graphene.ObjectType):
    min_rating = graphene.Float(required=True)
