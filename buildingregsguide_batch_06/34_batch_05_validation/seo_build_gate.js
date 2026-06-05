import { validateRoute } from './route_validator.js';
import { validateContentGuard } from './content_guard_validator.js';
import { smokeTestJsonLd } from './schema_smoke_tests.js';
import { auditSourceFreshness } from './source_freshness_audit.js';

export function evaluatePageForIndexing({ route, content, links = [], schemas = [] }) {
  const routeResult = validateRoute(route);
  const contentResult = validateContentGuard({ route, htmlOrMarkdown: content, links });
  const schemaResult = smokeTestJsonLd(schemas);
  const sourceResult = auditSourceFreshness(route, content);
  const errors = [
    ...routeResult.errors,
    ...contentResult.errors,
    ...schemaResult.errors
  ];
  const warnings = [
    ...routeResult.warnings,
    ...contentResult.warnings,
    ...sourceResult.warnings
  ];
  return {
    path: route.path,
    indexable: errors.length === 0,
    errors,
    warnings,
    recommendedRobots: errors.length ? 'noindex,follow' : 'index,follow'
  };
}
