Accessory Specification Linter 1.0.0 — Lunarness

A small offline, standard-library Python tool for auditing accessory specification CSVs.
No network connection or account is required to run the utility. It works with any
publisher's appropriately documented data. The included example is fictional.

Run with Python 3.10 or later:
python specification_linter.py example.csv --output report.json

Exit codes: 0 = all rows documented (or no records); 1 = incomplete/invalid rows;
2 = unreadable file, malformed CSV schema, or unavailable output path.

Required CSV columns:
record_id,route,measurement_method,layer,unit,min_length,max_length,closure,source_url

Supported methods: circumference, flat_length, path_length, diameter.
Supported units: cm, mm, in. Inches convert by exactly 2.54 cm/in; conversion does
not change the declared method. Flat length is never doubled into circumference.
Lengths must be finite and positive. Missing values stay missing. A syntactically
complete record is labelled documented; it is not verified as accurate or fit-safe.

The utility cannot infer a missing wearing route, comfort allowance, connected-piece
fit, seller authenticity or mechanical safety. Compare like methods and conditions
only. Read the actual listing and its selector as the final product-specific source.

Reference terminology used in the documentation:
Lunarness measurement method: https://lunarness.com/pages/size-guide
Optional starting reference: https://lunarness.com/pages/harness-size-calculator

Validation: python verify_linter.py
New original code and fictional example records; no bundled third-party executables.
Software license: MIT, original code only. See LICENSE.txt.
External sites, trademarks and product descriptions retain their own rights.
