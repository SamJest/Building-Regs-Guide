
// BuildingRegsGuide Batch 4 prototype: tailored download recommendations.

export const DOWNLOAD_RECOMMENDATIONS = {
  extension: [
    'extension-building-control-prep-pack',
    'foundation-inspection-prep-sheet',
    'drainage-inspection-prep-sheet',
    'insulation-before-cover-up-checklist',
    'completion-certificate-evidence-folder'
  ],
  loft_conversion: [
    'loft-conversion-fire-and-structure-checklist',
    'fire-safety-before-completion-checklist',
    'approved-document-b-fire-safety-homeowner-pack',
    'completion-certificate-evidence-folder'
  ],
  garage_conversion: [
    'garage-conversion-building-regs-pack',
    'approved-document-f-ventilation-homeowner-pack',
    'approved-document-l-energy-homeowner-pack',
    'completion-certificate-evidence-folder'
  ],
  structural_alteration: [
    'load-bearing-wall-removal-evidence-checklist',
    'approved-document-a-structure-homeowner-pack',
    'structural-calculation-record-sheet',
    'inspection-stage-checklist'
  ],
  bathroom: [
    'new-bathroom-and-ensuite-regs-checklist',
    'drainage-inspection-prep-sheet',
    'electrician-part-p-certificate-request',
    'competent-person-certificate-tracker'
  ],
  windows_doors: [
    'windows-and-doors-certificate-checklist',
    'approved-document-l-energy-homeowner-pack',
    'approved-document-p-electrical-homeowner-pack',
    'competent-person-certificate-tracker'
  ],
  heat_pump: [
    'heat-pump-installation-paperwork-checklist',
    'energy-and-ventilation-evidence-folder',
    'registered-installer-confirmation-form',
    'competent-person-certificate-tracker'
  ],
  default: [
    'building-regs-before-you-start-checklist',
    'building-control-route-decision-sheet',
    'inspection-stage-checklist',
    'completion-certificate-evidence-folder'
  ]
};

export function getDownloadRecommendations(projectType, flags = {}) {
  const base = DOWNLOAD_RECOMMENDATIONS[projectType] || DOWNLOAD_RECOMMENDATIONS.default;
  const extra = [];
  if (flags.includesElectricalWork) extra.push('electrician-part-p-certificate-request');
  if (flags.includesCompetentPersonWork) extra.push('competent-person-certificate-tracker');
  if (flags.includesStructuralWork) extra.push('structural-calculation-record-sheet');
  if (flags.includesPartLOrF) extra.push('energy-and-ventilation-evidence-folder');
  if (flags.sellingOrRetrospective) extra.push('regularisation-evidence-gatherer');
  return [...new Set([...base, ...extra])];
}

export function makePrintablePackManifest({ projectType, projectLabel, flags }) {
  return {
    generated_at: new Date().toISOString(),
    source_snapshot_id: 'official_source_snapshot_2026-06-04',
    project_type: projectType,
    project_label: projectLabel,
    recommended_downloads: getDownloadRecommendations(projectType, flags),
    warnings: [
      'This pack is a preparation aid, not approval.',
      'Check the latest official source and your building control body before relying on it.',
      'Planning permission may also be needed.',
      'Higher-risk buildings, flats and common parts may need specialist routing.'
    ]
  };
}
