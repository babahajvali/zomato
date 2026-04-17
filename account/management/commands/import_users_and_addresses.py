import csv
from django.db import transaction

from account.models import User, Address


def import_users_and_addresses(
        users_file='./sample_data/users.csv',
        addresses_file='./sample_data/addresses.csv'
):
    created_users = skipped_users = 0
    created_addresses = updated_addresses = 0

    try:
        with transaction.atomic():

            with open(users_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if not row['email'].strip():
                        raise ValueError(f"Invalid user row: {row}")

                    user = User.objects.filter(email=row['email']).first()

                    if user:
                        skipped_users += 1
                        continue

                    User.objects.create(
                        user_id=row['user_id'],
                        name=row['name'],
                        email=row['email'],
                        phone_number=row['phone_number'],
                        role=row['role'],
                    )

                    created_users += 1

            with open(addresses_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if not row['email'].strip():
                        raise ValueError(f"Invalid address row: {row}")

                    user = User.objects.filter(email=row['email']).first()
                    if not user:
                        raise ValueError(f"User not found: {row}")

                    if not row['full_address'].strip():
                        raise ValueError(f"Empty address: {row}")

                    address, created = Address.objects.update_or_create(
                        user=user,
                        label=row['label'],
                        full_address=row['full_address'],
                        defaults={
                            'city': row['city'],
                            'pin_code': row['pin_code'],
                        }
                    )

                    if created and not Address.objects.filter(
                            user=user).exclude(id=address.id).exists():
                        address.is_default = True
                        address.save()

                    if created:
                        created_addresses += 1
                    else:
                        updated_addresses += 1

        print(f"""
Users -> Created: {created_users}, Skipped: {skipped_users}
Addresses -> Created: {created_addresses}, Updated: {updated_addresses}
""")

    except Exception as e:
        print(f"Error: {e}")
        print("Transaction rolled back!")
        raise
