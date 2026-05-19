from unittest.mock import patch

import pytest

from accounts.tests.api_tests.user import BaseUserLoginTestCase
from accounts.tests.factories.storage_factories import UserFactory
import factory.random

factory.random.reseed_random(123)
MOCK_TOKEN = "mocked.jwt.token"


@pytest.mark.django_db
class TestUserLoginApi(BaseUserLoginTestCase):
    def test_user_login_with_valid_credentials_success(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        user = UserFactory(
            id=user_id,
            email="sample@gmail.com",
            name="Joshua Gray",
            phone_number="9000000002",
            password="Ravi1234",
        )

        with patch(
            "accounts.graphql.mutation.user_login_mutation._generate_access_token",
            return_value=MOCK_TOKEN,
        ):
            self.execute_schema(
                query=self.QUERY,
                variables={"params": {"email": user.email, "password": "Ravi1234"}},
                snapshot=snapshot,
                user_id=user_id,
            )

    def test_user_login_with_missing_email_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id, email="sample@gmail.com", password="Ravi1234")

        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {"email": "sample1@gmail.com", "password": "Ravi1234"}
            },
            snapshot=snapshot,
            user_id=user_id,
        )

    def test_user_login_with_invalid_password_raises_error(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id, email="sample@gmail.com", password="Ravi1234")

        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {"email": "sample1@gmail.com", "password": "Ravi12345"}
            },
            snapshot=snapshot,
            user_id=user_id,
        )
