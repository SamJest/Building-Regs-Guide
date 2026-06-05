# Prompt 01 — Create repo scaffold

Create the initial BuildingRegsGuide repo from the Batch 1 pack.

Use the UKPlanningGuide scaffold only as a reference architecture. Build a new repo structure:

- `build_site.py`
- `source/core/`
- `source/templates/base.html`
- `source/data/`
- `source/components/`
- `source/generators/`
- `source/scripts/`
- `source/utils/`
- `source/assets/`
- `output/` generated only by build

Copy/adapt data from `06_overlay_source/source/data/`.

First successful build should generate:

- `/`
- `/building-regulations/`
- top 15 guide/project routes from `route_registry.json`
- 5 tool shells
- 10 download pages
- `/sitemap.xml`

Do not add local pages, monetisation, email capture, or copied UKPlanningGuide planning text.
