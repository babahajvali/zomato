from django.test import TestCase

from accounts.models import Address
from accounts.storages.address_storage import AddressStorage
from accounts.interactors.dtos import AddressLookupDTO, CreateAddressDTO
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

    def test_get_existing_addresses(self):
        user = UserFactory(email="alice@example.com")
        AddressFactory(user=user, label="Home", pin_code="500001")
        AddressFactory(user=user, label="Office", pin_code="500002")

        result = self.storage.get_existing_addresses(
            pairs=[
                AddressLookupDTO(
                    user_id=str(user.id),
                    label="Home",
                    pincode="500001",
                ),
                AddressLookupDTO(
                    user_id=str(user.id),
                    label="Other",
                    pincode="500001",
                ),
            ],
        )

        assert len(result) == 1
        assert result[0].user_id == str(user.id)
        assert result[0].label == "Home"
        assert result[0].pincode == "500001"
