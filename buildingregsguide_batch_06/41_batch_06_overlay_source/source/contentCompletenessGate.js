export function contentCompletenessGate(content) {
  const failures = [];
  const body = (content?.body || '').replace(/\s+/g, ' ').trim();
  if (body.length < 1200) failures.push('body_too_short');
  if (!content?.intro) failures.push('missing_intro');
  if (!content?.practicalSteps?.length) failures.push('missing_practical_steps');
  if (!content?.sourceIds?.length) failures.push('missing_source_ids');
  if (!content?.faqs?.length) failures.push('missing_faqs');
  if (!content?.relatedLinks?.length) failures.push('missing_related_links');
  if (content?.regulatory === true && !content?.sourceVersionPanel) failures.push('missing_source_version_panel');
  return { pass: failures.length === 0, failures };
}
