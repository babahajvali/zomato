import factory

from restaurant.enums import Category
from restaurant.interactors.dtos import (
    CreateMenuItemDTO,
    CreateRestaurantDTO,
    MenuItemDTO,
)


class CreateRestaurantDTOFactory(factory.Factory):
    class Meta:
        model = CreateRestaurantDTO

    name = factory.Sequence(lambda n: f"Restaurant {n}")
    owner_email = factory.Sequence(lambda n: f"owner{n}@example.com")
    description = factory.Faker("sentence")
    cuisine_type = "Indian"
    address = factory.Faker("address")
    pin_code = factory.Sequence(lambda n: f"500{n:03d}")
    is_veg_only = False
    is_active = True


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

    item_id = factory.Sequence(lambda n: f"item-{n}")
    restaurant_id = factory.Sequence(lambda n: f"restaurant-{n}")
    name = factory.Sequence(lambda n: f"Item {n}")
    description = factory.Faker("sentence")
    price = 199.0
    is_veg = True
    is_available = True
    preparation_time_in_minutes = 15
    tags = factory.LazyFunction(list)
    category = Category.STARTER

