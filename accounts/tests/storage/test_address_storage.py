from django.test import TestCase

from accounts.exception.custom_exceptions import UserNotFound
from accounts.models import Address
from accounts.storages.address_storage import AddressStorage
from accounts.interactors.dtos import CreateAddressDTO
from accounts.tests.factories.storage_factories import AddressFactory, UserFactory


class TestAddressStorage(TestCase):
    def setUp(self):
        self.storage = AddressStorage()

    def test_create_bulk_addresses_success(self):
        user = UserFactory(id="00000000-0000-0000-0000-000000000001")
        addresses_dto = [
            CreateAddressDTO(
                user_id=str(user.id),
                label="Home",
                full_address="12 MG Road",
                city="Bangalore",
                pincode="560001",
                is_default=False,
            )
        ]

        result = self.storage.create_bulk_addresses(address_dtos=addresses_dto)

        assert len(result) == 1
        created = Address.objects.get(user_id=user.id, label="Home")
        assert created.full_address == "12 MG Road"
        assert created.pin_code == "560001"

    def test_create_bulk_addresses_user_not_found(self):
        addresses_dto = [
            CreateAddressDTO(
                user_id="00000000-0000-0000-0000-000000000999",
                label="Home",
                full_address="12 MG Road",
                city="Bangalore",
                pincode="560001",
                is_default=False,
            )
        ]

        with self.assertRaises(UserNotFound) as exc:
            self.storage.create_bulk_addresses(address_dtos=addresses_dto)

        assert exc.exception.user_id == "00000000-0000-0000-0000-000000000999"

    def test_get_existing_addresses(self):
        user = UserFactory(email="alice@example.com")
        AddressFactory(user=user, label="Home")
        AddressFactory(user=user, label="Office")

        result = self.storage.get_existing_addresses(
            user_label_pairs=[(user.id, "Home"), (user.id, "Other")],
        )

        assert result == [(str(user.id), "Home")]
