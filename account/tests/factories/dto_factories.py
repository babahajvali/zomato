import factory

from account.interactors.dtos import CreateAddressDTO, CreateUserDTO, UserDTO


class CreateUserDTOFactory(factory.Factory):
    class Meta:
        model = CreateUserDTO

    name = factory.Faker("name")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    phone_number = factory.Sequence(lambda n: f"900000{n:04d}")
    role = "CUSTOMER"


class CreateAddressDTOFactory(factory.Factory):
    class Meta:
        model = CreateAddressDTO

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    label = factory.Sequence(lambda n: f"label-{n}")
    full_address = factory.Faker("address")
    city = factory.Faker("city")
    pincode = factory.Sequence(lambda n: f"500{n:03d}")
    is_default = False

class UserDTOFactory(factory.Factory):
    class Meta:
        model = UserDTO

    id = factory.Sequence(lambda n: n)
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    phone_number = factory.Sequence(lambda n: f"900000{n:04d}")
    role = "CUSTOMER"