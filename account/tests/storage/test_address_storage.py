from django.test import TestCase

from account.exception.custom_exceptions import EmailNotFound
from account.models import Address
from account.storages.address_storage import AddressStorage
from account.tests.factories.dto_factories import CreateAddressDTOFactory
from account.tests.factories.storage_factories import AddressFactory, UserFactory


class TestAddressStorage(TestCase):
    def setUp(self):
        self.storage = AddressStorage()

    def test_create_bulk_addresses_success(self):
        UserFactory(email="alice@example.com")
        addresses_dto = [
            CreateAddressDTOFactory(
                email="alice@example.com",
                label="Home",
                full_address="12 MG Road",
                city="Bangalore",
                pincode="560001",
                is_default=False,
            )
        ]

        result = self.storage.create_bulk_addresses(address_dtos=addresses_dto)

        assert len(result) == 1
        created = Address.objects.get(user__email="alice@example.com", label="Home")
        assert created.full_address == "12 MG Road"
        assert created.pin_code == "560001"

    def test_create_bulk_addresses_user_not_found(self):
        addresses_dto = [
            CreateAddressDTOFactory(
                email="missing@example.com",
                label="Home",
            )
        ]

        with self.assertRaises(EmailNotFound) as exc:
            self.storage.create_bulk_addresses(address_dtos=addresses_dto)

        assert exc.exception.email == "missing@example.com"

    def test_get_existing_addresses(self):
        user = UserFactory(email="alice@example.com")
        AddressFactory(user=user, label="Home")
        AddressFactory(user=user, label="Office")

        result = self.storage.get_existing_addresses(
            emails=["alice@example.com"],
            labels=["Home", "Other"],
        )

        assert result == [("alice@example.com", "Home")]
