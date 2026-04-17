import csv
from django.utils import timezone
from django.db import transaction
from django.utils.dateparse import parse_datetime
from order.models import PromoCode


def import_promo_codes(file_path='./sample_data/promo_codes.csv'):
    created_count = updated_count = skipped_count = 0

    try:
        with transaction.atomic():

            with open(file_path, newline='') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if not row['code'].strip():
                        raise ValueError(f"Invalid promo row: {row}")

                    valid_from = parse_datetime(row['valid_from'])
                    valid_until = parse_datetime(row['valid_until'])

                    if valid_from:
                        valid_from = timezone.make_aware(valid_from)

                    if valid_until:
                        valid_until = timezone.make_aware(valid_until)

                    promocode, created = PromoCode.objects.update_or_create(
                        code=row['code'],
                        defaults={
                            'discount_type': row['discount_type'],
                            'discount_value': row['discount_value'],
                            'min_order_value': row['min_order_value'],
                            'max_usage': row['max_usage'],
                            'valid_from': valid_from,
                            'valid_until': valid_until,
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
