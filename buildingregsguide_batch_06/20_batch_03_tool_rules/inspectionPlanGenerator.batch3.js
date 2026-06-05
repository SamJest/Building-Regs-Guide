/**
 * Generates homeowner-friendly inspection plans.
 * Codex should wire this into /tools/inspection-stage-checklist-generator/.
 */

export function generateInspectionPlan(project, extraFlags = {}) {
  const base = project.inspections || [];
  const extras = [];

  if (extraFlags.drains) extras.push('drainage layout and test before cover');
  if (extraFlags.structural_steel) extras.push('beam bearing, padstones and fire protection before boxing in');
  if (extraFlags.insulation) extras.push('insulation continuity and thermal bridge check before plasterboard');
  if (extraFlags.electrics) extras.push('electrical testing and certificate before completion');
  if (extraFlags.fire_safety) extras.push('fire stopping, alarms and fire doors before final sign-off');

  return [...new Set([...base, ...extras])].map((stage, index) => ({
    order: index + 1,
    stage,
    homeowner_action: 'Do not cover this work until the agreed inspection/evidence has been recorded.',
    evidence_to_keep: ['photos', 'installer details', 'product/specification records', 'inspection notes']
  }));
}
