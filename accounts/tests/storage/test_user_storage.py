from django.test import TestCase

from accounts.models import User
from accounts.storages.user_storage import UserStorage
from accounts.tests.factories.interactor_factories import (
    CreateUserDTOFactory,
    UpdateUserDTOFactory,
    UserCreateDTOFactory,
)
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

        result = self.storage.get_users_by_emails(
            emails=["alice@example.com", "notfound@example.com"]
        )

        assert len(result) == 1
        assert result[0].email == "alice@example.com"

    def test_check_user_exists(self):
        user = UserFactory()

        assert self.storage.check_user_exists(user_id=str(user.id)) is True
        assert (
            self.storage.check_user_exists(
                user_id="00000000-0000-0000-0000-000000000000"
            )
            is False
        )

    def test_get_user_by_email_success(self):
        user = UserFactory(email="sample@gmail.com")

        result = self.storage.get_user_by_email(email="sample@gmail.com")

        assert result.id == str(user.id)
        assert result.email == "sample@gmail.com"

    def test_get_user_by_email_returns_none_when_user_not_found(self):
        result = self.storage.get_user_by_email(email="missing@gmail.com")

        assert result is None

    def test_get_user_success(self):
        user = UserFactory(name="Sample User")

        result = self.storage.get_user(user_id=str(user.id))

        assert result.id == str(user.id)
        assert result.name == "Sample User"

    def test_get_user_returns_none_when_user_not_found(self):
        result = self.storage.get_user(user_id="00000000-0000-0000-0000-000000000000")

        assert result is None

    def test_create_user_success(self):
        create_user_dto = UserCreateDTOFactory(
            name="Sample User",
            email="sample@gmail.com",
            phone_number="9876543210",
            password="password123",
        )

        result = self.storage.create_user(create_user_dto=create_user_dto)

        assert result.name == "Sample User"
        assert result.email == "sample@gmail.com"
        assert result.phone_number == "9876543210"
        assert User.objects.filter(email="sample@gmail.com").exists()

    def test_update_user_success(self):
        user = UserFactory(name="Old Name", phone_number="9000000000")
        update_user_dto = UpdateUserDTOFactory(
            user_id=str(user.id), name="New Name", phone_number="9999999999"
        )

        result = self.storage.update_user(update_user_dto=update_user_dto)

        user.refresh_from_db()
        assert result.id == str(user.id)
        assert result.name == "New Name"
        assert result.phone_number == "9999999999"
        assert user.name == "New Name"
        assert user.phone_number == "9999999999"

    def test_update_user_with_name_only_success(self):
        user = UserFactory(name="Old Name", phone_number="9000000000")
        update_user_dto = UpdateUserDTOFactory(
            user_id=str(user.id), name="New Name", phone_number=None
        )

        result = self.storage.update_user(update_user_dto=update_user_dto)

        user.refresh_from_db()
        assert result.name == "New Name"
        assert result.phone_number == "9000000000"
        assert user.name == "New Name"
        assert user.phone_number == "9000000000"
