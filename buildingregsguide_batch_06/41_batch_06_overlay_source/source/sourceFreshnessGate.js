const HIGH_SENSITIVITY = new Set(['approved_document', 'higher_risk_building', 'energy', 'ventilation', 'fire_safety', 'structural']);

export function sourceFreshnessGate(sourceRecord, pageSensitivity = 'general') {
  const failures = [];
  if (!sourceRecord?.url) failures.push('missing_url');
  if (!sourceRecord?.checked_date) failures.push('missing_checked_date');
  if (!sourceRecord?.name) failures.push('missing_source_name');
  if (!sourceRecord?.key_points_for_site?.length) failures.push('missing_key_points');

  if (HIGH_SENSITIVITY.has(pageSensitivity)) {
    if (!sourceRecord?.codex_handling) failures.push('missing_codex_handling');
    if (!sourceRecord?.checked_date?.startsWith('2026-')) failures.push('sensitive_source_not_recently_checked');
  }
  return { pass: failures.length === 0, failures };
}
