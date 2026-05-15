import pytest

from accounts.tests.api_tests.user import BaseUpdateUserTestCase
from accounts.tests.factories.storage_factories import UserFactory


@pytest.mark.django_db
class TestUpdateUserApi(BaseUpdateUserTestCase):
    def test_update_user_successfully(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(
            id=user_id,
            email="sample@gmail.com",
            name="Old Name",
            phone_number="9000000000",
        )
        variables = {
            "params": {
                "userId": user_id,
                "name": "New Name",
                "phoneNumber": "9876543210",
            }
        }

        self.execute_schema(
            query=self.QUERY, variables=variables, snapshot=snapshot, user_id=user_id
        )

    def test_update_user_with_phone_number_only(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(
            id=user_id,
            email="sample@gmail.com",
            name="Old Name",
            phone_number="9000000000",
        )
        variables = {
            "params": {
                "userId": user_id,
                "phoneNumber": "9876543210",
            }
        }

        self.execute_schema(
            query=self.QUERY, variables=variables, snapshot=snapshot, user_id=user_id
        )

    def test_update_user_not_found(self, snapshot):
        variables = {
            "params": {
                "userId": "49bb508e-c6d1-4882-95fd-1991d103f7cd",
                "name": "New Name",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            user_id="49bb508e-c6d1-4882-95fd-1991d103f7cd",
        )

    def test_update_user_with_empty_name(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id, email="sample@gmail.com")
        variables = {
            "params": {
                "userId": user_id,
                "name": "",
            }
        }

        self.execute_schema(
            query=self.QUERY, variables=variables, snapshot=snapshot, user_id=user_id
        )

    def test_update_user_with_no_properties(self, snapshot):
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7cd"
        UserFactory(id=user_id, email="sample@gmail.com")
        variables = {
            "params": {
                "userId": user_id,
            }
        }

        self.execute_schema(
            query=self.QUERY, variables=variables, snapshot=snapshot, user_id=user_id
        )
