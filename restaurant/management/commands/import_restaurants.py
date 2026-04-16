import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from account.models import User
from restaurant.models import Restaurant


class Command(BaseCommand):
    help = "Import Restaurants from CSV"

    def handle(self, *args, **kwargs):

        try:
            with transaction.atomic():  # 🔥 rollback support

                with open('./sample_data/restaurants.csv', newline='') as file:
                    reader = csv.DictReader(file)

                    for row in reader:

                        # 🔥 Get owner using email
                        try:
                            owner = User.objects.get(email=row['owner_email'], role='OWNER')
                        except User.DoesNotExist:
                            raise Exception(f"Owner not found: {row['owner_email']}")

                        # ✅ Create or update restaurant
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
                            self.stdout.write(
                                self.style.SUCCESS(f"Created: {restaurant.name}")
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f"Updated: {restaurant.name}")
                            )

                self.stdout.write(self.style.SUCCESS("✅ Restaurants imported successfully"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {str(e)}"))
            self.stdout.write(self.style.WARNING("⚠️ Transaction rolled back!"))