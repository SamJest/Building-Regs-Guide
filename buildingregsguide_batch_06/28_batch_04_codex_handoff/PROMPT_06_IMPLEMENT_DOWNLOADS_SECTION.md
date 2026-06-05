# Prompt 06: Implement downloads section

Implement the BuildingRegsGuide downloads section.

Inputs:

- `23_batch_04_download_assets/download_assets_v4_registry.json`
- `23_batch_04_download_assets/full_asset_markdown/*.md`
- `26_batch_04_wireframes/download_landing_page_wireframe.html`
- `27_batch_04_content_and_linking/download_landing_page_briefs.json`

Tasks:

1. Create `/downloads/` index page grouped by asset category.
2. Create individual pages at `/downloads/{asset_id}/`.
3. Render each page with a source/date warning panel.
4. Add print CSS.
5. Add "Save to my project" CTA, even if the dashboard is implemented in Prompt 07.
6. Add related tools and related downloads.
7. Add schema where appropriate: `WebPage`, `HowTo` only if the page gives steps, and `FAQPage` only if visible FAQs exist.

Acceptance criteria:

- Pages build without broken routes.
- Assets are not hidden behind email capture.
- Pages include warnings that the printable is not approval.
