# Schema implementation notes

## Use schema to clarify, not exaggerate

Use `WebPage` and `Article` for guidance pages, `BreadcrumbList` for all indexable routes, `FAQPage` only when the page contains visible genuine Q&A content, and `SoftwareApplication` for interactive tools.

Do not use `HowTo` for legal/compliance routes unless the page contains a true step-by-step task the user can complete safely without professional judgement. Most building regulations pages should not be marked as `HowTo`.

## Required fields

Every indexable page needs:

- canonical URL
- title
- meta description
- breadcrumb trail
- date modified
- source IDs rendered visibly in page content

## Validation

Codex should run `schema_smoke_tests.js` to verify JSON-LD parses, has no unresolved placeholders, and uses only allowed schema types for the page family.
