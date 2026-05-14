import factory
import uuid
from factory.django import DjangoModelFactory

from accounts.constants.enums import Role
from accounts.models import Address, User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("name")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    phone_number = factory.Sequence(lambda n: f"900000{n:04d}")
    role = Role.CUSTOMER.value
    password = factory.Faker("password")


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    user = factory.SubFactory(UserFactory)
    label = factory.Sequence(lambda n: f"label-{n}")
    full_address = factory.Faker("address")
    city = factory.Faker("city")
    pincode = factory.Sequence(lambda n: f"500{n:03d}")
    is_default = False
