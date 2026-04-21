import graphene


class RestaurantTimingType(graphene.ObjectType):
    id = graphene.Int(required=True)
    restaurant_id = graphene.String(required=True)
    day_of_week = graphene.Int(required=True)
    open_time = graphene.Time(required=True)
    close_time = graphene.Time(required=True)


class DeleteRestaurantTimingSuccessType(graphene.ObjectType):
    timing_id = graphene.Int(required=True)
    success = graphene.Boolean(required=True)


class RestaurantTimingsListType(graphene.ObjectType):
    restaurant_id = graphene.String(required=True)
    timings = graphene.List(RestaurantTimingType, required=True)


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
    is_deleted = graphene.Boolean(required=True)
    average_rating = graphene.Float(required=True)
    total_reviews = graphene.Int(required=True)
    is_open = graphene.Boolean(required=True)


class BrowseRestaurantsType(graphene.ObjectType):
    restaurants = graphene.List(BrowseRestaurantType, required=True)


class ViewMenuItemType(graphene.ObjectType):
    item_id = graphene.String()
    name = graphene.String()
    description = graphene.String()
    price = graphene.Float()
    category = graphene.String()
    is_veg = graphene.Boolean()
    is_available = graphene.Boolean()
    preparation_time_in_minutes = graphene.Int()
    tags = graphene.List(graphene.String)


class CategoryMenuType(graphene.ObjectType):
    category = graphene.String()
    items = graphene.List(ViewMenuItemType)


class RestaurantMenuType(graphene.ObjectType):
    restaurant_id = graphene.String(required=True)
    categories = graphene.List(CategoryMenuType)


class CartItemType(graphene.ObjectType):
    cart_item_id = graphene.Int(required=True)
    cart_id = graphene.String(required=True)
    menu_item_id = graphene.String(required=True)
    quantity = graphene.Int(required=True)
    item_price = graphene.Float(required=True)


class CartItemsType(graphene.ObjectType):
    cart_items = graphene.List(CartItemType)


class RemoveCartItemSuccessType(graphene.ObjectType):
    success = graphene.Boolean(required=True)
    cart_item_id = graphene.Int(required=True)


class ClearCartItemsSuccessType(graphene.ObjectType):
    success = graphene.Boolean(required=True)
    cart_id = graphene.String(required=True)
