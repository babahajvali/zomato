import pytest
from account.models import User, Address
from account.management.commands.import_users import import_users_and_addresses
import uuid


@pytest.fixture
def sample_user(db):
    return User.objects.create(
        user_id=uuid.uuid4(),
        name='Ravi Kumar',
        email='ravi@example.com',
        phone_number='9876543210',
        role='OWNER'
    )


class TestDataPopulateForUsersAndAddress:

    @pytest.mark.django_db
    def test_new_users_and_addresses_created_from_valid_csv(self, tmp_path):
        uid1 = str(uuid.uuid4())
        uid2 = str(uuid.uuid4())

        users_file = tmp_path / "users.csv"
        addresses_file = tmp_path / "addresses.csv"

        users_file.write_text(
            f"user_id,name,email,phone_number,role\n"
            f"{uid1},Ravi Kumar,ravi@example.com,9876543210,OWNER\n"
            f"{uid2},John Doe,john@example.com,9876543211,CUSTOMER\n"
        )

        addresses_file.write_text(
            f"user_id,label,full_address,city,pin_code,is_default\n"
            f"{uid2},home,123 MG Road,Bangalore,560001,True\n"
            f"{uid2},work,456 Brigade Road,Bangalore,560025,False\n"
        )

        import_users_and_addresses(str(users_file), str(addresses_file))

        assert User.objects.count() == 2
        assert Address.objects.filter(user__user_id=uid2).count() == 2

    @pytest.mark.django_db
    def test_duplicate_user_skips_creation_but_still_adds_new_address(
            self, tmp_path, sample_user):
        uid = str(sample_user.user_id)

        users_file = tmp_path / "users.csv"
        addresses_file = tmp_path / "addresses.csv"

        users_file.write_text(
            f"user_id,name,email,phone_number,role\n"
            f"{uid},Ravi Kumar,ravi@example.com,9876543210,OWNER\n"
        )

        addresses_file.write_text(
            f"user_id,label,full_address,city,pin_code,is_default\n"
            f"{uid},home,123 MG Road,Bangalore,560001,True\n"
        )

        import_users_and_addresses(str(users_file), str(addresses_file))

        assert User.objects.filter(user_id=uid).count() == 1
        assert Address.objects.filter(user=sample_user, label='home').exists()

    @pytest.mark.django_db
    def test_owner_with_empty_address_fields_creates_user_without_address(
            self, tmp_path):
        uid = str(uuid.uuid4())

        users_file = tmp_path / "users.csv"
        addresses_file = tmp_path / "addresses.csv"

        users_file.write_text(
            f"user_id,name,email,phone_number,role\n"
            f"{uid},Ravi Kumar,ravi@example.com,9876543210,OWNER\n"
        )

        addresses_file.write_text(
            "user_id,label,full_address,city,pin_code,is_default\n"
        )

        import_users_and_addresses(str(users_file), str(addresses_file))

        assert User.objects.filter(user_id=uid).exists()
        assert Address.objects.filter(user__user_id=uid).count() == 0

    @pytest.mark.django_db
    def test_first_address_for_user_gets_is_default_true(self, tmp_path):
        uid = str(uuid.uuid4())

        users_file = tmp_path / "users.csv"
        addresses_file = tmp_path / "addresses.csv"

        users_file.write_text(
            f"user_id,name,email,phone_number,role\n"
            f"{uid},John Doe,john@example.com,9876543211,CUSTOMER\n"
        )

        addresses_file.write_text(
            f"user_id,label,full_address,city,pin_code,is_default\n"
            f"{uid},home,123 MG Road,Bangalore,560001,True\n"
            f"{uid},work,456 Brigade Road,Bangalore,560025,False\n"
        )

        import_users_and_addresses(str(users_file), str(addresses_file))

        addresses = Address.objects.filter(user__user_id=uid).order_by('id')

        assert addresses[0].is_default is True
        assert addresses[1].is_default is False

    @pytest.mark.django_db
    def test_rerunning_same_csv_is_idempotent(self, tmp_path):
        uid1 = str(uuid.uuid4())
        uid2 = str(uuid.uuid4())

        users_file = tmp_path / "users.csv"
        addresses_file = tmp_path / "addresses.csv"

        users_file.write_text(
            f"user_id,name,email,phone_number,role\n"
            f"{uid1},Ravi Kumar,ravi@example.com,9876543210,OWNER\n"
            f"{uid2},John Doe,john@example.com,9876543211,CUSTOMER\n"
        )

        addresses_file.write_text(
            f"user_id,label,full_address,city,pin_code,is_default\n"
            f"{uid2},home,123 MG Road,Bangalore,560001,True\n"
        )

        import_users_and_addresses(str(users_file), str(addresses_file))
        import_users_and_addresses(str(users_file), str(addresses_file))

        assert User.objects.count() == 2
        assert Address.objects.count() == 1
