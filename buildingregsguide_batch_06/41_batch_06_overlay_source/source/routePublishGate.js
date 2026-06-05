export function routePublishGate(route) {
  const reasons = [];
  if (!route?.path?.startsWith('/')) reasons.push('path_must_start_with_slash');
  if (!route?.slug) reasons.push('missing_slug');
  if (!route?.family) reasons.push('missing_family');
  if (!route?.primary_source_id && route?.regulatory !== false) reasons.push('missing_primary_source_id');
  if (route?.candidate === true && route?.contentComplete !== true) reasons.push('candidate_not_content_complete');
  if (route?.indexable === true && route?.qualityGatePassed !== true) reasons.push('indexable_without_quality_gate');
  return { publishable: reasons.length === 0, reasons };
}
