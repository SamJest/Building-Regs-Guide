# No-thin-page policy

Codex must treat route records as candidates, not automatic published pages.

## A page must stay draft/noindex when any of these are true

- It has fewer than 4 content blocks that are specific to its project, Approved Document, download, comparison or evidence topic.
- It only repeats GOV.UK wording without adding homeowner interpretation, checklists, examples or next-step routing.
- It has no visible source block.
- It lacks a parent hub and breadcrumb.
- It has fewer than 5 useful internal links.
- It makes certainty claims such as “you definitely do not need approval” without a strong official basis and a warning about project-specific checks.
- It covers Part L, Part F, higher-risk buildings or fire safety without version/route warnings.

## Preferred page structure

1. Short answer.
2. What usually triggers approval or extra checks.
3. Route options.
4. Documents/evidence.
5. Inspection/certificate issues.
6. Mistakes to avoid.
7. Tool/download/dashboard next step.
8. Official source block.

## Publishing gates

Use `34_batch_05_validation/content_guard_validator.js` and `34_batch_05_validation/route_validator.js`. Codex should fail the build or mark the route as `noindex` when a route fails the gates.
