# Batch 5 QA checklist

## Route and indexability

- [ ] Route paths are lowercase and trailing-slash normalized.
- [ ] Candidate routes are not published until content passes the build gate.
- [ ] No route is orphaned unless intentionally noindex.
- [ ] No route has fewer than 3 outgoing links; content pages should target 5+.
- [ ] Canonical URLs do not include query strings.

## Content quality

- [ ] Every indexable page has a visible official source block.
- [ ] Every Part L/energy page has a 2026/version warning where relevant.
- [ ] Every Part F/ventilation page has 2026 circular/source handling where relevant.
- [ ] Every higher-risk building page routes to BSR and avoids ordinary domestic simplification.
- [ ] Every competent person scheme page explains it only applies to covered work by registered scheme members.
- [ ] Every planning/building-regs comparison says planning permission and building regulations approval are separate.

## Schema

- [ ] JSON-LD parses.
- [ ] Breadcrumb schema exists on all indexable pages.
- [ ] FAQ schema only appears when Q&A is visible on the page.
- [ ] Tool pages use SoftwareApplication schema with free GBP offer.
- [ ] No unresolved `{{placeholder}}` strings.

## Sitemap and robots

- [ ] Sitemap includes only canonical indexable pages.
- [ ] Raw print/tool-state URLs are excluded.
- [ ] `/robots.txt` points to the sitemap.
- [ ] Download landing pages are indexable; raw generated files are not.

## Internal links

- [ ] Project pages link to related Approved Documents.
- [ ] Approved Document pages link back to relevant projects.
- [ ] Question pages link to parent project and at least one tool/download.
- [ ] Evidence pages link to dashboard and evidence downloads.
- [ ] Cross-site links to UKPlanningGuide are contextually justified.
