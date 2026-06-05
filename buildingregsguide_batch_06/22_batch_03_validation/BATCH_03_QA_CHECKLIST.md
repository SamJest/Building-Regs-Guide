# Batch 3 QA checklist

Use this after Codex implements Batch 3.

## Route checks

- `/approved-documents/` exists.
- Every Approved Document hub route builds.
- Every project deep-dive route builds.
- New route registry can be generated from `route_registry_v3_combined.json`.

## Source checks

- Approved Document hubs link to GOV.UK Approved Documents.
- Part L hub links to Approved Document L 2026 and contains earlier-version warning.
- Higher-risk-building content routes to BSR, not ordinary domestic advice.
- Planning permission overlap boxes link to UKPlanningGuide.

## Content checks

- No official guidance is copied wholesale.
- No page guarantees approval or compliance.
- Project pages say likely/usually/often where the rule depends on design.
- Evidence and inspection sections are visible without scrolling too far.

## Tool checks

- Approved Document Router is data-driven.
- Tool results include official-source links.
- Tool results include evidence to keep.
- Tool results include red flags.
- Tool results include caveat/disclaimer.

## Internal linking checks

- Approved Document hubs link to relevant project pages.
- Project pages link to relevant Approved Document hubs.
- Tool pages link to both hubs and projects.
- UKPlanningGuide links appear only where planning overlap is real.
