import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.dateparse import parse_datetime
from order.models import PromoCode


class Command(BaseCommand):
    help = "Import PromoCodes from CSV"

    def handle(self, *args, **kwargs):

        try:
            with transaction.atomic():  # 🔥 rollback support

                with open('./sample_data/promo_codes.csv', newline='') as file:
                    reader = csv.DictReader(file)

                    for row in reader:

                        promocode, created = PromoCode.objects.update_or_create(
                            code=row['code'],
                            defaults={
                                'discount_type': row['discount_type'],
                                'discount_value': row['discount_value'],
                                'min_order_value': row['min_order_value'],
                                'max_usage': row['max_usage'],
                                'valid_from': parse_datetime(row['valid_from']),
                                'valid_until': parse_datetime(row['valid_until']),
                            }
                        )

                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(f"Created: {promocode.code}")
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f"Updated: {promocode.code}")
                            )

                self.stdout.write(self.style.SUCCESS("✅ PromoCodes imported successfully"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {str(e)}"))
            self.stdout.write(self.style.WARNING("⚠️ Transaction rolled back!"))