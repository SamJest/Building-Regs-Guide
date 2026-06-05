# Internal linking strategy

Batch 5 adds 878 proposed internal link edges.

## Priority link paths

1. Homepage -> major hubs -> core project pages.
2. Project pages -> tools/downloads/Approved Documents.
3. Approved Document hubs -> relevant project pages.
4. Question pages -> parent project page -> tool/download.
5. Evidence pages -> completion certificate checker -> evidence folder download -> dashboard save.

## Link quality rules

- Links must solve the next user question, not just move PageRank.
- Cross-site links to UKPlanningGuide should be limited to planning/permitted-development topics.
- BuildingRegsGuide should own building control, inspections, completion evidence, competent person schemes, certificates and Approved Documents.
- Avoid repetitive exact-match anchors. Use natural but descriptive anchors.

## Build note

Codex should use `internal_link_graph_v5.json` as a recommended graph, then let page components render contextual cards, related project links and next-step CTAs.
