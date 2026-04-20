from datetime import time
import uuid

import factory
from factory.django import DjangoModelFactory

from restaurant.models import MenuItem, Restaurant, RestaurantTiming


class RestaurantFactory(DjangoModelFactory):
    class Meta:
        model = Restaurant

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Sequence(lambda n: f"Restaurant {n}")
    description = factory.Faker("sentence")
    owner_id = factory.Sequence(lambda n: f"00000000-0000-0000-0000-{n:012d}")
    cuisine_type = "NORTH_INDIAN"
    address = factory.Faker("address")
    pin_code = factory.Sequence(lambda n: f"500{n:03d}")
    is_veg_only = False
    is_deleted = False


class RestaurantTimingFactory(DjangoModelFactory):
    class Meta:
        model = RestaurantTiming
    id = factory.Sequence(lambda n: n)
    restaurant = factory.SubFactory(RestaurantFactory)
    day_of_week = factory.Sequence(lambda n: (n % 7) + 1)
    open_time = time(9, 0)
    close_time = time(21, 0)


class MenuItemFactory(DjangoModelFactory):
    class Meta:
        model = MenuItem

    id = factory.LazyFunction(uuid.uuid4)
    restaurant = factory.SubFactory(RestaurantFactory)
    name = factory.Sequence(lambda n: f"Item {n}")
    description = factory.Faker("sentence")
    price = 199.0
    category = "STARTER"
    is_veg = True
    is_available = True
    preparation_time_in_minutes = 15
    tags = factory.LazyFunction(list)
