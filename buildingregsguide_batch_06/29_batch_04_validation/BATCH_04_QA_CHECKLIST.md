# Batch 4 QA checklist

Date: 2026-06-04

## Counts

- Download asset records: 48
- Full asset markdown files: 48
- Retention loop records: 8
- Prototype JS modules: 3
- Wireframes: 3
- Codex prompts: 4

## Must pass

- [ ] `/downloads/` index can be generated from JSON.
- [ ] Individual download pages can be generated from markdown files.
- [ ] Print button works and print layout hides nav but keeps warnings.
- [ ] Project dashboard stores data in localStorage only.
- [ ] User can export/import saved project JSON.
- [ ] Tool result can be saved with source snapshot and generated date.
- [ ] Certificates and evidence are metadata-only at launch.
- [ ] No email gate at launch.
- [ ] No false approval/compliance certainty.
- [ ] HRB, flat/common-parts and Part L/F warnings appear where relevant.

## Manual test scenarios

1. Create an extension project, run route checker, save result, print extension prep pack.
2. Create a loft conversion project, generate Part A/B/F/L flags, save inspection timeline.
3. Create a windows/doors project, add competent-person certificate expected item.
4. Export a project, clear localStorage, import project, confirm data returns.
5. Print a checklist and verify warning/source/date are visible.
