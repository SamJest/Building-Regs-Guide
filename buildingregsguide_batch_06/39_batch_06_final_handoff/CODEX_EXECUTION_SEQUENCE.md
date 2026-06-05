# Codex execution sequence

## Step 0 — Read before building

Read the final master prompt and the source snapshot. Confirm that the site is England-first and version-aware.

## Step 1 — Create the project shell

- Reuse the scaffold's static generation architecture where possible.
- Replace UKPlanningGuide branding, domains and content models with BuildingRegsGuide models.
- Add global components: source panel, breadcrumbs, warning box, related content, tool CTA, download CTA, print button.

## Step 2 — Import registries

- Import source registry and source snapshot.
- Import route registries.
- Import tool registry.
- Import download registry.
- Import link graph.
- Add schema and sitemap factories.

## Step 3 — Publish phase 1 pages only

Use `43_batch_06_content_priority/phase_1_launch_page_list.json` as the first publish queue. If a page lacks enough unique content, keep it draft/noindex and record the reason.

## Step 4 — Implement tools

Build the route checker, full plans vs building notice checker, competent person checker, completion certificate checker and Approved Document router first. Each result must show:

- likely route, not guaranteed answer
- confidence level
- red flags
- official source links
- next actions
- recommended downloads
- save/print buttons
- generated date and re-check warning

## Step 5 — Build downloads and dashboard

Generate download asset pages and print CSS. Implement no-login dashboard with localStorage only. Make privacy copy explicit.

## Step 6 — Add SEO system

- Generate schema only from visible page content.
- Generate sitemap only from indexable pages.
- Generate search index.
- Apply no-thin-page policy.
- Create hub/spoke links and contextual links.

## Step 7 — Run launch gates

Run route, source, content, link, schema, tool and dashboard gates. Do not override failures silently. Fix or keep draft/noindex.

## Step 8 — Deploy staging

Deploy a preview build and run the final QA matrix.

## Step 9 — Deploy production

Submit sitemap, check Search Console, and follow the 30-day post-launch plan.
