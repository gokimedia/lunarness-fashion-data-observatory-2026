Lunarness public catalog: literal measurement-disclosure signals
Snapshot label: 12 October 2026 (Europe/Istanbul)

Research question: Which literal measurement, route, closure and material signals
occur in the public catalog's product-description metadata at the capture time?

Population: all 162 product records returned by Lunarness's public products.json
endpoint during this capture. Limit 250; a second page returned zero records.
This is an endpoint snapshot, not a claim to include the entire business inventory,
every product page's theme content, or the wider accessory market.

Method: a deterministic standard-library Python parser strips HTML, excludes script
and style text, and applies the published regex rules only to body_html. Exact Size
option-name presence is observed separately. No photographs, customer measurements,
ratings, private inventory, sales or checkout information are included. CSV, JSON,
SQL, codebook and executable extraction/test source are supplied.

Interpretation: numeric_unit_pair is a text indicator; it may describe width or other
dimensions. numeric_range_with_unit is a literal range expression; it is not verified
as a wearable adjustment range. Route, closure and material tokens may appear in a
style description, so their presence does not establish completeness or authenticity.
No physical dimensions are invented or imputed. Missing indicators remain zero.
No product-quality ranking, fit recommendation, safety or comfort score is produced.

Reproducibility: capture-method-and-results.json stores capture timestamp, source URLs,
HTTP receipt statuses and SHA-256 digests. The full description payload is not part of
the published files. Running build_catalog_signals.py later fetches current public
data and may produce a different snapshot. verify_signal_rules.py passed 16 meaningful
fixtures; the generated SQL was loaded into SQLite and its row count/flags checked.

Affiliation and limitations: Lunarness operates the sampled store. This self-catalog
audit is not independent of the store and is not a representative industry study.
The implementation and writing were prepared with AI assistance; observations derive
from actual public JSON and deterministic rules. No claim of independent human coding
or manual product-measurement verification is made. Results should be interpreted as
literal automated indicators, with the exposed rules and limitations.

Terminology context and related source references:
https://lunarness.com/pages/size-guide
https://lunarness.com/pages/harness-size-calculator
These are optional context references; they are not part of the data extraction and
do not establish a particular product's fit. The original capture method is documented
in this README, codebook.json and executable source.

License for original sparse dataset/codebook/documentation: CC BY 4.0.
License for original extraction/test software: MIT.
See LICENSE-DATA.txt and LICENSE-CODE.txt for scope and attribution.
Linked websites, store trademarks and source product descriptions retain their own
rights. The dataset does not license or redistribute product images/descriptions.
No institutional, Harvard or platform endorsement is claimed.
