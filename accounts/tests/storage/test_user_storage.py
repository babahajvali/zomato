from django.test import TestCase

from accounts.models import User
from accounts.storages.user_storage import UserStorage
from accounts.tests.factories.interactor_factories import CreateUserDTOFactory
from accounts.tests.factories.storage_factories import UserFactory


class TestUserStorage(TestCase):
    def setUp(self):
        self.storage = UserStorage()

    def test_create_bulk_users_success(self):
        users_dto = [
            CreateUserDTOFactory(
                name="Alice",
                email="alice@example.com",
                phone_number="9999999999",
                role="OWNER",
            ),
            CreateUserDTOFactory(
                name="Bob",
                email="bob@example.com",
                phone_number="8888888888",
                role="CUSTOMER",
            ),
        ]

        result = self.storage.create_bulk_users(create_user_dtos=users_dto)

        assert len(result) == 2
        assert User.objects.filter(email="alice@example.com").exists()
        assert User.objects.filter(email="bob@example.com").exists()

    def test_get_existing_emails(self):
        UserFactory(email="alice@example.com")
        UserFactory(email="bob@example.com")

        result = self.storage.get_existing_emails(
            emails=["alice@example.com", "notfound@example.com"]
        )

        assert result == ["alice@example.com"]

    def test_check_user_exists(self):
        user = UserFactory()

        assert self.storage.check_user_exists(user_id=str(user.id)) is True
        assert (
            self.storage.check_user_exists(
                user_id="00000000-0000-0000-0000-000000000000"
            )
            is False
        )
