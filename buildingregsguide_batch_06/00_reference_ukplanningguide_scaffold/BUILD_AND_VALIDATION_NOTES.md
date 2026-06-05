# Build And Validation Notes

## Build Entrypoint

Main entrypoint: `source/build_site.py`

The build runs generator scripts from `source/scripts/` in order. The current build order includes core local/project pages, homepage/index pages, scenario pages, council pages, tools, FAQ pages, upgrade pages, download assets and sitemaps.

## Important Commands

```powershell
python build_site.py
python validate.py --mode local
python validate.py --mode links
python validate.py --mode content
python scripts\9_generate_sitemaps.py
python scripts\21_generate_download_assets.py
```

## Validation Coverage

`validate.py` checks:

- Rule inventory and local rule notes.
- Curated internal routes.
- Tool pages and interactive root markers.
- Tool smoke tests via Node.
- Canonicals, internal links and sitemap consistency.
- Metadata quality and role language.
- Official source block presence.
- Personalised guidance and Find Help pages.
- Duplicate and repeated content patterns.
- Local search and GSC recovery target integrity.
- Building regulations pages.
- Download asset pages.

## Current Export Verification

During export, targeted checks passed for:

- Python compile on changed scaffold/download files.
- Download asset page generation.
- Sitemap generation.
- Sitemap audit.
- Download asset audit: 20 assets.

The full `validate.py --mode local` pass was attempted, but the site-wide scan exceeded the available command window. This appears to be runtime size, not a reported failure.

## Fragile Areas

- `validate.py` is intentionally strict and knows many current route families.
- `utils/live_links.py` must be updated when new route families are added.
- `components/sitemap_builders.py` must classify new page families or sitemap checks may fail.
- The base template contains global CSS/JS, so new features can affect all pages.
