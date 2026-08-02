# SPIKE-A002: Layered-Asset Ingestion and Rig Publication

**Tracker:** `RGT-S010`

**Status:** Queued. Execute only after the fixture source artwork and candidate asset systems are identified.

## Question

Which asset-ingestion and rig-publication workflow can turn user-supplied layered 2D artwork into versioned, capability-declared character, prop, vehicle, and scene packs at acceptable visual quality and authoring effort?

## Why This Requires Evidence

Animation quality depends on pivots, layer structure, deformation, masks, draw order, expressions, anchors, motion compatibility, and publication discipline. Declaring an import format does not prove that creators can prepare assets reliably or that different runtimes preserve the intended look.

## Preconditions

- `SPIKE-C001` has screened relevant authoring tools, formats, and runtimes.
- `SPIKE-F001` has approved source artwork, archetype requirements, provenance, and expected visual tests.
- No candidate renderer or rig representation is treated as selected.

## Approaches to Compare

1. Import a documented layered artwork format, then map layers, pivots, masks, and rig bindings in RigTale metadata.
2. Import a published rig from an existing authoring ecosystem through a versioned adapter.
3. Use assisted layer, pivot, and anchor proposals followed by deterministic validation and human approval.

Prepared reference packs may bootstrap experiments, but the spike must measure the workflow that a real uploaded asset would follow.

## Required Cases

- biped with facial and mouth variants;
- quadruped with locomotion-critical contacts;
- vehicle with character and prop attachments;
- layered scene with foreground, background, masks, and parallax metadata;
- asset version change affecting a known set of shots;
- malformed, flattened, ambiguous, incompatible, and unlicensed inputs; and
- backend-specific derived conversion that remains traceable to the published source pack.

## Method

1. Inspect official format specifications and exact source implementations for qualified candidates.
2. Import the same approved source assets through each viable workflow.
3. Measure manual layer mapping, pivot placement, binding, expression, anchor, capability, and correction work.
4. Run deformation, attachment, draw-order, mask, expression, and motion-compatibility fixtures.
5. Publish a version, revise one source asset, publish a new version, and verify dependency impact.
6. Test invalid files, unsafe archives, missing licenses, incompatible versions, and unsupported features.
7. Record visual differences introduced by conversion and whether preview/final backends require separate derived assets.
8. Review authoring usability with target practitioners where access permits.

## Measurements

- hands-on preparation and correction time by archetype;
- number and severity of manual decisions;
- deformation, pivot, mask, draw-order, expression, and attachment defects;
- round-trip or source-of-truth preservation;
- capability and compatibility accuracy;
- conversion determinism and version traceability;
- invalid-input diagnostic quality;
- packaging, licensing, and redistribution constraints; and
- importer, authoring, and migration maintenance burden.

## Required Outputs

- Exact source revisions, formats, commands, imported artifacts, and visual evidence.
- Recommended source-of-truth and publication workflow or reason to defer.
- Proposed `CharacterPack`, `ScenePack`, `PropPack`, `MotionPack`, capability, and derived-conversion revisions.
- Minimum required manual authoring versus safe assisted proposals.
- Import, publication, compatibility, security, and migration failure catalogue.
- Updates to product requirements, contracts, pipeline, quality, operations, fixture, and implementation plan.
- Decision records for accepted source format, rig representation, or authoring integration.

## Exit Criteria

- At least two viable ingestion or publication approaches are evaluated where evidence permits.
- Every required asset archetype completes the documented publish flow or has a reproduced blocker.
- Visual and capability tests pass without silently flattening editable structure.
- Version updates and affected-shot dependencies are traceable.
- Invalid and unsafe inputs fail with actionable diagnostics.
- The selected workflow is practical for a solo creator or small studio under measured preparation effort.
