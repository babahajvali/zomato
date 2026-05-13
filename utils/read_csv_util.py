import csv


def read_csv(file_path):
    # TODO: loads the whole file into memory via list(...) — will OOM on large CSVs. Yield rows instead.
    with open(file_path, newline='', encoding='utf-8') as file:
        return list(csv.DictReader(file))


# TODO: What is row type?
def validate_row(row, required_fields, row_type="row"):
    for field in required_fields:
        # TODO: assumes every value is a str — if the column is missing entirely, row.get(field) is None and .strip() blows up.
        if not row.get(field) or not row[field].strip():
            raise ValueError(f"Invalid {row_type}: {row}")