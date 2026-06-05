export function routeToSearchRecord(route) {
  return {
    title: route.title,
    path: route.path,
    summary: route.summary || route.meta_description || '',
    family: route.family,
    intent: route.primary_intent || '',
    project: route.parent_project_slug || '',
    approvedDocument: route.parent_approved_document || '',
    source: route.primary_source_id || '',
    tokens: [route.title, route.summary, route.family, route.primary_intent, route.parent_project_slug, route.parent_approved_document]
      .filter(Boolean)
      .join(' ')
      .toLowerCase()
  };
}

export function buildSearchIndex(routes) {
  return routes
    .filter(route => route.indexable !== false && route.noindex !== true)
    .filter(route => route.title && route.path)
    .map(routeToSearchRecord);
}

export function simpleSearch(index, query, limit = 12) {
  const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
  return index
    .map(record => {
      const score = terms.reduce((sum, term) => sum + (record.tokens.includes(term) ? 1 : 0), 0);
      return { ...record, score };
    })
    .filter(record => record.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);
}
