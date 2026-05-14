import pytest

from accounts.tests.api_tests.user import BaseCreateUserTestCase
from accounts.tests.factories.storage_factories import UserFactory


@pytest.mark.django_db
class TestCreateUserApi(BaseCreateUserTestCase):
    def test_create_user_successfully(self, snapshot):
        variables = {
            "params": {
                "name": "Sample User",
                "email": "sample@gmail.com",
                "phoneNumber": "9876543210",
                "role": "CUSTOMER",
                "password": "password123",
            }
        }

        self.execute_schema(query=self.QUERY, variables=variables, snapshot=snapshot)

    def test_create_user_with_existing_email(self, snapshot):
        UserFactory(email="sample@gmail.com")
        variables = {
            "params": {
                "name": "Sample User",
                "email": "sample@gmail.com",
                "phoneNumber": "9876543210",
                "role": "CUSTOMER",
                "password": "password123",
            }
        }

        self.execute_schema(query=self.QUERY, variables=variables, snapshot=snapshot)

    def test_create_user_with_empty_name(self, snapshot):
        variables = {
            "params": {
                "name": "   ",
                "email": "sample@gmail.com",
                "phoneNumber": "9876543210",
                "role": "CUSTOMER",
                "password": "password123",
            }
        }

        self.execute_schema(query=self.QUERY, variables=variables, snapshot=snapshot)
