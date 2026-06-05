
// BuildingRegsGuide Batch 4 prototype: inspection timeline generator.

const STAGES = {
  pre_start: { label: 'Before work starts', evidence: ['approval route selected', 'drawings/specification', 'builder/installer details'] },
  excavation: { label: 'Excavation/foundation inspection', evidence: ['excavation photos', 'depth/ground notes', 'nearby drains noted'] },
  drainage: { label: 'Drainage inspection', evidence: ['pipe route photos', 'falls/connection notes', 'test/inspection record'] },
  structure: { label: 'Structural work inspection', evidence: ['engineer calculations', 'beam/lintel photos', 'fixing details'] },
  fire_safety: { label: 'Fire safety before completion', evidence: ['alarm specification', 'fire door/fire stopping photos', 'escape route notes'] },
  insulation: { label: 'Insulation before cover-up', evidence: ['insulation product/spec', 'photos before plasterboard', 'thermal bridge notes'] },
  ventilation: { label: 'Ventilation/commissioning', evidence: ['extract fan details', 'commissioning records', 'background ventilation notes'] },
  electrics: { label: 'Electrical certification', evidence: ['installer details', 'EIC/minor works certificate', 'Part P/building regs compliance certificate if relevant'] },
  final: { label: 'Final completion', evidence: ['completion certificate', 'competent person certificates', 'warranties and commissioning records'] }
};

const PROJECT_STAGE_MAP = {
  extension: ['pre_start', 'excavation', 'drainage', 'structure', 'insulation', 'ventilation', 'electrics', 'final'],
  loft_conversion: ['pre_start', 'structure', 'fire_safety', 'insulation', 'ventilation', 'electrics', 'final'],
  garage_conversion: ['pre_start', 'structure', 'fire_safety', 'insulation', 'ventilation', 'electrics', 'final'],
  structural_alteration: ['pre_start', 'structure', 'fire_safety', 'final'],
  bathroom: ['pre_start', 'drainage', 'ventilation', 'electrics', 'final'],
  heat_pump: ['pre_start', 'ventilation', 'electrics', 'final'],
  windows_doors: ['pre_start', 'fire_safety', 'insulation', 'final'],
  default: ['pre_start', 'structure', 'insulation', 'ventilation', 'final']
};

export function buildInspectionTimeline(projectType, options = {}) {
  const ids = PROJECT_STAGE_MAP[projectType] || PROJECT_STAGE_MAP.default;
  const stages = ids.map((id, index) => ({
    stage_id: id,
    order: index + 1,
    status: 'not_started',
    ...STAGES[id]
  }));

  if (options.includesPublicSewer && !stages.find(s => s.stage_id === 'drainage')) {
    stages.splice(1, 0, { stage_id: 'drainage', order: 2, status: 'not_started', ...STAGES.drainage });
  }

  if (options.includesElectricalWork && !stages.find(s => s.stage_id === 'electrics')) {
    stages.splice(stages.length - 1, 0, { stage_id: 'electrics', order: stages.length, status: 'not_started', ...STAGES.electrics });
  }

  return stages.map((stage, index) => ({ ...stage, order: index + 1 }));
}
