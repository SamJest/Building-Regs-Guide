# Codex Master Prompt — Build BuildingRegsGuide From Batch 1 Pack

Use HIGH reasoning.

You are creating a new static sister site to UKPlanningGuide, not modifying UKPlanningGuide directly unless explicitly asked. Target site: `BuildingRegsGuide`. Placeholder canonical domain: `https://buildingregsguide.co.uk`.

Read these first:

1. `README_BATCH_01.md`
2. `01_strategy/SITE_POSITIONING.md`
3. `01_strategy/ARCHITECTURE_MAP.md`
4. `01_strategy/CROSS_SITE_LINKING_RULES.md`
5. `02_data/route_registry.json`
6. `02_data/source_registry.json`
7. `02_data/tool_registry.json`
8. `02_data/download_assets_registry.json`
9. `07_validation/VALIDATION_SPEC.md`
10. `00_reference_ukplanningguide_scaffold/PROJECT_ARCHITECTURE.md`
11. `00_reference_ukplanningguide_scaffold/FUTURE_SITE_REUSE_NOTES.md`
12. `00_reference_ukplanningguide_scaffold/DOWNLOAD_ASSETS_SYSTEM.md`
13. `00_reference_ukplanningguide_scaffold/TOOLS_SYSTEM.md`

Goal: create a clean Python static generator repo for BuildingRegsGuide using the architecture patterns from UKPlanningGuide and the data/content supplied in this pack.

Hard rules:

- Reuse architecture patterns, not planning content.
- Do not copy UKPlanningGuide branding, copy, analytics IDs or planning-specific route logic.
- England-first. Add Wales/Scotland guardrail pages only; do not pretend England guidance is UK-wide.
- Every substantial page must include official-source blocks from `source_registry.json`.
- Do not create local council/building-control-body pages yet.
- Do not add heavy monetisation or lead capture in this first implementation.
- Implement HTML-first downloads; browser print is enough for Batch 1.
- Every internal link must validate.
- Every tool result must link to at least one guide, one official source and one printable asset.

Implementation target:

1. Working `build_site.py`.
2. Rebranded `templates/base.html`.
3. Data modules from `06_overlay_source/source/data/` adapted into the repo.
4. Generators/components for guide pages, project pages, Approved Document pages, tool pages and downloads.
5. First prototype generated pages: homepage, all high-priority routes, at least 5 tools and 10 downloads.
6. Sitemap generation.
7. Validation script adapted from UKPlanningGuide principles.

Deliverables:

- List of files created/changed.
- Build command.
- Validation command and results.
- Any routes skipped and why.
- Any assumptions about domain/analytics/CNAME.
