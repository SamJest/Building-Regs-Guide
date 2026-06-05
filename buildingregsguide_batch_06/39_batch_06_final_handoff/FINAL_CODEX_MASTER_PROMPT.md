# FINAL CODEX MASTER PROMPT — BuildingRegsGuide

You are implementing BuildingRegsGuide, a sister site to UKPlanningGuide. Your job is to convert this cumulative pack into a clean, static-first website that helps UK homeowners understand building regulations routes, evidence, inspection stages, competent person certificates and completion paperwork.

## Non-negotiable positioning

BuildingRegsGuide is not a clone of UKPlanningGuide. UKPlanningGuide handles planning permission and planning policy. BuildingRegsGuide handles building regulations approval, building control routes, Approved Documents, inspections, completion certificates and proof/evidence.

When a page overlaps with planning permission, keep the planning explanation brief and link to UKPlanningGuide for the deeper planning side.

## Non-negotiable safety/source rules

1. Never imply that the site grants approval or replaces building control, a competent professional, structural engineer, designer, installer or local authority/registered building control approver.
2. Use source/version panels on regulatory pages and tool results.
3. Treat England guidance separately from Wales, Scotland and Northern Ireland.
4. Treat higher-risk building signals as a stop-route to BSR/specialist guidance, not a normal homeowner flow.
5. Do not publish candidate SEO pages as indexable unless they pass source, uniqueness, body-depth, internal-link and schema checks.
6. Add date-generated and re-check warnings to downloadable/printable assets.
7. Keep the dashboard no-login/local-only unless explicitly implementing a real backend later.

## Build approach

Use the existing uploaded UKPlanningGuide scaffold as a structural reference only. Reuse proven static generation patterns, but rename and repurpose data, content, CTAs and routing around BuildingRegsGuide.

Start with Phase 1 launch pages and tools. Candidate pages can exist as draft/noindex but must not enter the sitemap until launchQualityGate passes.

## Core folders to read first

1. `README_BATCH_06.md`
2. `39_batch_06_final_handoff/CODEX_EXECUTION_SEQUENCE.md`
3. `39_batch_06_final_handoff/implementation_tickets.json`
4. `44_batch_06_citations_and_sources/current_source_snapshot_2026-06-05.json`
5. `43_batch_06_content_priority/phase_1_launch_page_list.json`
6. `41_batch_06_overlay_source/source/launchQualityGate.js`
7. `30_batch_05_seo_scale/NO_THIN_PAGE_POLICY.md`
8. `32_batch_05_internal_linking/INTERNAL_LINKING_STRATEGY.md`

## Output requirement

Build a coherent, navigable, static-first site. Include generated pages, tools, downloads, sitemap, robots, search index, schema, source panels, print views, and QA scripts. Produce a final build report listing what was published, what remains noindex/draft, and any blocked pages with reasons.
