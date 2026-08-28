# Distribution and citation plan

The goal is not to manufacture backlinks. It is to make one useful, versioned research asset easy to discover, verify and cite across scholarly, developer and AI ecosystems.

## Release rule

Publish version 1.0 first in one DOI-issuing repository, preferably Zenodo. Treat that DOI as the citation authority. Every mirror should include the same title, version, canonical Lunarness URL and primary DOI. Do not mint unrelated DOIs for byte-identical copies.

Before publishing, replace the editorial-team author with the legal person or organization that should own the scholarly record. After publication, add the DOI to `CITATION.cff`, `.zenodo.json`, this README, the canonical web page and every mirror.

## Recommended sequence

| Priority | Destination | Main benefit | Release action |
| --- | --- | --- | --- |
| 1 | Zenodo | Versioned DataCite DOI, durable citation page and downloadable archive | Reserve a DOI, upload the complete package, publish version 1.0 and record the DOI everywhere. |
| 2 | GitHub | Transparent revision history, `CITATION.cff` support and a natural source for later Zenodo releases | Create a public repository or tagged release; link the canonical page and primary DOI. |
| 3 | Hugging Face Datasets | Discovery by data practitioners and AI tooling through the dataset card, CSV/JSON files and metadata | Upload this directory as a dataset repository; keep the YAML front matter and Croissant metadata intact. |
| 4 | Figshare | Searchable research-object page and DataCite DOI support | Use as an institutional or audience-specific mirror; point its related identifier to the primary DOI instead of creating a competing citation target when possible. |
| 5 | OSF | Transparent project history and frozen registrations | Use an OSF project for working notes or a registration for a fixed methodology; link the primary DOI and canonical page. |
| 6 | Mendeley Data or Dataverse | Additional scholarly discovery and repository-specific audiences | Choose one only when it reaches a distinct audience or satisfies an institutional requirement; relate it to the primary DOI. |
| 7 | Kaggle | Community notebooks and exploratory reuse | Publish only if accompanied by a useful notebook or analysis; cite the primary DOI and source ledger. |

## Podcast and RSS companion

The official audio companion is [Lunarness Fashion Data Briefing](https://rss.com/podcasts/lunarness-fashion-data-briefing/). Its canonical distribution feed is [the open RSS feed](https://media.rss.com/lunarness-fashion-data-briefing/feed.xml).

Every public dataset mirror should include both links as supporting material. The podcast explains selected findings, while the DOI record and canonical Observatory page remain the citation authorities for data and methodology.

Verified directory records:

- [Spotify](https://open.spotify.com/show/6QwJGgZmdQUWCqck8ERs82)
- [Amazon Music](https://music.amazon.com/podcasts/f21efb1f-96cb-4cb2-8f46-c3734be17974/lunarness-fashion-data-briefing)
- [Apple Podcasts](https://podcasts.apple.com/us/podcast/lunarness-fashion-data-briefing/id6805995146)
- [Podcast Index](https://podcastindex.org/podcast/8007834)

## Quality requirements for every copy

- Preserve the `source_url`, `period`, `unit`, `derivation` and `comparability_note` fields.
- Link prominently to `https://lunarness.com/pages/fashion-statistics-observatory`.
- State that Media Impact Value is not revenue and that the historical attendance figures are not a current like-for-like ranking.
- Keep the third-party-data notice from `LICENSE.md`.
- Use the same version number and release date across repositories.
- Add an archive checksum when a platform supports it.
- Avoid profile farms, paid link networks, automated forum posting and thin duplicate articles.

## AI and MCP discoverability

The live Shopify site already exposes product discovery and commerce operations through UCP/MCP. A separate MCP application is therefore not required for product lookup. If the research collection grows, a small read-only research MCP can add genuine value with tools such as `list_datasets`, `get_metric`, `get_source` and `download_release`. Its responses should return the canonical page, metric period, unit, caveat and DOI together.

For model discovery, keep the public HTML page, sitemap entry, Dataset/Article/FAQ structured data, downloadable CSV/JSON, dataset card and DOI landing page synchronized. These are complementary citation surfaces; none guarantees inclusion or citation by a model.

## Ongoing release cadence

Create a new version only when sources, observations or methodology change materially. Maintain a short changelog, preserve previous DOI versions and point the concept DOI to the latest release. A quarterly source review is sufficient unless an underlying publisher issues a major update sooner.
