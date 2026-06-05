export function launchQualityGate(page) {
  const failures = [];
  if (!page) failures.push('missing_page_object');
  if (!page?.path) failures.push('missing_path');
  if (!page?.title || page.title.length < 20) failures.push('weak_title');
  if (!page?.metaDescription || page.metaDescription.length < 70) failures.push('weak_meta_description');
  if (!Array.isArray(page?.sources) || page.sources.length === 0) failures.push('missing_sources');
  if (page?.regulatory === true && !page?.sourcePanel) failures.push('missing_source_panel');
  if (!page?.bodyText || page.bodyText.replace(/\s+/g, ' ').trim().length < 1200) failures.push('thin_body_text');
  if (!Array.isArray(page?.internalLinks) || page.internalLinks.length < 3) failures.push('weak_internal_links');
  if (page?.publishState === 'index' && page?.noindex === true) failures.push('conflicting_index_state');
  if (page?.jurisdiction && /england/i.test(page.jurisdiction) === false && page?.usesEnglandOnlySource === true) failures.push('jurisdiction_source_mismatch');
  if (page?.higherRiskBuildingSignal === true && page?.normalHomeownerFlow === true) failures.push('hrb_normal_flow_not_allowed');
  return { pass: failures.length === 0, failures };
}
