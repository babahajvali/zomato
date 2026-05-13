import graphene


class RestaurantTimingNotFound(graphene.ObjectType):
    id = graphene.Int(required=True)


class InvalidTimingRange(graphene.ObjectType):
    open_time = graphene.Time(required=True)
    close_time = graphene.Time(required=True)


class RestaurantNotFound(graphene.ObjectType):
    restaurant_id = graphene.String(required=True)


class InvalidCategories(graphene.ObjectType):
    categories = graphene.List(graphene.String, required=True)


class InvalidCuisineTypeException(graphene.ObjectType):
    cuisine_type = graphene.String(required=True)


class InvalidMinRating(graphene.ObjectType):
    min_rating = graphene.Float(required=True)


class CartNotFound(graphene.ObjectType):
    cart_id = graphene.String(required=True)


class CartNotBelongsToUser(graphene.ObjectType):
    user_id = graphene.String(required=True)
    cart_id = graphene.String(required=True)


class MenuItemNotFound(graphene.ObjectType):
    menu_item_id = graphene.String(required=True)


class InvalidQuantity(graphene.ObjectType):
    quantity = graphene.Int(required=True)


class CartItemNotFound(graphene.ObjectType):
    cart_item_id = graphene.Int(required=True)


class RestaurantAlreadyReviewedByUser(graphene.ObjectType):
    user_id = graphene.String(required=True)


class InvalidRatingFound(graphene.ObjectType):
    user_rating = graphene.Int(required=True)


class InvalidDateRange(graphene.ObjectType):
    date_from = graphene.Date(required=True)
    date_to = graphene.Date(required=True)


class InvalidOffset(graphene.ObjectType):
    offset = graphene.Int(required=True)


class InvalidLimit(graphene.ObjectType):
    limit = graphene.Int(required=True)


class InvalidDayOfWeek(graphene.ObjectType):
    day_of_week = graphene.Int(required=True)
