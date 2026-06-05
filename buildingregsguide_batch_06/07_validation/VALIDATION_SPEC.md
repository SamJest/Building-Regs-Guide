# Validation Spec

Target route count in this seed pack: 108.

## Required failures

Validation should fail if:

- a path is duplicated;
- a slug is duplicated;
- a page has no source block;
- a tool result has no official source;
- a page says `guaranteed approval`, `definitely compliant`, or similar;
- an England-first guide appears under Wales/Scotland routes;
- a local building control page is generated without verified local source data;
- a download page is PDF-only rather than HTML-first;
- sitemap includes a route that was not generated;
- generated HTML includes UKPlanningGuide branding after rebrand.

## Manual QA sample

Check these first after build:

- `/`
- `/building-regulations/`
- `/building-regulations/do-i-need-building-regulations-approval/`
- `/building-regulations/full-plans-vs-building-notice/`
- `/projects/extensions-building-regulations/`
- `/projects/loft-conversion-building-regulations/`
- `/tools/building-control-route-checker/`
- `/downloads/extension-building-regulations-checklist/`
- `/building-regulations/wales/`
- `/building-regulations/scotland/`
