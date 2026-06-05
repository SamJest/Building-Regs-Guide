# Build validation contract for Codex

Codex should add a build step that reads the route registry, generated content registry, internal link graph and schema factory output.

## Required build behaviour

1. Validate every route.
2. Validate every rendered page for source blocks and risky certainty phrases.
3. Generate JSON-LD and smoke-test it.
4. Decide `index,follow` or `noindex,follow` per page.
5. Generate sitemap only from passing pages.
6. Fail the build for core pages with errors.
7. Allow candidate long-tail pages to remain generated as drafts/noindex when not ready.

## Suggested output

- `/dist/validation-report.json`
- `/dist/indexable-routes.json`
- `/dist/noindex-routes.json`
- `/dist/orphan-routes.json`
- `/dist/schema-errors.json`
