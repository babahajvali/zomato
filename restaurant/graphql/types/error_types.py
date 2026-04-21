import graphene


class RestaurantTimingNotFoundType(graphene.ObjectType):
    id = graphene.Int(required=True)


class OpenTimeGreaterThanCloseTimeType(graphene.ObjectType):
    open_time = graphene.Time(required=True)
    close_time = graphene.Time(required=True)


class UserIsNotRestaurantOwnerType(graphene.ObjectType):
    user_id = graphene.String(required=True)


class RestaurantNotFoundType(graphene.ObjectType):
    restaurant_id = graphene.String(required=True)


class InvalidCategoriesFoundType(graphene.ObjectType):
    categories = graphene.List(graphene.String, required=True)


class InvalidCuisineTypeExceptionType(graphene.ObjectType):
    cuisine_type = graphene.String(required=True)


class InvalidMinRatingExceptionType(graphene.ObjectType):
    min_rating = graphene.Float(required=True)


class CartNotFound(graphene.ObjectType):
    cart_id = graphene.String(required=True)


class MenuItemNotFound(graphene.ObjectType):
    menu_item_id = graphene.String(required=True)


class InvalidQuantity(graphene.ObjectType):
    quantity = graphene.Int(required=True)


class CartItemNotFound(graphene.ObjectType):
    cart_item_id = graphene.Int(required=True)
