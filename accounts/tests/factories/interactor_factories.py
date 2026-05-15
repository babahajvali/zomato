import factory

from accounts.constants.enums import Role
from accounts.interactors.dtos import (
    AddressDTO,
    CreateUserDTO,
    UpdateUserDTO,
    UserCreateDTO,
    UserDTO,
)


class CreateUserDTOFactory(factory.Factory):
    class Meta:
        model = CreateUserDTO

    id = factory.Sequence(lambda n: f"user-{n}")
    name = factory.Faker("name")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    phone_number = factory.Sequence(lambda n: f"900000{n:04d}")
    role = Role.CUSTOMER.value


class UserDTOFactory(factory.Factory):
    class Meta:
        model = UserDTO

    id = factory.Sequence(lambda n: f"user-{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    phone_number = factory.Sequence(lambda n: f"900000{n:04d}")
    role = Role.CUSTOMER.value


class UserCreateDTOFactory(factory.Factory):
    class Meta:
        model = UserCreateDTO

    name = factory.Faker("name")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    phone_number = factory.Sequence(lambda n: f"900000{n:04d}")
    role = Role.CUSTOMER
    password = factory.Faker("password")


class UpdateUserDTOFactory(factory.Factory):
    class Meta:
        model = UpdateUserDTO

    user_id = factory.Sequence(lambda n: f"user-{n}")
    name = factory.Faker("name")
    phone_number = factory.Sequence(lambda n: f"900000{n:04d}")


class AddressDTOFactory(factory.Factory):
    class Meta:
        model = AddressDTO

    address_id = factory.Sequence(lambda n: n + 1)
    full_address = factory.Faker("address")
    city = factory.Faker("city")
    pincode = factory.Sequence(lambda n: f"500{n:03d}")
    label = factory.Sequence(lambda n: f"label-{n}")
    is_default = False
    user_id = factory.Sequence(lambda n: f"user-{n}")
