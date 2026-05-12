import graphene


class UpdateRestaurantTimingInputParams(graphene.InputObjectType):
    timing_id = graphene.Int(required=True)
    open_time = graphene.Time()
    close_time = graphene.Time()


class DeleteRestaurantTimingInputParams(graphene.InputObjectType):
    timing_id = graphene.Int(required=True)


class GetRestaurantTimingsInputParams(graphene.InputObjectType):
    restaurant_id = graphene.String(required=True)


class CreateMenuItemInputParams(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    price = graphene.Float(required=True)
    category = graphene.String(required=True)
    is_veg = graphene.Boolean(required=True)
    is_available = graphene.Boolean(required=True)
    preparation_time_in_minutes = graphene.Int(required=True)
    tags = graphene.List(graphene.String)


class CreateMenuItemsInputParams(graphene.InputObjectType):
    restaurant_id = graphene.String(required=True)
    menu_items = graphene.List(CreateMenuItemInputParams, required=True)


class BrowseRestaurantsInputParams(graphene.InputObjectType):
    cuisine_type = graphene.String()
    is_veg_only = graphene.Boolean()
    pincode = graphene.String()
    min_rating = graphene.Float()
    search = graphene.String()
    limit = graphene.Int()
    offset = graphene.Int()


class ViewRestaurantMenuInputParams(graphene.InputObjectType):
    restaurant_id = graphene.String(required=True)


class UpdateCartItemInputParams(graphene.InputObjectType):
    cart_id = graphene.String(required=True)
    menu_item_id = graphene.String(required=True)
    quantity = graphene.Int(required=True)


class RemoveCartItemInputParams(graphene.InputObjectType):
    cart_item_id = graphene.Int(required=True)


class ClearCartItemsInputParams(graphene.InputObjectType):
    cart_id = graphene.String(required=True)


class GetCartItemsInputParams(graphene.InputObjectType):
    cart_id = graphene.String(required=True)


class CreateReviewInputParams(graphene.InputObjectType):
    restaurant_id = graphene.String(required=True)
    rating = graphene.Int(required=True)
    review = graphene.String()


class GetRestaurantDashboardInputParams(graphene.InputObjectType):
    restaurant_id = graphene.String(required=True)
    date_from = graphene.Date(required=True)
    date_to = graphene.Date(required=True)


class CreateRestaurantTimingInputParams(graphene.InputObjectType):
    restaurant_id = graphene.String(required=True)
    day_of_week = graphene.Int(required=True)
    open_time = graphene.Time()
    close_time = graphene.Time()


class UpdateMenuItemInputParams(graphene.InputObjectType):
    menu_item_id = graphene.String(required=True)
    name = graphene.String()
    price = graphene.Decimal()
    is_available = graphene.Boolean()
    preparation_time_in_minutes = graphene.Int()
    tags = graphene.List(graphene.String)


class DeleteMenuItemInputParams(graphene.InputObjectType):
    menu_item_id = graphene.String(required=True)


class GetUserRestaurantReviewInputParams(graphene.InputObjectType):
    restaurant_id = graphene.String(required=True)
    user_id = graphene.String(required=True)


class GetScoredRestaurantsInputParams(graphene.InputObjectType):
    pincode = graphene.String(required=True)
    limit = graphene.Int(required=True)
    offset = graphene.Int(required=True)


class GetScoredRestaurantItemsInputParams(graphene.InputObjectType):
    restaurant_id = graphene.String(required=True)
    limit = graphene.Int(required=True)
    offset = graphene.Int(required=True)
