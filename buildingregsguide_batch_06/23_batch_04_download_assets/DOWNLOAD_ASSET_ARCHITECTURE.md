# Batch 4 download asset architecture

Batch 4 adds 48 Codex-ready downloadable/printable assets. These are not final PDFs. They are structured markdown drafts and data records that Codex should render as:

1. normal HTML landing pages,
2. printer-friendly HTML,
3. optional generated PDFs later,
4. saved project-pack outputs inside the project dashboard.

## Why this matters

The sister site should not just answer "do I need building regulations?" once. It should keep homeowners returning during the whole project:

- before quotes,
- before application,
- before inspection stages,
- before covering up work,
- before final completion,
- before selling the home.

## Asset families

- **before_you_start**: Before-you-start packs
- **project_specific**: Project-specific checklists
- **evidence**: Evidence and certificate trackers
- **inspection**: Inspection-stage printables
- **approved_documents**: Approved Document quick packs
- **installer**: Installer and competent-person forms
- **sale_and_handover**: Sale, handover and record-keeping packs

## Implementation model for Codex

Create a `downloads` data collection from `download_assets_v4_registry.json`.

Each asset should have:

- title,
- plain-English purpose,
- source/date warning,
- project tags,
- related tool CTA,
- related project links,
- print button,
- save-to-project button,
- email-free option by default.

Do not block downloads behind email capture at launch. The user wants traffic/trust first. Use optional email capture later, after the site has stable search traffic.

## Lead magnet placement

- Homepage: before-you-start checklist and route decision sheet.
- Project pages: matching project-specific pack.
- Approved Document hubs: approved document router printout + Part-specific pack.
- Tool results: save answer + print tailored pack.
- Certificate pages: evidence folder + competent-person tracker.

## Build priority

1. Universal before-you-start checklist.
2. Extension prep pack.
3. Loft conversion fire/structure checklist.
4. Garage conversion pack.
5. Completion certificate evidence folder.
6. Competent person certificate tracker.
7. Inspection-stage checklist.
8. Approved Document router printout.
