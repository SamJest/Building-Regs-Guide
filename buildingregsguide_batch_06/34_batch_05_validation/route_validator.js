export function validateRoute(route) {
  const errors = [];
  const warnings = [];
  if (!route.title) errors.push('Missing title');
  if (!route.path || !route.path.startsWith('/')) errors.push('Path must start with /');
  if (route.path && !route.path.endsWith('/')) warnings.push('Path should use trailing slash');
  if (!route.family) errors.push('Missing family');
  if (!route.meta_description && !route.summary) warnings.push('Missing meta description/summary');
  if (route.needs_official_source_block && !route.primary_source_id) errors.push('Needs official source block but has no primary_source_id');
  if ((route.path || '').includes('?')) errors.push('Canonical route must not contain query string');
  if ((route.title || '').length > 70) warnings.push('Title may be long for meta/title rendering');
  if ((route.meta_description || '').length > 160) warnings.push('Meta description is longer than 160 chars');
  return { path: route.path, valid: errors.length === 0, errors, warnings };
}

export function validateRoutes(routes) {
  return routes.map(validateRoute);
}

export function failOnInvalidRoutes(routes) {
  const results = validateRoutes(routes);
  const failed = results.filter(r => !r.valid);
  if (failed.length) {
    throw new Error(`Invalid routes: ${failed.map(f => `${f.path}: ${f.errors.join(', ')}`).join(' | ')}`);
  }
  return results;
}
