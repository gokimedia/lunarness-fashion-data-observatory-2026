import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from specification_linter import audit, FIELDS

BASE = {'record_id':'a', 'route':'paper loop', 'measurement_method':'circumference',
        'layer':'paper', 'unit':'in', 'min_length':'12', 'max_length':'14',
        'closure':'overlap', 'source_url':'https://example.com/method'}

def check(row, status, flag=None):
    result = audit([row])['records'][0]
    assert result['status'] == status, result
    if flag:
        assert flag in result['errors'] + result['missing_fields'], result
    return result

assert check(BASE, 'documented')['normalized_range']['min_cm'] == '30.48'
flat = check({**BASE, 'measurement_method':'flat_length'}, 'documented')
assert flat['normalized_range']['min_cm'] == '30.48'
assert flat['normalized_range']['measurement_method'] == 'flat_length'
check({**BASE, 'layer':'unknown'}, 'incomplete', 'layer')
check({**BASE, 'unit':'ft'}, 'invalid', 'unsupported_unit')
check({**BASE, 'min_length':'15'}, 'invalid', 'reversed_range')
check({**BASE, 'min_length':'NaN'}, 'invalid', 'invalid_min_length')
check({**BASE, 'max_length':'Infinity'}, 'invalid', 'invalid_max_length')
check({**BASE, 'min_length':'0'}, 'invalid', 'invalid_min_length')
check({**BASE, 'source_url':'javascript:alert(1)'}, 'invalid', 'source_url_not_absolute_http')
check({**BASE, 'measurement_method':'guess'}, 'invalid', 'unsupported_measurement_method')
duplicate = audit([BASE, BASE])
assert duplicate['records'][1]['errors'] == ['duplicate_record_id']
mixed = audit([BASE, {**BASE, 'record_id':'b', 'unit':'cm', 'min_length':'30.48', 'max_length':'35.56'}])
assert mixed['counts']['documented'] == 2
assert mixed['records'][0]['normalized_range'] == mixed['records'][1]['normalized_range']
script = Path(__file__).with_name('specification_linter.py')
with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / 'bom.csv'
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader(); writer.writerow(BASE)
    valid = subprocess.run([sys.executable, str(script), str(path)], capture_output=True, text=True)
    assert valid.returncode == 0, valid.stderr
    assert json.loads(valid.stdout)['counts']['documented'] == 1
    path.write_text('record_id,record_id\na,a\n', encoding='utf-8')
    bad = subprocess.run([sys.executable, str(script), str(path)], capture_output=True, text=True)
    assert bad.returncode == 2 and 'duplicate CSV headers' in bad.stderr
    path.write_text(','.join(FIELDS) + '\n' + ','.join(BASE.values()) + ',extra\n', encoding='utf-8')
    extra = subprocess.run([sys.executable, str(script), str(path)], capture_output=True, text=True)
    assert extra.returncode == 2 and 'more cells' in extra.stderr
    path.write_text(','.join(FIELDS) + '\n', encoding='utf-8')
    empty = subprocess.run([sys.executable, str(script), str(path)], capture_output=True, text=True)
    assert empty.returncode == 0 and json.loads(empty.stdout)['record_count'] == 0
print(json.dumps({'meaningful_scenarios_passed': 16, 'scope':'unit conversion without method change, missing/invalid input, duplicate identity, CSV schema, UTF-8 BOM and CLI exits'}))
