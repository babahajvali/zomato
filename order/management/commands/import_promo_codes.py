import csv
from django.utils.dateparse import parse_datetime
from order.models import PromoCode


def import_promo_codes(file_path='./sample_data/promo_codes.csv'):
    created_count = updated_count = skipped_count = 0

    with open(file_path, newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if not row['code'].strip():
                skipped_count += 1
                continue

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
                created_count += 1
            else:
                updated_count += 1

    print(f"Done: Created {created_count}, Updated {updated_count}, Skipped {skipped_count}")