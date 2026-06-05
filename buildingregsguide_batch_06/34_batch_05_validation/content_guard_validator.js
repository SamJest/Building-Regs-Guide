const RISKY_CERTAINTY_PHRASES = [
  'definitely does not need approval',
  'never needs building regulations',
  'always exempt',
  'guaranteed approval',
  'approved automatically',
  'no need to check'
];

export function validateContentGuard({ route, htmlOrMarkdown, links = [] }) {
  const text = (htmlOrMarkdown || '').toLowerCase();
  const errors = [];
  const warnings = [];

  if (!text.includes('official source') && !text.includes('source:') && !text.includes('gov.uk')) {
    errors.push('Missing visible official source block');
  }
  for (const phrase of RISKY_CERTAINTY_PHRASES) {
    if (text.includes(phrase)) errors.push(`Unsafe certainty phrase: ${phrase}`);
  }
  if ((route.primary_source_id || '').includes('approved_document_l') || text.includes('part l') || text.includes('approved document l')) {
    if (!text.includes('version') && !text.includes('2026') && !text.includes('earlier versions')) {
      warnings.push('Part L content should carry a version/transitional warning');
    }
  }
  if (text.includes('higher-risk') || text.includes('higher risk') || text.includes('18 metres') || text.includes('7 storeys')) {
    if (!text.includes('building safety regulator') && !text.includes('bsr')) {
      errors.push('Higher-risk building content must mention BSR route');
    }
  }
  if (links.length < 5 && !['tool', 'homepage'].includes(route.family)) {
    warnings.push('Fewer than 5 internal links');
  }
  if (text.split(/\s+/).filter(Boolean).length < 550 && !['tool', 'homepage'].includes(route.family)) {
    warnings.push('Page may be too short or thin');
  }

  return { path: route.path, valid: errors.length === 0, errors, warnings };
}
