# SEO And Internal Linking

## Metadata

SEO metadata is mostly produced in `source/components/seo.py` and refined in `source/core/render.py`.

Each generated page receives:

- `<title>`
- meta description
- canonical URL
- Open Graph and Twitter metadata
- structured data
- breadcrumbs

## Breadcrumbs

Generators pass breadcrumb tuples into `inject_into_base`, for example:

```python
options={"breadcrumbs": [("Home", "/"), ("Downloads", "/downloads/"), (asset["title"], "")]}
```

The base renderer converts those into a breadcrumb nav.

## Internal Links

Internal links are generated in several ways:

- Component cards and related route blocks.
- Promoted links in `source/data/promoted_links.py`.
- Page-family route logic.
- Download asset source-page attachments.
- Tool result follow-up links.

`source/utils/live_links.py` is the route allow-list used by validation. New route families must be registered there.

## Sitemap

`source/components/sitemap_builders.py` walks `output/`, classifies URLs by route pattern, writes child sitemaps and creates `output/sitemap.xml`.

New page families need:

- A classifier branch.
- Priority and changefreq treatment if different from defaults.
- Live-route registration.

## Sister Site Advice

Do not copy keyword patterns directly. Reuse:

- answer-first metadata structure
- canonical discipline
- breadcrumb pattern
- related-card handoffs
- source-backed trust blocks

Rewrite:

- planning permission query targeting
- local planning route wording
- project-specific planning assumptions
