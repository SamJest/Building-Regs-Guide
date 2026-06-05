# Project Architecture

UKPlanningGuide is a Python static site generator.

## Main Layers

- `source/build_site.py`: orchestrates the full build.
- `source/scripts/`: thin command wrappers for each generator.
- `source/generators/`: page-family generators that load data and write HTML.
- `source/components/`: section builders, page blocks, tools and reusable UI.
- `source/core/`: file writing, paths and base-template injection.
- `source/templates/base.html`: shared layout, CSS, navigation, analytics, sitewide JS.
- `source/data/`: structured registries, page definitions, tool configs and source data.
- `source/utils/`: URL normalization, official source selection, internal links, sitemap config and route contracts.
- `source/validate.py`: build audit and validation suite.

## Generation Pattern

Most generators follow the same pattern:

1. Import data loaders and component builders.
2. Loop through a registry or dataset.
3. Build content sections as HTML strings.
4. Call `inject_into_base`.
5. Write `index.html` into `output/`.

## Base Rendering

`core.render.inject_into_base` handles:

- Metadata refinement.
- Social meta tags.
- Canonical link.
- Breadcrumb rendering.
- Structured data.
- Page trust strip.
- Sticky action bar for inner pages.
- Global tool templates.

## Sister Site Implication

For BuildingRegsGuide, keep the architecture but rebuild the data model around:

- Building-control routes.
- Approved Documents.
- Competent person schemes.
- Inspections and certificates.
- Project-specific building regulations triggers.
- England/Wales/Scotland differences where useful.
