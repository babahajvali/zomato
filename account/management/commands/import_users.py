import csv

from django.db import transaction

from account.models import User, Address


def import_users_and_addresses(
        users_file='./sample_data/users.csv',
        addresses_file='./sample_data/addresses.csv'
):
    created_users = updated_users = skipped_users = 0
    created_addresses = updated_addresses = skipped_addresses = 0

    try:
        with transaction.atomic():

            with open(users_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if not row['user_id'].strip():
                        skipped_users += 1
                        continue

                    user, created = User.objects.update_or_create(
                        user_id=row['user_id'],
                        defaults={
                            'name': row['name'],
                            'email': row['email'],
                            'phone_number': row['phone_number'],
                            'role': row['role'],
                        }
                    )

                    if created:
                        created_users += 1
                    else:
                        updated_users += 1

            with open(addresses_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if not row['user_id'].strip():
                        skipped_addresses += 1
                        continue

                    user = User.objects.filter(user_id=row['user_id']).first()
                    if not user:
                        skipped_addresses += 1
                        continue

                    address, created = Address.objects.update_or_create(
                        user=user,
                        label=row['label'],
                        full_address=row['full_address'],
                        defaults={
                            'city': row['city'],
                            'pin_code': row['pin_code'],
                            'is_default': str(row['is_default']).lower() == 'true'
                        }
                    )

                    if created:
                        created_addresses += 1
                    else:
                        updated_addresses += 1

        print(
            f"""
    Users -> Created: {created_users}, Updated: {updated_users}, Skipped: {skipped_users}
    Addresses -> Created: {created_addresses}, Updated: {updated_addresses}, Skipped: {skipped_addresses}
    """)
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Transaction rolled back!")
