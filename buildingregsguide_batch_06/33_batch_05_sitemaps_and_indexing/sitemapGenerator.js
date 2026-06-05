import fs from 'node:fs';

export function normaliseCanonical(path, domain = 'https://buildingregsguide.co.uk') {
  let p = path.split('?')[0].trim().toLowerCase();
  if (!p.startsWith('/')) p = `/${p}`;
  if (!p.endsWith('/')) p = `${p}/`;
  return `${domain}${p}`;
}

export function isIndexableRoute(route) {
  if (route.noindex === true) return false;
  if (!route.path || route.path.includes('?')) return false;
  if (route.path.startsWith('/print/') || route.path.startsWith('/api/')) return false;
  if ((route.batch_status || '').includes('draft') && !route.content_ready) return false;
  if (route.needs_official_source_block && !route.primary_source_id) return false;
  return true;
}

export function urlEntry(route, domain) {
  const priorityByFamily = {
    homepage: '1.0',
    project_deep_dive: '0.8',
    approved_document_hub: '0.8',
    tool: '0.8',
    comparison_page: '0.7',
    evidence_page: '0.7',
    download_landing_page: '0.6',
    programmatic_question_page: '0.5',
    approved_document_longtail: '0.5'
  };
  const changefreqByFamily = {
    homepage: 'weekly',
    tool: 'monthly',
    project_deep_dive: 'monthly',
    approved_document_hub: 'monthly',
    approved_document_longtail: 'monthly',
    download_landing_page: 'monthly',
    comparison_page: 'monthly',
    evidence_page: 'monthly',
    programmatic_question_page: 'monthly'
  };
  return `  <url>\n    <loc>${normaliseCanonical(route.path, domain)}</loc>\n    <changefreq>${changefreqByFamily[route.family] || 'monthly'}</changefreq>\n    <priority>${priorityByFamily[route.family] || '0.5'}</priority>\n  </url>`;
}

export function generateSitemap(routes, options = {}) {
  const domain = options.domain || 'https://buildingregsguide.co.uk';
  const entries = routes.filter(isIndexableRoute).map(route => urlEntry(route, domain)).join('\n');
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${entries}\n</urlset>\n`;
}

export function writeSitemap(routes, outPath, options = {}) {
  fs.writeFileSync(outPath, generateSitemap(routes, options), 'utf8');
}
