# Sitemap generation contract

## Files

Generate:

- `/sitemap.xml` for indexable canonical pages.
- `/sitemap-pages.xml` if the page count exceeds a comfortable single-file threshold.
- `/sitemap-tools.xml` for tools if separated.
- `/robots.txt` pointing to the sitemap index or main sitemap.

## Include only

- Canonical HTML routes.
- Pages that pass validation.
- Download landing pages, not raw generated PDF/print files.

## Exclude

- Tool result URLs with user-specific data.
- Print-only views.
- Draft pages.
- Any route with missing source block.
- Duplicate paths or non-trailing-slash URLs.

## Change frequency guidance

- Homepage and major hubs: weekly.
- Project/Approved Document hubs: monthly unless source changes.
- Download pages: monthly.
- Tools: monthly.
- Source-sensitive Part L/F/HRB pages: check after source registry update.
