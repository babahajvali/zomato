from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from accounts.models import Address
from accounts.storages.address_storage import AddressStorage
from accounts.interactors.dtos import AddressLookupDTO, CreateAddressDTO, UpdateAddressDTO
from accounts.tests.factories.storage_factories import AddressFactory, UserFactory


class TestAddressStorage(TestCase):
    def setUp(self):
        self.storage = AddressStorage()

    def test_create_bulk_addresses_with_valid_addresses_success(self):
        user = UserFactory(id="00000000-0000-0000-0000-000000000001")
        addresses_dto = [
            CreateAddressDTO(
                user_id=str(user.id),
                label="Home",
                full_address="12 MG Road",
                city="Bangalore",
                pincode=560001,
                is_default=False,
            )
        ]

        result = self.storage.create_bulk_addresses(address_dtos=addresses_dto)

        assert len(result) == 1
        created = Address.objects.get(user_id=user.id, label="Home")
        assert created.full_address == "12 MG Road"
        assert created.pincode == 560001

    def test_get_existing_addresses_with_matching_addresses_success(self):
        user = UserFactory(email="alice@example.com")
        AddressFactory(user=user, label="Home", pincode="500001")
        AddressFactory(user=user, label="Office", pincode="500002")

        result = self.storage.get_existing_addresses(
            address_pairs=[
                AddressLookupDTO(
                    user_id=str(user.id),
                    label="Home",
                    pincode=500001,
                ),
                AddressLookupDTO(
                    user_id=str(user.id),
                    label="Other",
                    pincode=500001,
                ),
            ],
        )

        assert len(result) == 1
        assert result[0].user_id == str(user.id)
        assert result[0].label == "Home"
        assert result[0].pincode == 500001

    def test_get_existing_addresses_with_empty_address_pairs_success(self):
        result = self.storage.get_existing_addresses(address_pairs=[])

        assert result == []

    def test_get_address_by_id_with_existing_address_success(self):
        user = UserFactory()
        address = AddressFactory(
            user=user,
            label="Home",
            full_address="221B Baker Street",
            city="London",
            pincode=560001,
            is_default=True,
        )

        result = self.storage.get_address_by_id(address_id=address.id)

        assert result.address_id == address.id
        assert result.user_id == str(user.id)
        assert result.label == "Home"
        assert result.full_address == "221B Baker Street"
        assert result.city == "London"
        assert result.pincode == 560001
        assert result.is_default is True

    def test_get_address_by_id_with_missing_address_success(self):
        result = self.storage.get_address_by_id(address_id=99999)

        assert result is None

    def test_get_user_addresses_returns_latest_addresses_first_success(self):
        user = UserFactory()
        old_address = AddressFactory(user=user, label="Home", pincode=560001)
        new_address = AddressFactory(user=user, label="Office", pincode=560002)
        AddressFactory(label="Other User", pincode=560003)
        now = timezone.now()
        Address.objects.filter(id=old_address.id).update(
            created_at=now - timedelta(days=1)
        )
        Address.objects.filter(id=new_address.id).update(created_at=now)

        result = self.storage.get_user_addresses(user_id=str(user.id))

        assert [address.address_id for address in result] == [
            new_address.id,
            old_address.id,
        ]
        assert [address.label for address in result] == ["Office", "Home"]

    def test_get_user_addresses_with_no_addresses_success(self):
        user = UserFactory()

        result = self.storage.get_user_addresses(user_id=str(user.id))

        assert result == []

    def test_update_bulk_addresses_with_valid_addresses_success(self):
        user = UserFactory()
        home = AddressFactory(
            user=user,
            label="Home",
            full_address="Old home",
            city="Bangalore",
            pincode=560001,
            is_default=True,
        )
        office = AddressFactory(
            user=user,
            label="Office",
            full_address="Old office",
            city="Bangalore",
            pincode=560002,
            is_default=False,
        )

        result = self.storage.update_bulk_addresses(
            address_dtos=[
                UpdateAddressDTO(
                    id=home.id,
                    user_id=str(user.id),
                    label="Home Updated",
                    full_address="New home",
                    city="Hyderabad",
                    pincode=500001,
                    is_default=False,
                ),
                UpdateAddressDTO(
                    id=office.id,
                    user_id=str(user.id),
                    label="Office Updated",
                    full_address="New office",
                    city="Chennai",
                    pincode=600001,
                    is_default=True,
                ),
            ]
        )

        home.refresh_from_db()
        office.refresh_from_db()

        assert len(result) == 2
        assert home.label == "Home Updated"
        assert home.full_address == "New home"
        assert home.city == "Hyderabad"
        assert home.pincode == 500001
        assert home.is_default is False
        assert office.label == "Office Updated"
        assert office.full_address == "New office"
        assert office.city == "Chennai"
        assert office.pincode == 600001
        assert office.is_default is True
