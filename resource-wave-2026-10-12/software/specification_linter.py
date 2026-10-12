#!/usr/bin/env python3
"""Offline accessory-specification CSV audit. Python standard library only."""
import argparse
import csv
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlparse

VERSION = '1.0.0'
FIELDS = ('record_id', 'route', 'measurement_method', 'layer', 'unit',
          'min_length', 'max_length', 'closure', 'source_url')
METHODS = {'circumference', 'flat_length', 'path_length', 'diameter'}
UNIT_TO_CM = {'cm': Decimal('1'), 'mm': Decimal('0.1'), 'in': Decimal('2.54')}
MISSING = {'', '?', 'unknown', 'not reported', 'not_reported', 'null'}

def number(text):
    if str(text).strip().lower() in MISSING:
        return None
    try:
        value = Decimal(str(text).strip())
        if not value.is_finite() or value <= 0:
            raise ValueError('length must be finite and positive')
        return value
    except (InvalidOperation, ValueError) as exc:
        raise ValueError('length must be finite and positive') from exc

def audit(rows):
    records, ids = [], set()
    for index, raw in enumerate(rows, 1):
        row = {key: str(raw.get(key) or '').strip() for key in FIELDS}
        errors, missing = [], []
        record_id = row['record_id'] or f'row-{index}'
        if not row['record_id']:
            missing.append('record_id')
        elif row['record_id'] in ids:
            errors.append('duplicate_record_id')
        ids.add(row['record_id'])
        for field in ('route', 'layer', 'closure', 'source_url'):
            if row[field].lower() in MISSING:
                missing.append(field)
        method = row['measurement_method'].lower()
        unit = row['unit'].lower()
        if method in MISSING:
            missing.append('measurement_method')
        elif method not in METHODS:
            errors.append('unsupported_measurement_method')
        if unit in MISSING:
            missing.append('unit')
        elif unit not in UNIT_TO_CM:
            errors.append('unsupported_unit')
        if 'source_url' not in missing:
            source = urlparse(row['source_url'])
            if source.scheme not in ('http', 'https') or not source.netloc:
                errors.append('source_url_not_absolute_http')
        bounds = {}
        for field in ('min_length', 'max_length'):
            try:
                bounds[field] = number(row[field])
                if bounds[field] is None:
                    missing.append(field)
            except ValueError:
                bounds[field] = None
                errors.append(f'invalid_{field}')
        minimum, maximum = bounds['min_length'], bounds['max_length']
        if minimum is not None and maximum is not None and minimum > maximum:
            errors.append('reversed_range')
        normalized = None
        if unit in UNIT_TO_CM and minimum is not None and maximum is not None and minimum <= maximum:
            normalized = {'min_cm': str(minimum * UNIT_TO_CM[unit]),
                          'max_cm': str(maximum * UNIT_TO_CM[unit]),
                          'measurement_method': method}
        records.append({'row': index, 'record_id': record_id,
                        'status': 'invalid' if errors else 'incomplete' if missing else 'documented',
                        'missing_fields': missing, 'errors': errors,
                        'normalized_range': normalized})
    return {'tool': 'Accessory Specification Linter', 'version': VERSION,
            'record_count': len(records),
            'counts': {s: sum(r['status'] == s for r in records)
                       for s in ('documented', 'incomplete', 'invalid')},
            'meaning': 'Documented means the required fields are present and syntactically valid. '
                       'It does not verify source accuracy, product safety, comfort or fit. '
                       'Unit conversion preserves the declared measurement method; '
                       'flat length is never doubled into circumference.',
            'records': records}

def read_csv(path):
    with Path(path).open(newline='', encoding='utf-8-sig') as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
        if len(headers) != len(set(headers)):
            raise ValueError('duplicate CSV headers')
        absent = [name for name in FIELDS if name not in headers]
        if absent:
            raise ValueError('missing CSV columns: ' + ', '.join(absent))
        rows = list(reader)
        if any(None in row for row in rows):
            raise ValueError('a CSV row contains more cells than the header')
        return rows

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_file', help='UTF-8 accessory specification CSV')
    parser.add_argument('--output', help='Write JSON report to a local file')
    parser.add_argument('--version', action='version', version=VERSION)
    options = parser.parse_args(argv)
    try:
        report = audit(read_csv(options.csv_file))
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        print(f'Cannot audit input: {exc}', file=sys.stderr)
        return 2
    result = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if options.output:
        try:
            Path(options.output).write_text(result, encoding='utf-8')
        except OSError as exc:
            print(f'Cannot write report: {exc}', file=sys.stderr)
            return 2
    else:
        print(result, end='')
    return 1 if report['counts']['invalid'] or report['counts']['incomplete'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
