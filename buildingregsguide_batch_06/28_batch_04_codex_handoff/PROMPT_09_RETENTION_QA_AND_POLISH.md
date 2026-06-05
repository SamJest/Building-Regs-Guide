# Prompt 09: Batch 4 retention QA and polish

Run a QA pass on the download and retention layer.

Check:

1. No page says the site gives approval.
2. Every saved/printed output has generated date and source snapshot.
3. LocalStorage has one namespace only: `brg_projects_v1`.
4. Export/import handles invalid JSON safely.
5. Print styles remove navigation and keep warning panels visible.
6. Download CTAs do not block users with email capture.
7. Cross-site UKPlanningGuide links open only where planning overlap exists.
8. Higher-risk-building warnings are visible where flats/common parts/HRB risks appear.
9. Part L/F content has version warning.
10. Lighthouse/accessibility basics pass: labelled buttons, no colour-only warnings, keyboard focus visible.
