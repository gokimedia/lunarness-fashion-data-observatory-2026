# Lunarness Fashion Data Transparency Standard v1.0

The Lunarness Fashion Data Transparency Standard (LFDTS) is a small, evidence-oriented disclosure standard for public pages that publish fashion statistics, comparisons or derived calculations. It is designed to make a claim traceable by a reader, journalist, researcher or machine without treating a badge as proof.

The standard is maintained by Lunarness. It is not a government accreditation, sustainability certification, product-safety approval or endorsement of an organization. Verification applies only to the URL and scope named in a registry record.

Canonical page: <https://lunarness.com/pages/fashion-data-transparency-standard>

## Mandatory criteria

A page must satisfy all eight criteria for the scope under review.

1. **Source identity (`S1`)**: Every material externally sourced statistic names its publisher and links to the supporting source page or stable record.
2. **Measurement context (`M1`)**: Each statistic preserves its unit, period, geography and reference population or denominator when one exists.
3. **Calculation provenance (`C1`)**: A value calculated by the publisher is labeled as derived and includes a reproducible formula or transformation note.
4. **Comparability warning (`C2`)**: Unlike metrics, time windows or populations are not merged into one ranking without an explicit comparability note.
5. **Machine-readable access (`A1`)**: The reviewed material is available as CSV, JSON or another documented structured format with stable field meanings.
6. **Version and canonical identity (`V1`)**: The page states a version and publication or update date, exposes a canonical URL and identifies the matching downloadable release.
7. **Corrections and contact (`G1`)**: A public correction route, issue tracker or contact address is provided. Material corrections must update the version history.
8. **Evidence integrity (`I1`)**: The registry record stores the reviewed URL, review date, expiry date and SHA-256 digest of the reviewed machine-readable artifact.

## Status model

- `verified`: An assessor other than the applicant reviewed all mandatory criteria. `independent_review` must be `true`.
- `self-assessed`: The publisher checked its own material. This is a disclosure, not independent verification.
- `expired`: The review period ended and has not been renewed.
- `revoked`: Evidence no longer satisfies the standard or the badge is being misrepresented.

Records expire no later than 12 months after issue. A material change to scope, measurement definitions or the machine-readable artifact requires a new review and digest.

## Verification workflow

1. Open a verification request using the repository issue form.
2. Provide the organization, domain, canonical evidence URL, machine-readable artifact URL, requested scope and a criterion-by-criterion self-assessment.
3. The reviewer checks the live page, follows source links, reproduces at least one derived value and calculates the artifact digest.
4. If every mandatory criterion passes, a registry record and status endpoint are added by pull request.
5. The badge may be embedded only after the registry pull request is merged. The badge must link to the canonical registry page or record.

Lunarness does not require a followed backlink for verification. Search-engine ranking, commercial payment, customer status or reciprocal promotion must not affect the review result.

## Registry record

Records conform to [`registry-entry.schema.json`](registry-entry.schema.json). The current index is [`registry.json`](registry.json). The founding Lunarness record is intentionally labeled `self-assessed` because the maintainer and applicant are the same organization.

## Badge endpoint

Each registry entry can have a small [Shields endpoint](https://shields.io/badges/endpoint-badge) JSON file in `badges/`. The image is generated from the public status file, so an expired or revoked record can change without asking every participant to replace its embed code.

Example for the founding self-assessment:

```html
<a href="https://lunarness.com/pages/fashion-data-transparency-standard#record-lfdts-2026-0001">
  <img
    src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fgokimedia%2Flunarness-fashion-data-observatory-2026%2Fmain%2Fstandard%2Fbadges%2Flunarness.com.json"
    alt="LFDTS v1.0 self-assessed"
  >
</a>
```

The linked registry record, not the SVG image, is the verification source. Copying the image or changing its text does not create a valid status.

## Governance and corrections

Propose a clarification through a GitHub issue. Changes that alter a requirement create a new standard version; editorial clarifications may update the documentation without changing the test itself. Registry corrections are preserved in Git history. False claims, broken evidence or undisclosed conflicts can trigger revocation.

LFDTS v1.0 is licensed under CC BY 4.0. Organizations may implement the criteria without displaying a badge.
