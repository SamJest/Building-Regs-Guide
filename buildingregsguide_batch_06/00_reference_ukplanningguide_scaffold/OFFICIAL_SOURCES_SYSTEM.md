# Official Sources System

Official source handling appears in:

- `source/data/official_sources.py`
- `source/utils/official_sources.py`
- `source/components/official_sources.py`
- `source/components/page_authority.py`
- validation checks in `source/validate.py`

## Current Model

The site stores official sources by authority, page family, category and source relevance. Components select a small number of relevant links for the page context.

Typical context fields:

- page family
- authority slug
- country slug
- project slug
- scenario slug
- max links

## Rendered Output

Official source blocks include:

- source title
- category label
- last reviewed date where available
- reason the source matters
- outbound official link

## Sister Site Mapping

For BuildingRegsGuide, source categories should be rebuilt around:

- GOV.UK building regulations guidance
- Planning Portal building control routes
- Approved Documents
- competent person schemes
- local authority building control pages
- warranty/building control body guidance where appropriate
- devolved jurisdiction pages

Keep the principle: every high-risk page should show the official source most likely to settle the next decision.
