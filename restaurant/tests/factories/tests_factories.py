import factory

from restaurant.Interactors.dtos import CreateRestaurantDTO


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

