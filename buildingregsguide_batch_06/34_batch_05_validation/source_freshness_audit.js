const VERSION_SENSITIVE_PATTERNS = [
  { pattern: /approved document l|part l|energy efficiency|conservation of fuel/i, requiredSource: 'govuk_approved_document_l_2026' },
  { pattern: /approved document f|part f|ventilation/i, requiredSource: 'govuk_future_homes_buildings_circular_01_2026' },
  { pattern: /higher-risk|higher risk|18 metres|7 storeys|building safety regulator|bsr/i, requiredSource: 'govuk_higher_risk_building_control_approval' },
  { pattern: /competent person scheme|self-certify|registered installer/i, requiredSource: 'govuk_building_regs_approval' }
];

export function auditSourceFreshness(route, contentText = '') {
  const text = `${route.title || ''} ${route.summary || ''} ${contentText}`;
  const sourceIds = [route.primary_source_id, route.secondary_source_ids].filter(Boolean).join(';');
  const warnings = [];
  for (const rule of VERSION_SENSITIVE_PATTERNS) {
    if (rule.pattern.test(text) && !sourceIds.includes(rule.requiredSource)) {
      warnings.push(`Route may need source ${rule.requiredSource}`);
    }
  }
  return { path: route.path, warnings, ok: warnings.length === 0 };
}
