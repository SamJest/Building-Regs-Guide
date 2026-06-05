# Building Control Route Checker

Path: `/tools/building-control-route-checker/`

## Purpose

Chooses likely next route: planning-first, full plans, building notice, competent person, regularisation, or specialist advice.

## Inputs

- jurisdiction: England / Wales / Scotland / not sure
- project type
- has work started?
- structural alteration?
- changes to drainage?
- new or altered electrics/heating/glazing?
- missing certificate or historic work?
- needs quick start or certainty before building?

## Result logic

1. If jurisdiction is Wales or Scotland, return source-aware jurisdiction result. Do not apply England route logic.
2. If higher-risk building, flats/high-rise or commercial complexity is detected, return specialist/BSR/building-control warning.
3. If work is already done and approval/certificates are missing, return regularisation/evidence result.
4. If work is covered by common competent person categories, return competent-person evidence result.
5. If complex structural/fire/drainage/loft/extension work, bias toward full plans or early building-control contact.
6. If smaller domestic alteration with low complexity, building notice may be a route to discuss.

## Outputs

- likely route, never definitive compliance
- why this route was selected
- checklist of evidence to gather
- official source links from registry
- related guide/download routes

## Validation

Tool must render at least 3 distinct result states and link to at least one official source in every state.
