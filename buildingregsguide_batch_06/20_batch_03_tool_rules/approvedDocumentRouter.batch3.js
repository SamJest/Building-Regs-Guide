/**
 * BuildingRegsGuide Batch 3 approved-document router.
 * Data-driven starter module for Codex. Replace imports with project data path.
 */

export function routeApprovedDocuments(input, rules) {
  const warnings = [];
  const projectId = input.project_id;
  const parts = new Set(rules.project_to_parts?.[projectId] || []);

  if (input.structural_change) parts.add('A');
  if (input.affects_escape || input.loft_conversion || input.flat_work) parts.add('B');
  if (input.new_wet_room || input.kitchen_or_bathroom) { parts.add('F'); parts.add('G'); parts.add('H'); }
  if (input.new_electrical_circuit || input.consumer_unit || input.outdoor_power) parts.add('P');
  if (input.heating_or_combustion) { parts.add('J'); parts.add('L'); }
  if (input.new_or_replacement_windows_doors) { parts.add('L'); parts.add('K'); parts.add('F'); }
  if (input.new_dwelling) { ['A','B','C','E','F','G','H','K','L','M','O','P','Q','R','S'].forEach(p => parts.add(p)); }
  if (input.ev_charging || input.new_parking_with_dwelling) parts.add('S');
  if (input.overheating_risk || input.large_solar_gain) parts.add('O');

  if (input.jurisdiction && input.jurisdiction !== 'England') {
    warnings.push({type:'jurisdiction', message:'This router is England-first. Show Wales/Scotland/NI handoff.'});
  }
  if (input.higher_risk_building) {
    warnings.push({type:'bsr', message:'Potential HRB: route to Building Safety Regulator guidance.'});
  }
  if (input.planning_unknown) {
    warnings.push({type:'planning_overlap', message:'Planning permission is separate. Cross-link to UKPlanningGuide.'});
  }

  const sorted = Array.from(parts).sort((a,b) => {
    const order = ['A','B','C','D','E','F','G','H','J','K','L','M','O','P','Q','R','S','T','7'];
    return order.indexOf(a) - order.indexOf(b);
  });

  return {
    project_id: projectId,
    approved_documents: sorted,
    evidence: sorted.flatMap(p => rules.part_to_evidence?.[p] || []),
    red_flags: sorted.flatMap(p => rules.part_to_red_flags?.[p] || []),
    warnings,
    disclaimer: 'This is a route-finding tool, not design approval. Confirm with building control or a competent professional.'
  };
}
