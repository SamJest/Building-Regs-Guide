# Download Assets System

The download/linkable asset system was added as a crawlable HTML-first resource layer.

Key files:

- `source/data/download_assets.py`
- `source/components/download_assets.py`
- `source/generators/download_assets.py`
- `source/scripts/21_generate_download_assets.py`
- `source/templates/base.html`
- validation in `source/validate.py`
- route registration in `source/utils/live_links.py`
- sitemap classification in `source/components/sitemap_builders.py`

## Current Behaviour

Download assets generate pages under `/downloads/{slug}/`.

Each page includes:

- print/save control using browser print
- copy link
- copy checklist text
- copy citation
- official source block
- related tools
- related guides
- disclaimer
- structured data
- sitemap inclusion
- inbound links from relevant source pages

## Why HTML First

The HTML page is the backlink target. Browser print is the first PDF path. This avoids adding brittle PDF dependencies while still giving users a printable resource.

## Sister Site Use

For BuildingRegsGuide, start with:

- Extension building regulations checklist.
- Building notice vs full plans worksheet.
- Completion certificate record sheet.
- Competent person scheme checklist.
- Inspection stage checklist.
- Garage conversion building regulations checklist.
- Loft conversion fire safety prep checklist.
- Drainage and waste checklist.
