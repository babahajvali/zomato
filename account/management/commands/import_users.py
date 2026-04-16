import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from account.models import User, Address


class Command(BaseCommand):
    help = "Populate users and addresses from CSV (with rollback)"

    def handle(self, *args, **kwargs):

        try:
            with transaction.atomic():  # 🔥 ensures full rollback

                # ---- Load Users ----
                with open('./sample_data/users.csv', newline='') as file:
                    reader = csv.DictReader(file)

                    for row in reader:
                        user, created = User.objects.get_or_create(
                            user_id=row['user_id'],
                            defaults={
                                'name': row['name'],
                                'email': row['email'],
                                'phone_number': row['phone_number'],
                                'role': row['role'],
                            }
                        )

                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(f"User created: {user.name}")
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f"User exists: {user.name}")
                            )

                # ---- Load Addresses ----
                with open('./sample_data/addresses.csv', newline='') as file:
                    reader = csv.DictReader(file)

                    for row in reader:
                        user = User.objects.get(user_id=row['user_id'])

                        # Prevent duplicate addresses
                        address, created = Address.objects.get_or_create(
                            user=user,
                            label=row['label'],
                            full_address=row['full_address'],
                            defaults={
                                'city': row['city'],
                                'pin_code': row['pin_code'],
                                'is_default': row['is_default'] == 'True'
                            }
                        )

                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(f"Address added for {user.name}")
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f"Address already exists for {user.name}")
                            )

                self.stdout.write(self.style.SUCCESS("✅ Data population completed!"))

        except Exception as e:
            # 🔥 ANY error → FULL rollback
            self.stdout.write(self.style.ERROR(f"❌ Error: {str(e)}"))
            self.stdout.write(self.style.WARNING("⚠️ All changes rolled back!"))