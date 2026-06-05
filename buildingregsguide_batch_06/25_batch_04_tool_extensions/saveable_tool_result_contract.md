# Saveable tool result contract

Every tool result should be displayable, printable and saveable.

## Required result fields

```ts
export type ToolResult = {
  result_id: string;
  tool_id: string;
  tool_version: string;
  generated_at: string;
  source_snapshot_id: string;
  user_inputs_summary: Record<string, string | boolean | number | null>;
  risk_level: 'low' | 'medium' | 'high' | 'specialist';
  headline: string;
  plain_english_answer: string;
  likely_routes: string[];
  approved_document_flags: ApprovedDocumentFlag[];
  evidence_needed: EvidenceItem[];
  inspection_stages: InspectionStage[];
  warnings: string[];
  next_links: InternalLink[];
  download_recommendations: string[];
};
```

## UX buttons

- Save to my project.
- Print result.
- Download checklist.
- Re-run checker.
- Start a project dashboard.

## Result warnings

Every tool result must include:

- not approval,
- check official source,
- check building control body,
- planning permission may also be needed,
- HRB / flat / common parts escalation where relevant.
