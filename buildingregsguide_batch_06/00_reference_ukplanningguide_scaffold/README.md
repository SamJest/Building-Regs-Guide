# UKPlanningGuide Scaffold Pack

This pack is a compact export of the UKPlanningGuide static-site architecture for planning a related sister site such as BuildingRegsGuide.

It is not a full repo clone. It contains the source patterns, representative data, representative output, validation code and explanatory notes needed for another developer or AI to understand how the current site works and decide what should be reused.

## Quick Start

From a full repo, the normal build command is:

```powershell
python build_site.py
```

In this Codex environment, Python was available at:

```powershell
C:\Users\Jest\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
```

Targeted generation examples:

```powershell
python scripts\2_generate_homepage_and_indexes.py
python scripts\12_generate_planning_tools.py
python scripts\19_generate_building_regulations_pages.py
python scripts\21_generate_download_assets.py
python scripts\9_generate_sitemaps.py
python validate.py --mode local
```

## Pack Layout

- `source/`: build orchestration, templates, components, generators, scripts, utils, selected data modules and assets.
- `representative-data/`: sample projects, council files, rule files, official-source code and download-asset data.
- `representative-output/`: selected generated HTML pages and sitemap samples from different page families.
- `reports/`: current export report, route sample and existing SEO/build reports.

## How The Build Works

`build_site.py` runs generator scripts in a fixed order, clears `output/`, writes static HTML pages, copies assets, writes `CNAME` and `.nojekyll`, then calls `validate.py`.

Most pages follow this shape:

1. Load structured data from `data/`.
2. Build page sections with component functions.
3. Pass content to `core.render.inject_into_base`.
4. Write `output/.../index.html`.
5. Generate sitemaps from generated output.
6. Run validation and link audits.

## What To Reuse For A Sister Site

Safe to reuse after rebranding and domain changes:

- Static generator orchestration.
- `templates/base.html` layout pattern.
- SEO/meta/canonical/breadcrumb handling.
- Official-source block pattern.
- Tool rendering pattern.
- Download/linkable asset system.
- Sitemap generation and validation approach.
- Page-family separation between data, components and generators.

Planning-specific and should be rewritten:

- Planning permission copy and page titles.
- Local planning rule datasets.
- Planning-specific tools and decision logic.
- UKPlanningGuide brand voice where it mentions planning permission directly.
- GA ID and public analytics config unless intentionally shared.

## Known Warnings

- Full validation over roughly 35k generated pages can take longer than short command windows.
- Building regulations pages already exist inside UKPlanningGuide as a pilot, but a sister site should rebuild the content model around building-control decisions rather than copy planning pages directly.
- Output is intentionally sampled. Do not treat `representative-output/` as deployable.
- `source/data/*.py` includes large content registries for context, not a clean future-site dataset.

## Suggested Next Step For ChatGPT

Ask ChatGPT to design the sister-site architecture using this pack, starting from `FUTURE_SITE_REUSE_NOTES.md`, `PROJECT_ARCHITECTURE.md`, and the representative Building Regulations output pages.
