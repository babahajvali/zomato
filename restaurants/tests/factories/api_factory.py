import factory
from datetime import time

from restaurants.interactors.dtos import RestaurantTimingDTO
from restaurants.constants.enums import Category


class RestaurantTimingDTOFactory(factory.Factory):
    class Meta:
        model = RestaurantTimingDTO

    id = factory.Sequence(lambda n: n)
    restaurant_id = factory.Faker("uuid4")
    day_of_week = factory.Sequence(lambda n: (n % 7) + 1)
    open_time = factory.LazyFunction(lambda: time(9, 0))
    close_time = factory.LazyFunction(lambda: time(21, 0))


class MenuItemDTOFactory(factory.Factory):
    class Meta:
        model = dict

    item_id = factory.Faker("uuid4")
    restaurant_id = factory.Faker("uuid4")
    name = factory.Sequence(lambda n: f"Item {n}")
    description = factory.Faker("sentence")
    price = factory.Faker("pyfloat", left_digits=3, right_digits=2, positive=True)
    category = factory.LazyFunction(lambda: Category.STARTER.value)
    is_veg = factory.Faker("boolean")
    is_available = True
    preparation_time_in_minutes = factory.Faker("random_int", min=10, max=60)
    tags = factory.LazyFunction(lambda: ["spicy", "popular", "fresh"])


class RestaurantDTOFactory(factory.Factory):
    class Meta:
        model = dict

    restaurant_id = factory.Faker("uuid4")
    name = factory.Sequence(lambda n: f"Restaurant {n}")
    description = factory.Faker("sentence")
    cuisine_type = factory.LazyFunction(lambda: "NORTH_INDIAN")
    address = factory.Faker("address")
    pin_code = factory.Sequence(lambda n: f"500{n:03d}")
    is_veg_only = factory.Faker("boolean")
    is_active = True
    average_rating = factory.Faker(
        "pyfloat", left_digits=1, right_digits=1, min=0, max=5
    )
    total_reviews = factory.Faker("random_int", min=0, max=1000)
    is_open = factory.Faker("boolean")


class CartItemDTOFactory(factory.Factory):
    class Meta:
        model = dict

    cart_item_id = factory.Sequence(lambda n: n)
    cart_id = factory.Faker("uuid4")
    menu_item_id = factory.Faker("uuid4")
    quantity = factory.Faker("random_int", min=0, max=10)
    item_price = factory.Faker("pyfloat", left_digits=5, right_digits=2, positive=True)
