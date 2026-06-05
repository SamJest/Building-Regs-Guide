# Architecture Map

Reuse the UKPlanningGuide static architecture, not its planning-copy.

## Reuse

- Python static generator orchestration.
- `templates/base.html` pattern after rebranding.
- route registry / live-link validation approach.
- answer-first guide templates.
- official-source block system.
- tool rendering pattern.
- HTML-first printable download assets.
- sitemap generation and strict validation.

## Replace

- planning permission data and page copy.
- planning-specific tools.
- local planning authority assumptions.
- UKPlanningGuide metadata wording.
- planning-heavy internal links unless used as contextual handoffs.

## New route families

1. `/building-regulations/` — basics and approval routes.
2. `/projects/{project}-building-regulations/` — project-specific building regs checks.
3. `/approved-documents/{approved-document}/` — homeowner-focused Approved Document hubs.
4. `/tools/{tool}/` — static decision tools.
5. `/downloads/{asset}/` — printable HTML-first assets.
6. `/building-regulations/wales/` and `/building-regulations/scotland/` — jurisdiction guardrails.

## Build order

1. Rebrand base template and global nav.
2. Add data registries from `02_data/`.
3. Implement core guide generator.
4. Implement project page generator.
5. Implement Approved Document page generator.
6. Implement downloads generator.
7. Implement first 5 tools.
8. Wire internal links and source blocks.
9. Generate sitemaps.
10. Run validation and fix errors before adding more routes.
