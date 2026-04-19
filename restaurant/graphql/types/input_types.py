import graphene


class UpdateRestaurantTimingInputParams(graphene.InputObjectType):
    id = graphene.Int(required=True)
    open_time = graphene.Time()
    close_time = graphene.Time()


class CreateMenuItemInputParams(graphene.InputObjectType):
    restaurant_id = graphene.String(required=True)
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    price = graphene.Float(required=True)
    category = graphene.String(required=True)
    is_veg = graphene.Boolean(required=True)
    is_available = graphene.Boolean(required=True)
    preparation_time_in_minutes = graphene.Int(required=True)
    tags = graphene.List(graphene.String)


class CreateMenuItemsInputParams(graphene.InputObjectType):
    menu_items = graphene.List(CreateMenuItemInputParams)


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