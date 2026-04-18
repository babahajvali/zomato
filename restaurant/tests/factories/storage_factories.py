from datetime import time

import factory
from factory.django import DjangoModelFactory

from account.tests.factories.storage_factories import UserFactory
from restaurant.models import Restaurant, RestaurantTiming


class RestaurantFactory(DjangoModelFactory):
    class Meta:
        model = Restaurant

    name = factory.Sequence(lambda n: f"Restaurant {n}")
    description = factory.Faker("sentence")
    owner = factory.SubFactory(UserFactory, role="OWNER")
    cuisine_type = "NORTH_INDIAN"
    address = factory.Faker("address")
    pin_code = factory.Sequence(lambda n: f"500{n:03d}")
    is_veg_only = False
    is_active = True


class RestaurantTimingFactory(DjangoModelFactory):
    class Meta:
        model = RestaurantTiming

    restaurant = factory.SubFactory(RestaurantFactory)
    day_of_week = 1
    open_time = time(9, 0)
    close_time = time(21, 0)
