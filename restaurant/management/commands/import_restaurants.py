import csv
from django.db import transaction
from account.models import User
from restaurant.models import Restaurant


def import_restaurants(file_path='./sample_data/restaurants.csv'):
    created_count = updated_count = skipped_count = 0

    try:
        with transaction.atomic():

            with open(file_path, newline='') as file:
                reader = csv.DictReader(file)

                for row in reader:

                    if not row['name'].strip():
                        skipped_count += 1
                        continue

                    try:
                        owner = User.objects.get(
                            email=row['owner_email'],
                            role='OWNER'
                        )
                    except User.DoesNotExist:
                        skipped_count += 1
                        print(
                            f"Skipped (owner not found): {row['owner_email']}")
                        continue

                    restaurant, created = Restaurant.objects.update_or_create(
                        name=row['name'],
                        owner=owner,
                        defaults={
                            'description': row['description'],
                            'cuisine_type': row['cuisine_type'],
                            'address': row['address'],
                            'pin_code': row['pin_code'],
                            'is_veg_only': row['is_veg_only'] == 'True',
                            'is_active': row['is_active'] == 'True',
                        }
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

        print(
            f"Done: Created {created_count}, Updated {updated_count}, Skipped {skipped_count}")

    except Exception as e:
        print(f"Error: {str(e)}")
        print("Transaction rolled back!")
