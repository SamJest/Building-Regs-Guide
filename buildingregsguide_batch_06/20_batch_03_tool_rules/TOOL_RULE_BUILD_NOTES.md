# Batch 3 tool rule build notes

This batch adds router depth rather than full UI.

Codex should:

1. Load `approved_document_router_rules_v2.json` into the Approved Document Router.
2. Use project IDs from `project_deep_dive_index.json`.
3. Render results as:
   - likely Approved Documents;
   - why each Part may matter;
   - evidence to keep;
   - inspection points;
   - red flags;
   - official-source links.
4. Treat every result as advisory route-finding, not approval.
5. Trigger UKPlanningGuide cross-links where planning status is unknown.
6. Trigger BSR routing where HRB flags appear.
