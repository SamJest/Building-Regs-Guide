# Prompt 08 — wire router and source guards

Wire the Batch 3 rule files into the tool layer.

Tasks:

1. Import or adapt `approvedDocumentRouter.batch3.js`.
2. Load `approved_document_router_rules_v2.json` as data.
3. Return likely Approved Documents, evidence, red flags and warnings.
4. Add BSR warning for HRB inputs.
5. Add planning overlap warning linking to UKPlanningGuide.
6. Add validation using `sourceVersionGuard.batch3.js`.
7. Ensure the router result component links to the relevant project page and Approved Document hubs.

Tests:

- Loft conversion returns A, B, F, K, L, P.
- New dwelling conversion returns A, B, C, E, F, G, H, K, L, M, O, P, Q, R, S.
- Window replacement returns L, K, F and optionally B/Q depending on inputs.
- HRB flag shows BSR route warning.
- Part L pages include 2026 source/version note.
