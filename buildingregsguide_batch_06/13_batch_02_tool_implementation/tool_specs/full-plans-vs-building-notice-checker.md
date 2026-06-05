# Full Plans vs Building Notice Checker

## Purpose

Helps users choose safer application route based on complexity and evidence risk.

## Inputs

- projectType
- isHigherRisk
- alreadyStarted
- alreadyFinished
- usesRegisteredInstaller
- affectsStructure
- affectsFireSafety
- affectsDrainage
- affectsElectrics
- affectsHeating
- affectsWindowsDoors
- affectsInsulation
- createsHabitableRoom
- includesSleepingAccommodation
- listedOrConservationOrFlat

## Outputs

Use the shared tool result component contract. All outputs must be conservative and source-linked.

## Implementation

Import `routeBuildingControl`, `chooseFullPlansVsBuildingNotice` and `PROJECT_REQUIREMENT_MATRIX` from the Batch 2 overlay source. Use `routeBuildingControl()` for the main result and the project matrix for evidence/inspection lists.

## Copy guardrails

- Do not say the user definitely does or does not need approval unless the underlying official source is explicit.
- Do not calculate structural sizes or fire design.
- Do not let competent person results imply planning/listed/freeholder consent is irrelevant.
- Do not use the normal domestic route for higher-risk buildings.
