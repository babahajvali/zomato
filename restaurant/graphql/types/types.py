import graphene


class RestaurantTimingType(graphene.ObjectType):
    id = graphene.Int(required=True)
    restaurant_id = graphene.String(required=True)
    day_of_week = graphene.Int(required=True)
    open_time = graphene.Time(required=True)
    close_time = graphene.Time(required=True)

class MenuItemType(graphene.ObjectType):
    item_id = graphene.String(required=True)
    restaurant_id = graphene.String(required=True)
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    price = graphene.Float(required=True)
    category = graphene.String(required=True)
    is_veg = graphene.Boolean(required=True)
    is_available = graphene.Boolean(required=True)
    preparation_time_in_minutes = graphene.Int(required=True)
    tags = graphene.List(graphene.String)


class MenuItemsType(graphene.ObjectType):
    menu_items = graphene.List(MenuItemType)


class BrowseRestaurantType(graphene.ObjectType):
    restaurant_id = graphene.String(required=True)
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    cuisine_type = graphene.String(required=True)
    address = graphene.String(required=True)
    pin_code = graphene.String(required=True)
    is_veg_only = graphene.Boolean(required=True)
    is_active = graphene.Boolean(required=True)
    average_rating = graphene.Float(required=True)
    total_reviews = graphene.Int(required=True)
    is_open = graphene.Boolean(required=True)


class BrowseRestaurantsType(graphene.ObjectType):
    restaurants = graphene.List(BrowseRestaurantType, required=True)
