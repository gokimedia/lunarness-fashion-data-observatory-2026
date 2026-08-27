---
license: other
license_name: cc-by-4.0-derived-analysis
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
    doi = {10.5281/zenodo.22131190},
    url = {https://lunarness.com/pages/fashion-statistics-observatory}
  }
---

# Lunarness Fashion Data Observatory 2026

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22131190.svg)](https://doi.org/10.5281/zenodo.22131190)

This package is the machine-readable companion to the [Lunarness Fashion Data Observatory 2026](https://lunarness.com/pages/fashion-statistics-observatory). It combines a small set of cited public findings about Fashion Week media attention, historical event attendance, online fashion behavior and textile circularity with clearly labeled arithmetic derivations.

The Lunarness page is the canonical editorial presentation. The same versioned package is distributed through the following research and data platforms, with one shared Zenodo DOI:

- [Zenodo record](https://zenodo.org/records/22131190)
- [GitHub repository](https://github.com/gokimedia/lunarness-fashion-data-observatory-2026)
- [Hugging Face dataset](https://huggingface.co/datasets/FoodSecuriry/lunarness-fashion-data-observatory-2026)
- [Kaggle dataset](https://www.kaggle.com/datasets/morrispoint/lunarness-fashion-data-observatory-2026)

## Audio companion

The [Lunarness Fashion Data Briefing](https://rss.com/podcasts/lunarness-fashion-data-briefing/) is the official audio companion to this release. Its source-led episodes explain selected Observatory findings without replacing the dataset, source ledger or DOI record.

- [Official podcast page](https://rss.com/podcasts/lunarness-fashion-data-briefing/)
- [Open podcast RSS feed](https://media.rss.com/lunarness-fashion-data-briefing/feed.xml)
- [Apple Podcasts listing](https://podcasts.apple.com/us/podcast/lunarness-fashion-data-briefing/id6805995146)

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

> Lunarness Editorial Team (2026). *Lunarness Fashion Data Observatory 2026* (Version 1.0). https://doi.org/10.5281/zenodo.22131190

The Zenodo DOI above is the primary archived citation. Distribution copies should retain the same DOI and canonical Lunarness URL instead of minting unrelated identifiers for identical content.

## Licensing

Lunarness's original prose, calculations and dataset structure are available under CC BY 4.0. Third-party facts, names and source materials remain subject to their respective source terms. Reusers should cite the canonical Lunarness page and the underlying source for each metric.
