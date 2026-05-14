import csv
from typing import Dict, List, Any


def read_csv(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def validate_row(
    row: Dict[str, Any],
    required_fields: List[str],
    row_type: str = "row",
) -> None:
    for field in required_fields:
        value = row.get(field)

        if value is None:
            raise ValueError(f"Missing field '{field}' in {row_type}: {row}")

        if not str(value).strip():
            raise ValueError(f"Empty field '{field}' in {row_type}: {row}")
