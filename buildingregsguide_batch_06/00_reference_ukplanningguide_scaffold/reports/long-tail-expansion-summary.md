# Long-Tail Expansion Summary

Date: 2026-04-28

## Expansion Size

- Previous generated output: 23,975 pages
- Expanded generated output: 34,106 pages
- Net increase: 10,131 pages
- New project-scenario rollout pairs added: 33
- Planning areas per pair: 307

## Rollout Strategy

The expansion uses the existing project-specific scenario generator rather than creating a new template family. Each added pair creates a useful local long-tail route such as:

- `/dropped-kerbs/{county}/{council}/planning-permission/`
- `/porches/{county}/{council}/permitted-development/`
- `/side-extensions/{county}/{council}/distance-from-boundary/`
- `/change-of-use/{county}/{council}/article-4/`

This keeps the site static-first and reuses existing metadata, official source, trust, internal link and CTA components.

## New Page Families Added

Added rollout coverage for:

- dropped kerbs: planning permission, permitted development, boundary rules, conservation areas, listed buildings
- porches: planning permission, permitted development, height limits, maximum height, conservation areas
- side extensions: planning permission, permitted development, height limits, boundary rules, distance from boundary, conservation areas
- single-storey extensions: planning permission, permitted development, depth limits, height limits, boundary rules
- garage conversions: planning permission, permitted development, roof alterations, conservation areas
- driveways: planning permission, permitted development, boundary rules, conservation areas
- change of use: planning permission, permitted development, Article 4, conservation areas

## Why These Families

The selection follows the Search Console opportunity report:

- dropped kerb pages already showed local traction and clear planning/highway intent
- porch pages had impressions, especially around Cardiff/Wales-style planning searches
- extension queries showed demand for local and measurement-specific routes
- garage conversion and change-of-use queries showed early impressions but needed better local/rule matching
- Article 4, conservation area and permitted development pages already performed well as long-tail modifiers

## Validation

Generated and validated:

- `scripts/3b_generate_project_scenario_pages.py`
- `scripts/8_generate_nearby_links.py`
- `scripts/9_generate_sitemaps.py`
- `validate.py --mode links`
- `validate.py --mode role-metadata`
- `validate.py --mode content`

Validation results:

- Sitemap audit passed with 22 sitemap files and 34,103 indexed sitemap URLs
- Local-search audit passed
- Canonical and internal-link scan passed across 34,106 generated HTML pages
- Page health: healthy, 100% coverage across critical, important and long-tail groups
- Role metadata audit passed
- Metadata quality audit passed
- Content validation passed

Content validation now samples large generated families deterministically for repeated template checks, while sitemap/link and metadata checks still run broadly.

## Notes To Monitor

- New long-tail impressions for dropped kerb, porch, side-extension, single-storey extension, driveway, garage-conversion and change-of-use modifiers.
- Whether Google indexes the new project-scenario sitemap chunks quickly.
- CTR on the new local/rule combinations versus the broader local project pages.
- Family-repetition warnings on large generated groups; these are not build blockers, but they show where the next quality pass should add more local variation.
