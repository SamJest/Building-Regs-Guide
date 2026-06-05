# Codex Batch 5 master prompt

You are implementing Batch 5 of the BuildingRegsGuide sister site to UKPlanningGuide.

The project already has Batch 1-4 assets in this pack. Batch 5 adds the SEO-scale layer. Your job is not to publish hundreds of thin pages. Your job is to add a safe, validated route generation system that can scale without damaging quality.

## Inputs to use

- `30_batch_05_seo_scale/seo_route_expansion_registry.json`
- `30_batch_05_seo_scale/route_registry_v5_candidate_combined.json`
- `30_batch_05_seo_scale/page_family_templates.json`
- `31_batch_05_schema/schemaFactory.js`
- `31_batch_05_schema/breadcrumbRules.js`
- `32_batch_05_internal_linking/internal_link_graph_v5.json`
- `32_batch_05_internal_linking/relatedContentEngine.js`
- `33_batch_05_sitemaps_and_indexing/sitemapGenerator.js`
- `34_batch_05_validation/*.js`
- `38_batch_05_search_and_discovery/searchIndexBuilder.js`

## Build tasks

1. Add canonical URL generation.
2. Add breadcrumb generation.
3. Add JSON-LD schema generation and smoke tests.
4. Add internal related-content cards from the link graph.
5. Add sitemap generation from indexable routes only.
6. Add route/content validation gates.
7. Add search index generation.
8. Keep candidate long-tail pages as draft/noindex until content passes validation.

## Publishing rules

- Core Batch 1-4 pages can be indexable if content exists and source blocks are present.
- Batch 5 comparison/evidence/download pages can be indexable once rendered with real unique blocks.
- Batch 5 question and Approved Document long-tail routes should be published in controlled waves after validation.
- Never generate location pages by swapping council names only.

## Required output

- Working build scripts.
- Validation report.
- Sitemap and robots output.
- Search index output.
- Documented route publication workflow.
- No broken internal links.
- No unsupported legal certainty wording.

## Current Batch 5 scale

- New candidate route records: 259
- Combined candidate route records: 393
- Internal link edges: 878
