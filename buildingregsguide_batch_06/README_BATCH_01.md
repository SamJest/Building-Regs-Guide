# BuildingRegsGuide Batch 1 Codex Pack

Created: 2026-06-04

Purpose: start the sister site to `ukplanningguide.co.uk` using the proven static architecture, but rebuilt around building regulations, building control, Approved Documents, competent person schemes, inspections and completion evidence.

This pack contains:

- `00_reference_ukplanningguide_scaffold/` — the uploaded scaffold, included as reference only.
- `01_strategy/` — site positioning, architecture, page families, cross-site linking and build sequence.
- `02_data/` — machine-readable seed registries for routes, sources, tools, downloads, Approved Documents, FAQs and validation rules.
- `03_content_briefs/` — page brief for every Batch 1 seed route.
- `04_tools_logic/` — decision-tree specs for the first interactive tools.
- `05_codex_prompts/` — master prompt and staged implementation prompts.
- `06_overlay_source/` — Python modules Codex can adapt into the new repo.
- `07_validation/` — validation checklist and route-family rules.
- `08_wireframes/` — simple HTML wireframes for the homepage, guide page and tool result flow.
- `09_manifest/` — file and route inventory.

Working assumption: target domain placeholder is `https://buildingregsguide.co.uk`. Codex should replace it if you buy/use a different domain.

Batch 1 deliberately avoids creating local council/building-control pages. The data source for local building-control bodies needs a separate verification pass first.
