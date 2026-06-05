export function getRelatedContent(currentPath, edges, options = {}) {
  const limit = options.limit || 8;
  const placement = options.placement || null;
  let matches = edges.filter(edge => edge.source_path === currentPath);
  if (placement) matches = matches.filter(edge => edge.placement === placement);
  return matches.slice(0, limit).map(edge => ({
    path: edge.target_path,
    title: edge.anchor,
    reason: edge.reason,
    placement: edge.placement
  }));
}

export function incomingLinkCount(path, edges) {
  return edges.filter(edge => edge.target_path === path).length;
}

export function outgoingLinkCount(path, edges) {
  return edges.filter(edge => edge.source_path === path).length;
}

export function detectOrphans(routes, edges) {
  const exempt = new Set(['/']);
  return routes.filter(route => !exempt.has(route.path) && incomingLinkCount(route.path, edges) === 0);
}

export function detectDeadEnds(routes, edges) {
  return routes.filter(route => route.indexable !== false && outgoingLinkCount(route.path, edges) < 3);
}
