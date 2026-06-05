# Local storage contract for Codex

Use a single namespace:

`brg_projects_v1`

Do not spread unrelated keys across local storage.

## Suggested TypeScript model

```ts
export type BuildingRegsProject = {
  project_id: string;
  created_at: string;
  updated_at: string;
  jurisdiction: 'england' | 'wales' | 'scotland' | 'northern_ireland' | 'unknown';
  project_type: string;
  project_label: string;
  property_type?: 'house' | 'flat' | 'maisonette' | 'bungalow' | 'commercial' | 'mixed' | 'unknown';
  is_flat_or_common_parts?: boolean;
  is_higher_risk_possible?: boolean;
  source_snapshot_id: string;
  saved_tool_results: SavedToolResult[];
  downloads: SavedDownload[];
  inspection_stages: InspectionStage[];
  evidence_items: EvidenceItem[];
  certificate_chaser: CertificateItem[];
  notes: ProjectNote[];
};
```

## Versioning

Every saved object must include:

- `schema_version: 1`,
- `source_snapshot_id`,
- `generated_at`,
- `expires_recheck_at` where relevant.

## Export/import

Add two buttons:

- Export project JSON.
- Import project JSON.

This lets users keep their own copy without accounts.
