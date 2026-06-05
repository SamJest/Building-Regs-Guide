# Prompt 02 — Implement tools and downloads

Use `04_tools_logic/` and `02_data/download_assets_registry.json`.

Implement static tool pages with inline JavaScript. No backend/API.

First tools:

1. building-control-route-checker
2. full-plans-vs-building-notice-checker
3. competent-person-scheme-checker
4. completion-certificate-readiness-checker
5. inspection-stage-checklist-generator

Every result state must include:

- result label
- why this route was selected
- evidence to gather
- official source links
- related guide
- related printable checklist

Implement download pages under `/downloads/{slug}/` with:

- print button
- copy checklist text button
- related guide/tool cards
- source block
- disclaimer
- structured data where existing pattern supports it
