# Batch 4 retention loop architecture

The sister site should become a project companion, not a one-off article site.

## Launch principle

Use no-login local storage at launch. This avoids account friction and supports fast static deployment. Account sync, email reminders and paid upgrades can be added later after traffic exists.

## Core object model

```json
{
  "project_id": "uuid",
  "created_at": "2026-06-04T00:00:00Z",
  "updated_at": "2026-06-04T00:00:00Z",
  "jurisdiction": "england",
  "project_type": "loft_conversion",
  "project_label": "Loft conversion",
  "property_type": "house",
  "is_flat_or_common_parts": false,
  "is_higher_risk_possible": false,
  "source_snapshot_id": "official_source_snapshot_2026-06-04",
  "saved_tool_results": [],
  "downloads": [],
  "inspection_stages": [],
  "evidence_items": [],
  "certificate_chaser": [],
  "notes": []
}
```

## Pages Codex should add

- `/my-project/` — local dashboard.
- `/my-project/new/` — project setup wizard.
- `/my-project/evidence/` — evidence metadata log.
- `/my-project/inspections/` — timeline and stage cards.
- `/my-project/certificates/` — certificate chaser.
- `/downloads/` — asset index.

## No-login dashboard modules

1. Project summary card.
2. Approval route status.
3. Approved Document flags.
4. Inspection timeline.
5. Evidence/certificate tracker.
6. Downloaded packs.
7. Re-check source warning.
8. Cross-link to UKPlanningGuide planning checker pages.

## Privacy rule

At launch, do not upload or store files. Store only user-entered metadata in browser local storage. Explain this clearly.

## Retention CTAs

Use these CTAs across the site:

- Save this result to my project.
- Print this checklist.
- Add this to my evidence folder.
- Build my inspection timeline.
- Re-check because my project changed.
- Check planning permission on UKPlanningGuide.
