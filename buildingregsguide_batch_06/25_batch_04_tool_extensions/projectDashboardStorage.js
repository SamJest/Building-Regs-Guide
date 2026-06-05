
// BuildingRegsGuide Batch 4 prototype
// No external dependencies. Codex can adapt this to the project framework.

export const BRG_STORAGE_KEY = 'brg_projects_v1';

export function loadProjects() {
  try {
    const raw = window.localStorage.getItem(BRG_STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch (error) {
    console.warn('Could not load BuildingRegsGuide projects', error);
    return [];
  }
}

export function saveProjects(projects) {
  window.localStorage.setItem(BRG_STORAGE_KEY, JSON.stringify(projects));
}

export function createProject({ projectType, projectLabel, jurisdiction = 'england', propertyType = 'unknown', sourceSnapshotId }) {
  const now = new Date().toISOString();
  const project = {
    schema_version: 1,
    project_id: crypto.randomUUID ? crypto.randomUUID() : `project_${Date.now()}`,
    created_at: now,
    updated_at: now,
    jurisdiction,
    project_type: projectType,
    project_label: projectLabel,
    property_type: propertyType,
    is_flat_or_common_parts: propertyType === 'flat' || propertyType === 'maisonette',
    is_higher_risk_possible: false,
    source_snapshot_id: sourceSnapshotId || 'official_source_snapshot_2026-06-04',
    saved_tool_results: [],
    downloads: [],
    inspection_stages: [],
    evidence_items: [],
    certificate_chaser: [],
    notes: []
  };
  const projects = loadProjects();
  projects.push(project);
  saveProjects(projects);
  return project;
}

export function updateProject(projectId, updater) {
  const projects = loadProjects();
  const next = projects.map(project => {
    if (project.project_id !== projectId) return project;
    const updated = updater({ ...project });
    return { ...updated, updated_at: new Date().toISOString() };
  });
  saveProjects(next);
  return next.find(project => project.project_id === projectId) || null;
}

export function saveToolResult(projectId, result) {
  return updateProject(projectId, project => {
    project.saved_tool_results = project.saved_tool_results || [];
    project.saved_tool_results.unshift({
      ...result,
      saved_at: new Date().toISOString(),
      source_snapshot_id: result.source_snapshot_id || project.source_snapshot_id
    });
    return project;
  });
}

export function addEvidenceItem(projectId, item) {
  return updateProject(projectId, project => {
    project.evidence_items = project.evidence_items || [];
    project.evidence_items.push({
      evidence_id: crypto.randomUUID ? crypto.randomUUID() : `evidence_${Date.now()}`,
      created_at: new Date().toISOString(),
      status: 'needed',
      ...item
    });
    return project;
  });
}

export function addCertificateChaserItem(projectId, item) {
  return updateProject(projectId, project => {
    project.certificate_chaser = project.certificate_chaser || [];
    project.certificate_chaser.push({
      certificate_id: crypto.randomUUID ? crypto.randomUUID() : `certificate_${Date.now()}`,
      created_at: new Date().toISOString(),
      status: 'expected',
      ...item
    });
    return project;
  });
}

export function exportProject(projectId) {
  const project = loadProjects().find(p => p.project_id === projectId);
  if (!project) return null;
  return JSON.stringify(project, null, 2);
}

export function importProject(jsonText) {
  const parsed = JSON.parse(jsonText);
  if (!parsed || !parsed.project_id || parsed.schema_version !== 1) {
    throw new Error('This does not look like a valid BuildingRegsGuide project export.');
  }
  const projects = loadProjects().filter(p => p.project_id !== parsed.project_id);
  projects.push({ ...parsed, imported_at: new Date().toISOString() });
  saveProjects(projects);
  return parsed;
}
