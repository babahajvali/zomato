import csv


def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as file:
        return list(csv.DictReader(file))

def validate_row(row, required_fields, row_type="row"):
    for field in required_fields:
        if not row.get(field) or not row[field].strip():
            raise ValueError(f"Invalid {row_type}: {row}")