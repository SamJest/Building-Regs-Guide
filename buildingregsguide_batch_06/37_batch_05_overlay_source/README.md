# Batch 5 overlay source

These JavaScript modules are implementation starters for Codex. They are framework-neutral and can be adapted into the existing site build.

Suggested integration:

- `schemaFactory.js` -> `src/lib/seo/schemaFactory.js`
- `breadcrumbRules.js` -> `src/lib/seo/breadcrumbs.js`
- `relatedContentEngine.js` -> `src/lib/links/relatedContentEngine.js`
- `sitemapGenerator.js` -> `scripts/generate-sitemap.js`
- validation modules -> `scripts/validate-build/`
- `searchIndexBuilder.js` -> `scripts/build-search-index.js`

Do not expose source registry internals in user-facing pages except as human-readable official source blocks.
