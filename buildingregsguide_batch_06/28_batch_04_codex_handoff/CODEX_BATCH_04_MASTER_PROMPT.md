# Codex Batch 4 master prompt

You are implementing Batch 4 of BuildingRegsGuide, a sister site to UKPlanningGuide.

Use all previous batch folders as context. Batch 4 adds the retention and downloadable asset layer. Do not replace existing Batch 1-3 architecture; extend it.

## Main objectives

1. Add a `/downloads/` section powered by `23_batch_04_download_assets/download_assets_v4_registry.json`.
2. Render each download asset as normal HTML and print-friendly HTML.
3. Add a no-login `/my-project/` dashboard using browser localStorage only.
4. Make every major tool result saveable, printable and linked to recommended downloads.
5. Add inspection timeline, certificate chaser and evidence metadata components.
6. Add source/date/version warning panels on saved and printed outputs.
7. Preserve cross-site linking to UKPlanningGuide for planning permission checks.

## Files to use

- `23_batch_04_download_assets/download_assets_v4_registry.json`
- `23_batch_04_download_assets/full_asset_markdown/*.md`
- `24_batch_04_retention_system/retention_loops_registry.json`
- `24_batch_04_retention_system/LOCAL_STORAGE_CONTRACT.md`
- `25_batch_04_tool_extensions/*.js`
- `26_batch_04_wireframes/*.html`
- `27_batch_04_content_and_linking/*.json`

## Implementation approach

Create reusable components:

- `DownloadCard`
- `SourceWarningPanel`
- `PrintButton`
- `SaveToProjectButton`
- `ProjectDashboardCard`
- `EvidenceItemForm`
- `CertificateChaserItem`
- `InspectionTimeline`
- `RecommendedDownloads`

## Data rules

- Every saved item includes `generated_at` and `source_snapshot_id`.
- Every printed item includes a visible official-source warning.
- Every project stores only local metadata at launch.
- Do not require an account.
- Do not require email capture.
- Do not store uploaded files.

## Done definition

- `/downloads/` index works.
- At least 10 priority download pages render.
- Print CSS works for download pages.
- A project can be created, saved to localStorage, exported and imported.
- A tool result can be saved to a project.
- Dashboard shows route, downloads, evidence, certificates and inspection cards.
- No page claims that the site grants approval.
