import csv
from io import StringIO
from django.http import HttpResponse
from typing import List, Dict, Any


def generate_csv_response(data: List[Dict[str, Any]], filename: str) -> HttpResponse:
    """
    Generate CSV response from list of dictionaries
    """
    if not data:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    fieldnames = data[0].keys()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    
    return response


def parse_csv_file(csv_file) -> List[Dict[str, str]]:
    """
    Parse uploaded CSV file and return list of dictionaries
    """
    csv_file.seek(0)
    reader = csv.DictReader(StringIO(csv_file.read().decode('utf-8')))
    return list(reader)


def validate_csv_headers(headers: List[str], required_headers: List[str]) -> bool:
    """
    Validate CSV headers against required headers
    """
    return all(header in headers for header in required_headers)


def create_sample_csv_file(model_type: str) -> HttpResponse:
    """
    Create sample CSV file for different model types
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="sample_{model_type}.csv"'
    
    writer = csv.writer(response)
    
    if model_type == 'restaurant':
        writer.writerow([
            'name', 'description', 'owner_email', 'owner_name', 'owner_phone',
            'cuisine_type', 'address', 'pin_code', 'is_veg_only', 'is_active'
        ])
        writer.writerow([
            'Test Restaurant', 'A great place to eat', 'owner@example.com', 'John Doe', '1234567890',
            'SOUTH_INDIAN', '123 Main St, Bangalore', '560001', 'false', 'true'
        ])
    
    elif model_type == 'user':
        writer.writerow([
            'name', 'email', 'phone_number', 'role', 'address_label', 
            'full_address', 'city', 'address_pin_code', 'is_default_address'
        ])
        writer.writerow([
            'John Doe', 'john@example.com', '1234567890', 'CUSTOMER', 'Home',
            '123 Main St, Bangalore', 'Bangalore', '560001', 'true'
        ])
    
    elif model_type == 'promo_code':
        writer.writerow([
            'code', 'discount_type', 'discount_value', 'min_order_value', 
            'max_usage', 'valid_from', 'valid_until'
        ])
        writer.writerow([
            'SAVE10', 'PERCENTAGE', '10.00', '100.00', '100', 
            '2024-01-01 00:00:00', '2024-12-31 23:59:59'
        ])
    
    return response


def bulk_create_from_csv(model_class, csv_data: List[Dict[str, str]], 
                        field_mapping: Dict[str, str], 
                        processors: Dict[str, callable] = None) -> int:
    """
    Bulk create model instances from CSV data
    """
    instances = []
    
    for row in csv_data:
        instance_data = {}
        
        for csv_field, model_field in field_mapping.items():
            value = row.get(csv_field)
            
            if processors and csv_field in processors:
                value = processors[csv_field](value)
            
            instance_data[model_field] = value
        
        instances.append(model_class(**instance_data))
    
    model_class.objects.bulk_create(instances)
    return len(instances)
