import csv
from django.core.management.base import BaseCommand
from restaurant.models import Restaurant


class Command(BaseCommand):
    help = 'Export restaurants to CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to output CSV file')
        parser.add_argument('--active-only', action='store_true', help='Export only active restaurants')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        active_only = options['active_only']
        
        try:
            queryset = Restaurant.objects.all()
            if active_only:
                queryset = queryset.filter(is_active=True)
            
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Write headers
                headers = [
                    'id', 'name', 'description', 'owner_email', 'owner_name', 
                    'cuisine_type', 'address', 'pin_code', 'is_veg_only', 
                    'is_active', 'created_at', 'updated_at'
                ]
                writer.writerow(headers)
                
                # Write data
                for restaurant in queryset:
                    row = [
                        restaurant.id,
                        restaurant.name,
                        restaurant.description,
                        restaurant.owner.email,
                        restaurant.owner.name,
                        restaurant.cuisine_type,
                        restaurant.address,
                        restaurant.pin_code,
                        restaurant.is_veg_only,
                        restaurant.is_active,
                        restaurant.created_at.isoformat() if restaurant.created_at else '',
                        restaurant.updated_at.isoformat() if restaurant.updated_at else ''
                    ]
                    writer.writerow(row)
                
                count = queryset.count()
                self.stdout.write(self.style.SUCCESS(f'Exported {count} restaurants to {csv_file_path}'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error exporting restaurants: {str(e)}'))
