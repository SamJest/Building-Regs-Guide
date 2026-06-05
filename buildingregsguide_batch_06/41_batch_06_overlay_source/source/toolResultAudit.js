export function toolResultAudit(result) {
  const failures = [];
  if (!result?.toolSlug) failures.push('missing_tool_slug');
  if (!result?.resultType) failures.push('missing_result_type');
  if (!result?.generatedAt) failures.push('missing_generated_date');
  if (!Array.isArray(result?.sources) || result.sources.length === 0) failures.push('missing_sources');
  if (!Array.isArray(result?.nextActions) || result.nextActions.length === 0) failures.push('missing_next_actions');
  if (!result?.warningCopy) failures.push('missing_warning_copy');
  if (/guaranteed|approved|complies/i.test(result?.summary || '')) failures.push('unsafe_certainty_wording');
  if (result?.higherRiskBuildingSignal === true && result?.resultType !== 'specialist_bsr_route') failures.push('hrb_must_stop_route');
  return { pass: failures.length === 0, failures };
}
