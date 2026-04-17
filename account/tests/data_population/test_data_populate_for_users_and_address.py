import pytest
from account.models import User, Address
from account.management.commands.import_users import import_users_and_addresses
import uuid


class TestDataPopulateForUsersAndAddress:

    @pytest.mark.django_db
    def test_new_users_and_addresses_created_from_valid_csv(self, tmp_path):
        users_file = tmp_path / "users.csv"
        addresses_file = tmp_path / "addresses.csv"

        users_file.write_text(
            "user_id,name,email,phone_number,role\n"
            f"{uuid.uuid4()},Ravi Kumar,ravi@example.com,9876543210,OWNER\n"
            f"{uuid.uuid4()},John Doe,john@example.com,9876543211,CUSTOMER\n"
        )

        addresses_file.write_text(
            "email,label,full_address,city,pin_code\n"
            "john@example.com,home,123 MG Road,Bangalore,560001\n"
            "john@example.com,work,456 Brigade Road,Bangalore,560025\n"
        )

        import_users_and_addresses(str(users_file), str(addresses_file))

        assert User.objects.count() == 2
        assert Address.objects.filter(user__email="john@example.com").count() == 2

    @pytest.mark.django_db
    def test_duplicate_user_skips_creation_but_still_adds_new_address(self, tmp_path):
        user = User.objects.create(
            user_id=uuid.uuid4(),
            name='Ravi Kumar',
            email='ravi@example.com',
            phone_number='9876543210',
            role='OWNER'
        )

        users_file = tmp_path / "users.csv"
        addresses_file = tmp_path / "addresses.csv"

        users_file.write_text(
            "user_id,name,email,phone_number,role\n"
            f"{uuid.uuid4()},Ravi Kumar,ravi@example.com,9876543210,OWNER\n"
        )

        addresses_file.write_text(
            "email,label,full_address,city,pin_code\n"
            "ravi@example.com,home,123 MG Road,Bangalore,560001\n"
        )

        import_users_and_addresses(str(users_file), str(addresses_file))

        assert User.objects.filter(email="ravi@example.com").count() == 1
        assert Address.objects.filter(user=user, label='home').exists()

    @pytest.mark.django_db
    def test_owner_with_empty_address_fields_creates_user_without_address(self, tmp_path):
        users_file = tmp_path / "users.csv"
        addresses_file = tmp_path / "addresses.csv"

        users_file.write_text(
            "user_id,name,email,phone_number,role\n"
            f"{uuid.uuid4()},Ravi Kumar,ravi@example.com,9876543210,OWNER\n"
        )

        addresses_file.write_text(
            "email,label,full_address,city,pin_code\n"
        )

        import_users_and_addresses(str(users_file), str(addresses_file))

        assert User.objects.filter(email="ravi@example.com").exists()
        assert Address.objects.count() == 0

    @pytest.mark.django_db
    def test_first_address_for_user_gets_is_default_true(self, tmp_path):
        users_file = tmp_path / "users.csv"
        addresses_file = tmp_path / "addresses.csv"

        users_file.write_text(
            "user_id,name,email,phone_number,role\n"
            f"{uuid.uuid4()},John Doe,john@example.com,9876543211,CUSTOMER\n"
        )

        addresses_file.write_text(
            "email,label,full_address,city,pin_code\n"
            "john@example.com,home,123 MG Road,Bangalore,560001\n"
            "john@example.com,work,456 Brigade Road,Bangalore,560025\n"
        )

        import_users_and_addresses(str(users_file), str(addresses_file))

        addresses = Address.objects.filter(user__email="john@example.com").order_by('id')

        assert addresses[0].is_default is True
        assert addresses[1].is_default is False

    @pytest.mark.django_db
    def test_rerunning_same_csv_is_idempotent(self, tmp_path):
        users_file = tmp_path / "users.csv"
        addresses_file = tmp_path / "addresses.csv"

        users_file.write_text(
            "user_id,name,email,phone_number,role\n"
            f"{uuid.uuid4()},Ravi Kumar,ravi@example.com,9876543210,OWNER\n"
            f"{uuid.uuid4()},John Doe,john@example.com,9876543211,CUSTOMER\n"
        )

        addresses_file.write_text(
            "email,label,full_address,city,pin_code\n"
            "john@example.com,home,123 MG Road,Bangalore,560001\n"
        )

        import_users_and_addresses(str(users_file), str(addresses_file))
        import_users_and_addresses(str(users_file), str(addresses_file))

        assert User.objects.count() == 2
        assert Address.objects.count() == 1