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
