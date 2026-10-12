"""Reproducible literal disclosure-signal snapshot of Lunarness public catalog.

Only public storefront data. No customer data, images or invented measurements.
The full source payload stays local; publication files contain sparse facts only.
"""
import csv
import hashlib
import html
import json
import re
import sqlite3
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LABEL_DATE = '2026-10-12'
BASE = 'https://lunarness.com/products.json?limit=250'
NUM = r'\d+(?:[.,]\d+)?'
UNIT = r'(?:centimeters?|millimeters?|inches|inch|cm|mm|in)'
PAIR = re.compile(r'(?<![\w.])' + NUM + r'\s*(' + UNIT + r')(?![\w])', re.I)
RANGE = re.compile(r'(?<![\w.])' + NUM + r'\s*(?:-|–|—|\bto\b)\s*' + NUM + r'\s*' + UNIT + r'(?![\w])', re.I)
ROUTE = re.compile(r'\b(?:chest|bust|waist|neck|wrist|thigh|hips?|ankles?|shoulder|torso)\b', re.I)
CLOSURE = re.compile(r'\b(?:buckles?|clasps?|snaps?|ties?|hooks?|lace-up|lacing|velcro|fasteners?)\b', re.I)
MATERIAL = re.compile(r'\b(?:leather|polyurethane|pu|pvc|metal|steel|alloy|silver|gold|fabric|lace|nylon|elastic|mesh|chainmail)\b', re.I)

class TextOnly(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.hidden = [], 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        if tag in ('p', 'li', 'br', 'div', 'tr'):
            self.parts.append(' ')
    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.hidden:
            self.hidden -= 1
        if tag in ('p', 'li', 'div', 'tr'):
            self.parts.append(' ')
    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)

def text_only(value):
    parser = TextOnly(); parser.feed(value or '')
    return ' '.join(''.join(parser.parts).split())

def signals(body_html, option_names):
    text = text_only(body_html)
    units = sorted({m.group(1).lower() for m in PAIR.finditer(text)})
    return {
        'numeric_unit_pair': int(bool(units)),
        'numeric_range_with_unit': int(bool(RANGE.search(text))),
        'route_token': int(bool(ROUTE.search(text))),
        'closure_token': int(bool(CLOSURE.search(text))),
        'material_token': int(bool(MATERIAL.search(text))),
        'size_option_name': int(any(name.casefold().strip() == 'size' for name in option_names)),
        'unit_tokens_detected': ';'.join(units)
    }

def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'LunarnessCatalogDisclosureAudit/1.0'})
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read()
        return json.loads(raw), {'url': url, 'status': response.status,
            'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def sql_literal(value):
    if isinstance(value, int): return str(value)
    return "'" + str(value).replace("'", "''") + "'"

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    captured = datetime.now(timezone.utc).isoformat()
    first, first_receipt = fetch(BASE)
    second, second_receipt = fetch(BASE + '&page=2')
    products = first.get('products', [])
    second_products = second.get('products', [])
    if second_products:
        raise RuntimeError('Second page was not empty; review pagination before labelling export complete.')
    if len({p['id'] for p in products}) != len(products):
        raise RuntimeError('Duplicate product IDs in snapshot')
    rows = []
    for product in sorted(products, key=lambda p:p['handle']):
        names = [str(option.get('name', '')) for option in product.get('options', [])]
        fields = signals(product.get('body_html', ''), names)
        rows.append({'product_id':str(product['id']), 'handle':product['handle'],
            'product_type':product.get('product_type') or 'Not reported',
            'source_url':'https://lunarness.com/products/' + product['handle'],
            'captured_at_utc':captured, 'option_names':';'.join(names),
            'variant_count':len(product.get('variants', [])), **fields})
    with (ROOT/'catalog-disclosure-signals.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (ROOT/'catalog-disclosure-signals.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # Sparse source facts only; full description HTML is deliberately not included.
    marker_fields = ('numeric_unit_pair','numeric_range_with_unit','route_token','closure_token','material_token','size_option_name')
    summary={'label_date_istanbul':LABEL_DATE,'captured_at_utc':captured,'records':len(rows),
        'counts':{name:sum(row[name] for row in rows) for name in marker_fields},
        'population':'All records returned by the public products.json endpoint in this capture; page 2 returned zero. Not a complete store inventory claim.',
        'method':'Deterministic regex indicators applied only to body_html, plus exact Size option-name presence. Theme content, reviews, linked size-guide text and images excluded.',
        'meaning':'Indicators record literal disclosure signals. They do not establish product dimensions, adjustment bounds, completeness, safety, customer fit, material authenticity or comparative quality.',
        'researcher_affiliation':'Lunarness, the same organization as the sampled store. This self-catalog snapshot is not a representative market study.',
        'source_receipts':[first_receipt,second_receipt], 'customer_or_human_measurements':False,
        'raw_description_and_images_published':False,
        'reproduce_command':'python build_catalog_signals.py; this fetches current data, so later snapshots may differ.'}
    (ROOT/'capture-method-and-results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    columns=list(rows[0]); ints={'variant_count',*marker_fields}
    create='CREATE TABLE catalog_signals ('+', '.join('`'+key+'` '+('INT' if key in ints else 'VARCHAR(32)' if key=='product_id' else 'VARCHAR(2048)')+(' PRIMARY KEY' if key=='product_id' else '') for key in columns)+');\n'
    inserts='INSERT INTO catalog_signals VALUES\n'+',\n'.join('('+', '.join(sql_literal(row[key]) for key in columns)+')' for row in rows)+';\n'
    (ROOT/'catalog-signals.sql').write_text(create+inserts,encoding='utf-8')
    connection=sqlite3.connect(':memory:');connection.executescript(create+inserts)
    assert connection.execute('SELECT COUNT(*) FROM catalog_signals').fetchone()[0]==len(rows)
    assert connection.execute('SELECT COUNT(*) FROM catalog_signals WHERE numeric_unit_pair NOT IN (0,1)').fetchone()[0]==0
    connection.close()
    print(json.dumps(summary,ensure_ascii=False))

if __name__ == '__main__': main()
