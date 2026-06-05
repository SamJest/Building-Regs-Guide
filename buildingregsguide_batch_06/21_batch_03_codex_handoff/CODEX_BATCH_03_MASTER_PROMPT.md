# Codex Batch 3 master prompt

You are continuing the BuildingRegsGuide implementation using the cumulative pack.

Main goal: implement the Batch 3 Approved Document and project-deep-dive layer without turning the site into a copied legal document repository.

Use these files:

- `18_batch_03_approved_document_hubs/approved_document_hub_index.json`
- `18_batch_03_approved_document_hubs/full_page_markdown/*.md`
- `19_batch_03_project_deep_dives/project_deep_dive_index.json`
- `19_batch_03_project_deep_dives/full_page_markdown/*.md`
- `19_batch_03_project_deep_dives/project_approved_document_crosswalk.json`
- `20_batch_03_tool_rules/approved_document_router_rules_v2.json`
- `20_batch_03_tool_rules/*.js`
- `17_batch_03_source_update/official_source_snapshot_2026-06-04.json`

Implementation requirements:

1. Create a route family for Approved Document hubs.
2. Create a route family for project deep-dive pages.
3. Render Approved Document chips on project pages.
4. Render project chips on Approved Document pages.
5. Add a source/version panel to every Approved Document page.
6. Add a planning-permission separation box to project pages.
7. Wire the Approved Document Router to the Batch 3 rules.
8. Add source version guard validation.
9. Preserve the existing UKPlanningGuide-inspired architecture but do not make this a planning site clone.
10. Keep copy plain-English and homeowner-facing.

Definition of done:

- All new routes build.
- Every Batch 3 page has title/meta description/source block/internal links.
- Approved Document Router uses data, not hard-coded copy.
- No page states that a project is legally approved or guaranteed compliant.
- Validation fails if source-sensitive pages omit required source notes.
