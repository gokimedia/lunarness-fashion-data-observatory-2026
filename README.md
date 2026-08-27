---
license: other
license_name: CC-BY-4.0-derived-analysis
license_link: https://creativecommons.org/licenses/by/4.0/
language:
  - en
pretty_name: Lunarness Fashion Data Observatory 2026
homepage: https://lunarness.com/pages/fashion-statistics-observatory
size_categories:
  - n<1K
tags:
  - fashion
  - fashion-week
  - ecommerce
  - media-impact
  - sustainability
  - circularity
  - tabular
configs:
  - config_name: default
    data_files:
      - split: train
        path: data/fashion_observatory_2026.csv
citation: |
  @dataset{lunarness_fashion_observatory_2026,
    author = {{Lunarness Editorial Team}},
    title = {Lunarness Fashion Data Observatory 2026},
    year = {2026},
    version = {1.0},
    url = {https://lunarness.com/pages/fashion-statistics-observatory}
  }
---

# Lunarness Fashion Data Observatory 2026

This package is the machine-readable companion to the [Lunarness Fashion Data Observatory 2026](https://lunarness.com/pages/fashion-statistics-observatory). It combines a small set of cited public findings about Fashion Week media attention, historical event attendance, online fashion behavior and textile circularity with clearly labeled arithmetic derivations.

The package is designed for publication on Hugging Face Datasets, GitHub and a DOI-issuing research repository such as Zenodo. The Lunarness page is the canonical editorial presentation; repository copies should link back to it using the URL above.

## Files

- `data/fashion_observatory_2026.csv`: flat, row-level release with source and comparability fields.
- `data/fashion_observatory_2026.json`: compact JSON release used by the web page.
- `data_dictionary.md`: field meanings and interpretation rules.
- `croissant.json`: MLCommons Croissant-style dataset metadata for machine discovery.
- `CITATION.cff`: citation metadata for GitHub and scholarly tools.
- `.zenodo.json`: suggested metadata for a Zenodo deposit or GitHub release integration.
- `LICENSE.md`: scope of the CC BY 4.0 grant and third-party source notice.

## Intended uses

- Referencing individual fashion-market indicators with their units, periods and caveats intact.
- Reproducing the simple sums, shares, ratios and percentage-point differences shown on the canonical page.
- Testing citation-aware retrieval, question answering and data-to-text workflows.
- Teaching why metrics such as MIV, website visits, purchases, consumption and waste cannot be collapsed into a single score.

## Out-of-scope uses

- Presenting the historical attendance figures as a current worldwide ranking.
- Treating Media Impact Value as revenue, sales, profit, reach or audited advertising spend.
- Training a model to make environmental claims about individual products.
- Redistributing source downloads or implying that Lunarness owns third-party databases.

## Method

1. Use sources with a named publisher, period, geography and measurement description.
2. Record reported values without inventing missing observations.
3. Limit derivations to transparent arithmetic and show the formula in the `derivation` field.
4. Keep a `comparability_note` next to values that are easy to overstate.
5. Link every row to the source page that supports it.

## Citation

Preferred short citation:

> Lunarness Editorial Team (2026). *Lunarness Fashion Data Observatory 2026* (Version 1.0). https://lunarness.com/pages/fashion-statistics-observatory

After a DOI has been minted, add the DOI to `CITATION.cff`, `.zenodo.json`, the canonical web page and every distribution copy. Use one DOI-backed release as the citation authority instead of minting unrelated DOIs for identical copies.

## Licensing

Lunarness's original prose, calculations and dataset structure are available under CC BY 4.0. Third-party facts, names and source materials remain subject to their respective source terms. Reusers should cite the canonical Lunarness page and the underlying source for each metric.
