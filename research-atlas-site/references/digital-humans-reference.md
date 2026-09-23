# Digital Humans research-site reference

## Recorded sources

- Live site: https://wojciechzielonka.com/how-to-build-digital-humans/
- Public repository: https://github.com/Zielon/how-to-build-digital-humans
- Survey paper: https://arxiv.org/abs/2607.04341
- Title: *How to Build Digital Humans? From Priors to Photorealistic Avatars*
- Venue: Eurographics 2026 State-of-the-Art Report
- Recorded as a reference on 2026-09-07.

Reinspect the current sources before relying on implementation details because the repository and site may change.

## Observed architecture

The project is a mostly static academic website rather than a server-backed application:

```text
BibTeX + CSV + ordering files
        -> Python normalization and enrichment
        -> generated HTML + JSON + LaTeX
        -> HTML/CSS/vanilla JavaScript frontend
        -> GitHub Actions
        -> GitHub Pages
```

The build scripts fetch arXiv abstracts, produce first-page PDF thumbnails, generate publication and taxonomy views, produce matching LaTeX tables, validate new entries, and update cache versions. Generated table fragments are loaded into a common page through tab navigation.

The contribution form does not write to a live database. It prepares structured data or a patch for submission through GitHub, where CI checks the contribution before deployment.

## Reusable design patterns

- Academic-project hero with title, authors, affiliations, abstract, teaser, and primary resource buttons.
- A clear transition from explanatory landing page to interactive research collection.
- Publications, Taxonomy, Assets, Datasets, Statistics, and Add Entry as task-oriented views over related data.
- Paper cards combining visual preview, bibliographic metadata, abstract, taxonomy, and resource links.
- Taxonomy encoded as data so it can power filtering, comparison, and statistics.
- One source pipeline producing both website artifacts and publication-ready LaTeX tables.
- Static hosting, reproducible builds, cache busting, validation, and Git-based contributions.

## Adaptation for a broader personal research atlas

Do not copy the site's fragmented source model blindly. A multi-domain atlas should normally keep a canonical record per paper and derive all views from it. Useful fields include:

```yaml
id: stable-record-id
title: English title
title_zh: 中文标题
date: 2026-01-01
venue: arXiv
topics: []
tasks: []
representations: []
modalities: []
paper: https://...
project: https://...
code: https://...
dataset: null
model: null
demo: null
thumbnail: path-or-url
abstract_en: ""
abstract_zh: ""
notes: null
status: unread
```

Generate Paper, Taxonomy, Dataset, Asset, Statistics, and bilingual views from this canonical model. Keep personal reading status and editorial summaries separable from externally verified metadata.

## Cautions

- The reference repository did not visibly expose a license when recorded. Use it as an architectural and visual reference unless reuse permission is confirmed.
- Remote PDF and arXiv enrichment can be slow or rate-limited; cache results and preserve provenance.
- Generated HTML should not become another manually edited source of truth.
- A GitHub patch workflow suits technical contributors but may need an administrative form for personal or nontechnical use.
