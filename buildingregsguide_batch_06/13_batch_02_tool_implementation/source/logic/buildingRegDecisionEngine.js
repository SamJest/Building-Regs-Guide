// BuildingRegsGuide batch 2 decision engine.
// Conservative static-site helper. It routes users; it must not claim to give legal/professional approval.

export const OUTCOMES = {
  BSR_ROUTE: 'bsr_route',
  LIKELY_BUILDING_CONTROL: 'likely_building_control_needed',
  COMPETENT_PERSON: 'competent_person_route_possible',
  MAYBE_EXEMPT: 'may_be_exempt_or_minor',
  REGULARISATION: 'regularisation_or_evidence_problem'
};

export function normaliseAnswers(answers = {}) {
  return {
    projectType: answers.projectType || 'unknown',
    isHigherRisk: Boolean(answers.isHigherRisk),
    alreadyStarted: Boolean(answers.alreadyStarted),
    alreadyFinished: Boolean(answers.alreadyFinished),
    usesRegisteredInstaller: Boolean(answers.usesRegisteredInstaller),
    affectsStructure: Boolean(answers.affectsStructure),
    affectsFireSafety: Boolean(answers.affectsFireSafety),
    affectsDrainage: Boolean(answers.affectsDrainage),
    affectsElectrics: Boolean(answers.affectsElectrics),
    affectsHeating: Boolean(answers.affectsHeating),
    affectsWindowsDoors: Boolean(answers.affectsWindowsDoors),
    affectsInsulation: Boolean(answers.affectsInsulation),
    createsHabitableRoom: Boolean(answers.createsHabitableRoom),
    includesSleepingAccommodation: Boolean(answers.includesSleepingAccommodation),
    listedOrConservationOrFlat: Boolean(answers.listedOrConservationOrFlat)
  };
}

export function routeBuildingControl(answers = {}, projectMatrix = []) {
  const a = normaliseAnswers(answers);
  const project = projectMatrix.find(p => p.project_id === a.projectType) || null;
  const reasons = [];
  const warnings = [];
  const nextSteps = [];

  if (a.isHigherRisk) {
    reasons.push('The building may fall within the higher-risk building route.');
    warnings.push('Do not rely on normal domestic building-control routing until higher-risk status is resolved.');
    nextSteps.push('Read BSR higher-risk building control approval guidance.');
    return buildResult(OUTCOMES.BSR_ROUTE, project, reasons, warnings, nextSteps);
  }

  if (a.alreadyFinished || a.alreadyStarted) {
    reasons.push(a.alreadyFinished ? 'The work appears to be complete or substantially complete.' : 'The work appears to have already started.');
    warnings.push('Normal pre-start application routes may not be available for work that has already started.');
    nextSteps.push('Gather photos, invoices, certificates, drawings and structural evidence.');
    nextSteps.push('Contact local authority building control about regularisation/evidence recovery.');
    return buildResult(OUTCOMES.REGULARISATION, project, reasons, warnings, nextSteps);
  }

  const competentRoute = a.usesRegisteredInstaller && (a.affectsWindowsDoors || a.affectsElectrics || a.affectsHeating);
  const controlledWork = a.affectsStructure || a.affectsFireSafety || a.affectsDrainage || a.affectsElectrics || a.affectsHeating || a.affectsWindowsDoors || a.affectsInsulation || a.createsHabitableRoom || a.includesSleepingAccommodation;

  if (competentRoute && !a.affectsStructure && !a.affectsDrainage && !a.createsHabitableRoom && !a.includesSleepingAccommodation) {
    reasons.push('A registered installer/competent person route may cover the notifiable work.');
    nextSteps.push('Check the installer is registered for the exact type of work.');
    nextSteps.push('Keep the building regulations compliance certificate.');
    if (a.listedOrConservationOrFlat) warnings.push('Separate planning, listed building, leaseholder or freeholder consent may still be needed.');
    return buildResult(OUTCOMES.COMPETENT_PERSON, project, reasons, warnings, nextSteps);
  }

  if (controlledWork || (project && project.needs_regs_default.startsWith('yes'))) {
    reasons.push('The project affects controlled building work or evidence-sensitive areas.');
    if (project) reasons.push(`Project default: ${project.needs_regs_default}.`);
    nextSteps.push('Use the evidence checklist before contacting building control.');
    nextSteps.push('Consider full plans where structural, fire, drainage or complex energy details are involved.');
    if (a.listedOrConservationOrFlat) warnings.push('Planning/listed/freeholder/lease restrictions are separate from building regulations.');
    return buildResult(OUTCOMES.LIKELY_BUILDING_CONTROL, project, reasons, warnings, nextSteps);
  }

  reasons.push('The answers do not show an obvious controlled-work trigger.');
  warnings.push('Minor work can still be caught if it forms part of a wider project or affects controlled services.');
  nextSteps.push('Keep product/installer evidence and check with building control if unsure.');
  return buildResult(OUTCOMES.MAYBE_EXEMPT, project, reasons, warnings, nextSteps);
}

function buildResult(outcome, project, reasons, warnings, nextSteps) {
  return {
    outcome,
    project: project ? { project_id: project.project_id, project: project.project } : null,
    reasons,
    warnings,
    nextSteps,
    approvedDocuments: project ? project.approved_documents : [],
    evidence: project ? project.evidence : [],
    inspectionStages: project ? project.inspection_stages : [],
    redFlags: project ? project.red_flags : []
  };
}

export function chooseFullPlansVsBuildingNotice(answers = {}) {
  const a = normaliseAnswers(answers);
  const reasons = [];
  if (a.isHigherRisk) return { recommendation: 'Do not use this normal domestic comparison. Check BSR route.', confidence: 'high', reasons: ['Higher-risk building flag selected.'] };
  if (a.affectsStructure) reasons.push('Structural work benefits from checked drawings/calculations before work progresses.');
  if (a.affectsFireSafety) reasons.push('Fire-safety implications make pre-checking safer.');
  if (a.affectsDrainage) reasons.push('Drainage routes and build-over risks are easier to resolve before site work.');
  if (a.createsHabitableRoom || a.includesSleepingAccommodation) reasons.push('New habitable/sleeping accommodation increases evidence and safety needs.');
  if (reasons.length >= 2) return { recommendation: 'Full plans strongly preferred', confidence: 'medium-high', reasons };
  if (reasons.length === 1) return { recommendation: 'Full plans usually safer, building notice may be possible for simple domestic work', confidence: 'medium', reasons };
  return { recommendation: 'Building notice may be possible if the work is simple and allowed locally', confidence: 'low-medium', reasons: ['No major complexity flags selected.'] };
}
