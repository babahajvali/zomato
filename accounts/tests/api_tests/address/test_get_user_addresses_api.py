import pytest
from django.core.cache import cache

from accounts.tests.api_tests.address import BaseGetUserAddressesTestCase
from accounts.tests.factories.storage_factories import AddressFactory, UserFactory

import factory.random

factory.random.reseed_random(123)


@pytest.mark.django_db
class TestGetUserAddressesApi(BaseGetUserAddressesTestCase):
    def setup_method(self):
        cache.clear()

    def test_get_user_addresses_successfully(self, snapshot):
        # Arrange
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        user = UserFactory(id=user_id)
        AddressFactory(user=user, label="Home", is_default=True)
        AddressFactory(user=user, label="Office", is_default=False)

        # Act & Assert
        self.execute_schema(
            query=self.QUERY,
            variables={},
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_get_user_addresses_empty(self, snapshot):
        # Arrange
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id)

        # Act & Assert
        self.execute_schema(
            query=self.QUERY,
            variables={},
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_user_not_found(self, snapshot):
        # Arrange
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"

        # Act & Assert
        self.execute_schema(
            query=self.QUERY,
            variables={},
            snapshot=snapshot,
            user_id=user_id,
        )
