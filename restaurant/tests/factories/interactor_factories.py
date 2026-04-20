import factory

from restaurant.enums import Category
from restaurant.interactors.dtos import (
    CategoryMenuDTO,
    CreateMenuItemDTO,
    CreateRestaurantTimingDTO,
    CreateRestaurantDTO,
    MenuItemDTO,
    MenuItemWithTagsDTO,
    RestaurantMenuDTO, RestaurantTimingDTO, RestaurantDTO,
)


class CreateRestaurantDTOFactory(factory.Factory):
    class Meta:
        model = CreateRestaurantDTO

    name = factory.Sequence(lambda n: f"Restaurant {n}")
    owner_id = factory.Sequence(lambda n: f"00000000-0000-0000-0000-{n:012d}")
    description = factory.Faker("sentence")
    cuisine_type = "Indian"
    address = factory.Faker("address")
    pin_code = factory.Sequence(lambda n: f"500{n:03d}")
    is_veg_only = False
    is_deleted = False


class CreateMenuItemDTOFactory(factory.Factory):
    class Meta:
        model = CreateMenuItemDTO

    name = factory.Sequence(lambda n: f"Item {n}")
    description = factory.Faker("sentence")
    restaurant_id = factory.Sequence(lambda n: f"restaurant-{n}")
    category = Category.STARTER
    price = 199.0
    is_veg = True
    is_available = True
    preparation_time_in_minutes = 15
    tags = factory.LazyFunction(list)


class MenuItemDTOFactory(factory.Factory):
    class Meta:
        model = MenuItemDTO

    id = factory.Sequence(lambda n: f"item-{n}")
    restaurant_id = factory.Sequence(lambda n: f"restaurant-{n}")
    name = factory.Sequence(lambda n: f"Item {n}")
    description = factory.Faker("sentence")
    price = 199.0
    is_veg = True
    is_available = True
    preparation_time_in_minutes = 15
    tags = factory.LazyFunction(list)
    category = Category.STARTER


class CreateRestaurantTimingDTOFactory(factory.Factory):
    class Meta:
        model = CreateRestaurantTimingDTO

    restaurant_id = factory.Sequence(lambda n: f"restaurant-{n}")
    day_of_week = 1
    open_time = "09:00:00"
    close_time = "21:00:00"


class MenuItemWithTagsDTOFactory(factory.Factory):
    class Meta:
        model = MenuItemWithTagsDTO

    item_id = factory.Sequence(lambda n: f"item-{n}")
    name = factory.Sequence(lambda n: f"Item {n}")
    description = factory.Faker("sentence")
    price = 199.0
    category = Category.STARTER
    is_veg = True
    is_available = True
    preparation_time_in_minutes = 15
    tags = factory.LazyFunction(list)


class CategoryMenuDTOFactory(factory.Factory):
    class Meta:
        model = CategoryMenuDTO

    category = Category.STARTER
    items = factory.LazyFunction(list)


class RestaurantMenuDTOFactory(factory.Factory):
    class Meta:
        model = RestaurantMenuDTO

    restaurant_id = factory.Sequence(lambda n: f"restaurant-{n}")
    categories = factory.LazyFunction(list)



class RestaurantTimingDTOFactory(factory.Factory):
    class Meta:
        model = RestaurantTimingDTO

    id = factory.Sequence(lambda n: f"timing-{n}")
    restaurant_id = factory.Sequence(lambda n: f"restaurant-{n}")
    day_of_week = 1
    open_time = "09:00:00"
    close_time = "21:00:00"


class RestaurantDTOFactory(factory.Factory):
    class Meta:
        model = RestaurantDTO

    id = factory.Sequence(lambda n: f"restaurant-{n}")
    name = factory.Sequence(lambda n: f"Restaurant {n}")
    description = factory.Faker("sentence")
    owner_id = factory.Sequence(lambda n: f"00000000-0000-0000-0000-{n:012d}")
    cuisine_type = "NORTH_INDIAN"
    address = factory.Faker("address")
    pin_code = factory.Sequence(lambda n: f"500{n:03d}")
    is_veg_only = False
    is_deleted = False