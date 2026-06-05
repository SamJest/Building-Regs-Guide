# Prompt 08: Make tool results saveable and printable

Use the Batch 4 saveable result contract to upgrade existing tools.

Inputs:

- `25_batch_04_tool_extensions/saveable_tool_result_contract.md`
- `25_batch_04_tool_extensions/downloadPackGenerator.js`
- `25_batch_04_tool_extensions/inspectionTimelineEngine.js`
- existing Batch 2-3 tool specs and decision engines

Tasks:

1. Add a result object to each implemented tool.
2. Add recommended downloads to tool results.
3. Add source/version warnings.
4. Add print result button.
5. Add save result to existing or new project.
6. Add inspection timeline generation where relevant.

Acceptance criteria:

- Building control route checker can save a result.
- Approved Document router can save Part flags.
- Inspection-stage checklist generator can save timeline stages.
- Competent person checker can add certificate chaser items.
