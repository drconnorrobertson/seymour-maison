"""Illustrative rectangular-sample arithmetic, not a standardized textile test."""
import csv
from decimal import Decimal, InvalidOperation
import json
import sys


def calculate(rows):
    output = []
    seen = set()
    for row in rows:
        name = row['sample'].strip()
        if not name or name in seen:
            raise ValueError('Sample identifiers must be present and unique')
        seen.add(name)
        values = []
        for field in ['length_cm', 'width_cm', 'mass_g']:
            try:
                value = Decimal(row[field])
            except (InvalidOperation, TypeError):
                raise ValueError('Invalid numeric field: ' + field)
            if not value.is_finite() or value <= 0:
                raise ValueError('Expected a finite positive value: ' + field)
            values.append(value)
        length, width, mass = values
        area = length * width / Decimal(10000)
        output.append({'sample': name, 'area_m2': format(area.normalize(), 'f'),
                       'calculated_gsm': format((mass / area).normalize(), 'f')})
    if not output:
        raise ValueError('No sample rows')
    return output


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 fabric_gsm.py fictional-samples.csv')
    with open(sys.argv[1], newline='', encoding='utf-8') as source:
        result = calculate(csv.DictReader(source))
    print(json.dumps(result, indent=2))
