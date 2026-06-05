# Pre-launch smoke test plan

Run these checks on staging before production.

## Core navigation

- Open homepage.
- Open project hub.
- Open Approved Document hub.
- Open tool.
- Generate tool result.
- Save result to dashboard.
- Print result.
- Open recommended download.
- Return to project page.
- Use internal search.

## Regression inputs

Test these project examples:

- single-storey extension, not started
- loft conversion with stairs and fire-door questions
- garage conversion with insulation and ventilation
- removing load-bearing wall
- replacement windows using registered installer
- electrical work in a bathroom
- missing certificate for past work
- high-rise flat / HRB signal

## Fail conditions

Fail the build if:

- a tool says approval is guaranteed
- HRB input goes through normal homeowner flow
- source panel missing on regulatory page
- noindex page appears in sitemap
- dashboard stores data remotely without explicit implementation and consent
- broken links appear in header/footer/core hubs
