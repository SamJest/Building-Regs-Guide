# Prompt 10: implement schema, canonicals and breadcrumbs

Use the Batch 5 schema files to add canonical URLs, breadcrumbs and JSON-LD output across all page families.

Requirements:

- Normalize all canonical URLs to lowercase trailing-slash routes.
- Add breadcrumb UI and `BreadcrumbList` JSON-LD to every indexable page.
- Add `Article` schema to project, Approved Document, comparison and evidence pages.
- Add `SoftwareApplication` schema to tool pages.
- Add `FAQPage` schema only where visible FAQs exist.
- Add smoke tests so unresolved placeholders fail validation.
