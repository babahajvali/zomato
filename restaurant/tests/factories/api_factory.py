import factory
from datetime import time

from restaurant.interactors.dtos import RestaurantTimingDTO
from restaurant.constants.enums import Category


class UserDTOFactory(factory.Factory):
    class Meta:
        model = dict  # Using dict since UserDTO is likely a simple data transfer object

    user_id = factory.Faker('uuid4')


class RestaurantTimingDTOFactory(factory.Factory):
    class Meta:
        model = RestaurantTimingDTO

    id = factory.Sequence(lambda n: n)
    restaurant_id = factory.Faker('uuid4')
    day_of_week = factory.Sequence(lambda n: (n % 7) + 1)  # 1-7 for days of week
    open_time = factory.LazyFunction(lambda: time(9, 0))
    close_time = factory.LazyFunction(lambda: time(21, 0))


class MenuItemDTOFactory(factory.Factory):
    class Meta:
        model = dict  # Using dict since MenuItemDTO is likely a simple data transfer object

    item_id = factory.Faker('uuid4')
    restaurant_id = factory.Faker('uuid4')
    name = factory.Sequence(lambda n: f"Item {n}")
    description = factory.Faker('sentence')
    price = factory.Faker('pyfloat', left_digits=3, right_digits=2, positive=True)
    category = factory.LazyFunction(lambda: Category.STARTER.value)
    is_veg = factory.Faker('boolean')
    is_available = True
    preparation_time_in_minutes = factory.Faker('random_int', min=10, max=60)
    tags = factory.LazyFunction(lambda: ['spicy', 'popular', 'fresh'])


class RestaurantDTOFactory(factory.Factory):
    class Meta:
        model = dict  # Using dict since RestaurantDTO is likely a simple data transfer object

    restaurant_id = factory.Faker('uuid4')
    name = factory.Sequence(lambda n: f"Restaurant {n}")
    description = factory.Faker('sentence')
    cuisine_type = factory.LazyFunction(lambda: 'NORTH_INDIAN')
    address = factory.Faker('address')
    pin_code = factory.Sequence(lambda n: f"500{n:03d}")
    is_veg_only = factory.Faker('boolean')
    is_active = True
    average_rating = factory.Faker('pyfloat', left_digits=1, right_digits=1, min=0, max=5)
    total_reviews = factory.Faker('random_int', min=0, max=1000)
    is_open = factory.Faker('boolean')
