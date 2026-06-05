# Codex Batch 2 Master Prompt

You are continuing the BuildingRegsGuide sister-site build using the cumulative batch pack. Batch 1 supplied the architecture, sources, route registry, initial page briefs, tool registry and validation rules. Batch 2 adds deeper page drafts, project matrices, inspection-stage data, competent-person routing data and a first implementation-ready decision engine.

## Main implementation goals

1. Import the Batch 2 project matrix and decision engine into the static site source tree.
2. Convert the full-page markdown drafts into generated data records or page templates, preserving source handling and conservative wording.
3. Implement the shared tool result component contract.
4. Build at least these tools in working static JS:
   - Building Control Route Checker
   - Full Plans vs Building Notice Checker
   - Competent Person Scheme Checker
   - Completion Certificate Readiness Checker
   - Inspection Stage Checklist Generator
5. Build download landing pages for the six Batch 2 asset specs.
6. Ensure every route has source links and a visible `last checked` date.

## Hard constraints

- Do not clone UKPlanningGuide branding or copy planning pages directly.
- Keep cross-links to UKPlanningGuide as helpful sister-site links only.
- Do not state that users are approved, compliant, legal or safe to start.
- Higher-risk building answers must route to BSR guidance.
- Part L pages must be version-aware because a 2026 Approved Document L source is included.
- Keep the site useful before monetisation. Prioritise trust, retention, source transparency and downloadable assets.

## Test expectations

After implementation, run the project's existing validation flow. Add or adapt checks for:

- No empty source URLs.
- No generated result uses banned phrases: `you are approved`, `safe to start`, `definitely compliant`, `guaranteed`.
- Tool result JSON always contains outcome, reasons, warnings, nextSteps, approvedDocuments, evidence and inspectionStages.
- Project pages link back to core explainer pages and at least one tool.
