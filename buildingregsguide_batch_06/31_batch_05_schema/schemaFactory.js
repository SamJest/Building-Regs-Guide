export const ALLOWED_SCHEMA_BY_FAMILY = {
  homepage: ['WebPage', 'BreadcrumbList'],
  project_deep_dive: ['Article', 'BreadcrumbList', 'FAQPage'],
  approved_document_hub: ['Article', 'BreadcrumbList', 'FAQPage'],
  approved_document_longtail: ['Article', 'BreadcrumbList'],
  programmatic_question_page: ['WebPage', 'BreadcrumbList', 'FAQPage'],
  download_landing_page: ['WebPage', 'BreadcrumbList'],
  comparison_page: ['Article', 'BreadcrumbList', 'FAQPage'],
  evidence_page: ['Article', 'BreadcrumbList', 'FAQPage'],
  tool: ['SoftwareApplication', 'WebPage', 'BreadcrumbList']
};

export function makeCanonical(path, domain = 'https://buildingregsguide.co.uk') {
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${domain}${cleanPath.endsWith('/') ? cleanPath : `${cleanPath}/`}`;
}

export function makeBreadcrumbSchema(items) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url
    }))
  };
}

export function makeWebPageSchema(route, options = {}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name: route.title,
    description: route.meta_description || route.summary,
    url: makeCanonical(route.path, options.domain),
    isPartOf: {
      '@type': 'WebSite',
      name: 'BuildingRegsGuide',
      url: options.domain || 'https://buildingregsguide.co.uk/'
    },
    inLanguage: 'en-GB',
    about: ['Building regulations', 'Building control', 'Home improvement']
  };
}

export function makeArticleSchema(route, options = {}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: route.title,
    description: route.meta_description || route.summary,
    mainEntityOfPage: makeCanonical(route.path, options.domain),
    author: { '@type': 'Organization', name: 'BuildingRegsGuide' },
    publisher: { '@type': 'Organization', name: 'BuildingRegsGuide' },
    dateModified: options.dateModified || new Date().toISOString().slice(0, 10),
    inLanguage: 'en-GB'
  };
}

export function makeFAQSchema(faqs) {
  if (!Array.isArray(faqs) || faqs.length < 2) return null;
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map(faq => ({
      '@type': 'Question',
      name: faq.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: faq.answer
      }
    }))
  };
}

export function makeToolSchema(route, options = {}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: route.title,
    applicationCategory: 'UtilitiesApplication',
    operatingSystem: 'Web',
    url: makeCanonical(route.path, options.domain),
    description: route.meta_description || route.summary,
    offers: { '@type': 'Offer', price: '0', priceCurrency: 'GBP' }
  };
}

export function schemasForRoute(route, options = {}) {
  const family = route.family || 'page';
  const crumbs = options.breadcrumbs || [
    { name: 'Home', url: makeCanonical('/', options.domain) },
    { name: route.title, url: makeCanonical(route.path, options.domain) }
  ];

  const schemas = [makeBreadcrumbSchema(crumbs)];
  if (family === 'tool') schemas.push(makeToolSchema(route, options));
  else if (['project_deep_dive', 'approved_document_hub', 'approved_document_longtail', 'comparison_page', 'evidence_page'].includes(family)) schemas.push(makeArticleSchema(route, options));
  else schemas.push(makeWebPageSchema(route, options));

  const faqSchema = makeFAQSchema(options.faqs || []);
  if (faqSchema) schemas.push(faqSchema);
  return schemas;
}

export function assertSchemaAllowed(route, schemas) {
  const allowed = ALLOWED_SCHEMA_BY_FAMILY[route.family] || ['WebPage', 'Article', 'BreadcrumbList', 'FAQPage'];
  const bad = schemas.filter(s => !allowed.includes(s['@type']));
  if (bad.length) {
    throw new Error(`Disallowed schema for ${route.path}: ${bad.map(s => s['@type']).join(', ')}`);
  }
  return true;
}
