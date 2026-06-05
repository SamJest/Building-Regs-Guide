# Tool Implementation Overview

Use the UKPlanningGuide static tool pattern: data registry -> generator -> static HTML shell -> inline JavaScript decision tree -> result cards -> related routes/downloads.

First tools to implement:

- `building-control-route-checker` — Chooses likely next route: planning-first, full plans, building notice, competent person, regularisation, or specialist advice.
- `full-plans-vs-building-notice-checker` — Compares project complexity, certainty needs, start timing and structural risk.
- `competent-person-scheme-checker` — Checks whether the work type commonly fits registered installer self-certification.
- `completion-certificate-readiness-checker` — Creates a record list for inspections, certificates and missing evidence before completion.
- `inspection-stage-checklist-generator` — Builds likely inspection/evidence stages for extensions, lofts, garages and structural work.
- `approved-document-router` — Maps project features to relevant Approved Documents and source pages.
- `extension-regs-prep-pack` — Generates a pre-application pack for extension building control conversations.
- `loft-fire-safety-prep-checker` — Flags loft conversion fire, escape and stair questions to settle before quotes.
- `garage-conversion-regs-checker` — Checks common garage conversion triggers: damp, insulation, ventilation, structure and fire.
- `structural-alteration-readiness-checker` — Creates a checklist for beams, openings, calculations, party wall risk and inspections.

Common result fields:

- `route_label`
- `confidence`
- `why`
- `before_you_start`
- `evidence_to_keep`
- `official_sources`
- `related_guides`
- `related_downloads`
- `planning_handoff_url`

Never produce a result that says work is definitely compliant. Say what route/evidence needs checking.
