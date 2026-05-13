import factory

from accounts.constants.enums import Role
from accounts.interactors.dtos import AddressDTO, CreateAddressDTO, CreateUserDTO, UserDTO


class CreateUserDTOFactory(factory.Factory):
    class Meta:
        model = CreateUserDTO

    id = factory.Sequence(lambda n: f"user-{n}")
    name = factory.Faker("name")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    phone_number = factory.Sequence(lambda n: f"900000{n:04d}")
    role = Role.CUSTOMER.value


class CreateAddressDTOFactory(factory.Factory):
    class Meta:
        model = CreateAddressDTO

    # TODO: `email` doesn't exist on CreateAddressDTO and required `user_id` is missing — factory breaks if called without overrides.
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    label = factory.Sequence(lambda n: f"label-{n}")
    full_address = factory.Faker("address")
    city = factory.Faker("city")
    pincode = factory.Sequence(lambda n: f"500{n:03d}")
    is_default = False


class UserDTOFactory(factory.Factory):
    class Meta:
        model = UserDTO

    id = factory.Sequence(lambda n: f"user-{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    phone_number = factory.Sequence(lambda n: f"900000{n:04d}")
    role = Role.CUSTOMER.value


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
