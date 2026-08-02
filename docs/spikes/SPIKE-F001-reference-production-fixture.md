# SPIKE-F001: Representative Multi-Character Production Fixture

**Tracker:** `RGT-S003`

**Status:** Queued. Do not execute until the v1 documentation baseline is approved and competitive research has identified the production risks the fixture must expose.

## Question

What versioned, legally redistributable fixture set can evaluate RigTale's character orchestration, rendering, quality, recovery, editability, and full-production behavior without favoring one engine or rig representation?

## Why This Requires a Spike

A convenient demo scene can make weak architectures look successful. The test fixture must expose multi-character continuity, motion conflicts, role-based interaction, draw-order changes, repetition, cache invalidation, and operational recovery. It must also provide objective expected results without copying a protected cast or visual identity.

## Preconditions

- The v1 charter and documentation baseline are approved for evidence work.
- `SPIKE-C001` has identified relevant production patterns and common failure modes.
- `SPIKE-W001` has established target-user workflow, gate, and value evidence.
- Reference assets may be created, commissioned, or adapted only from sources with compatible, documented licenses.

## Fixture Structure

The fixture suite must contain three layers.

### Contract fixtures

Small valid and invalid artifacts covering schema versions, dependencies, capabilities, licenses, time boundaries, migrations, stale references, and structured errors.

### Diagnostic shots

Short shots that isolate one difficult behavior at a time:

- hierarchical biped motion and deformation;
- quadruped locomotion and ground contact;
- vehicle motion, wheel or component cycles, and character attachment;
- concurrent locomotion, upper-body action, expression, gaze, viseme, and prop tracks;
- three-character synchronized choreography;
- a role-based two-character interaction with a visible contact frame;
- character-prop handoff or attachment;
- masks, occlusion, draw-order changes, foreground and background layers;
- camera movement, parallax, safe-area boundaries, and aspect-ratio framing;
- unsupported action, motion conflict, missing asset, and incompatible-version failures;
- exact frame addressing, interrupted execution, and isolated rerendering.

### Complete reference production

A 150–210 second, multi-shot 2D cutout production exercising:

- at least three simultaneous character instances;
- reusable biped, quadruped, vehicle, prop, and environment packs;
- repeated sections with controlled variation;
- solo action, group choreography, interaction, reaction, expression, and camera changes;
- synchronized media and timing where the selected story requires them;
- continuity across shot boundaries;
- one structured correction that should invalidate only a known subset of output; and
- final assembly, captions, manifests, QC, export, restore, and rerender.

The subject, script, and visual design must be original or safely licensed. Similar production constraints may be studied, but the fixture must not imitate protected characters, music, artwork, or branding.

## Fixture-Neutrality Rules

- Expected behavior is described in production semantics and visible assertions before engine adapters are written.
- Source assets retain an engine-neutral master where practical.
- Backend-specific conversion is generated and versioned as derived evidence.
- The fixture cannot require a feature merely because one preferred engine exposes it.
- A candidate may document an unsupported assertion; the fixture must not be weakened to make every candidate pass.
- Short diagnostic output cannot replace complete-duration evidence.

## Expected Evidence

Each case must provide the applicable subset of:

- source artifacts and exact licenses;
- intended semantic action and required capability;
- approved reference pose, composition, contact frame, or sequence;
- frame and time ranges;
- measurable tolerances where evidence exists;
- expected success or structured failure;
- dependency and invalidation expectations;
- render and environment profile; and
- review rubric and approval record.

Thresholds that cannot be justified before execution remain explicitly evidence-pending and are calibrated without rewriting the intended visible behavior.

## Method

1. Derive a risk catalogue from the charter, v1 requirements, quality system, competitive research, and repository reviews.
2. Map each material risk to at least one isolated fixture assertion.
3. Design an original production brief and cast sufficient to exercise the required archetypes.
4. Record provenance and license compatibility before asset work begins.
5. Produce engine-neutral source assets, expected references, semantic descriptions, and invalid cases.
6. Review the fixture for accidental backend bias and missing full-duration risks.
7. Version and publish the fixture manifest before orchestration or renderer experiments.
8. Amend the fixture only through a reviewed version with an explanation of affected results.

## Required Outputs

- Fixture risk-to-requirement matrix.
- Versioned contract and failure corpus.
- Versioned diagnostic-shot manifests and expected evidence.
- Versioned complete-production brief, source assets, timeline, and acceptance rubric.
- Asset provenance, license, attribution, and redistribution report.
- Fixture authoring and execution instructions.
- Quality, recovery, cache-invalidation, and human-rubric calibration plan.
- A decision record approving the fixture version used for comparative spikes.
- Updates to product requirements, quality rules, and downstream spike preconditions.

## Exit Criteria

- Every charter reference-production constraint maps to fixture evidence.
- Every `SPIKE-A001` and `SPIKE-R001` material measurement has an input case.
- The fixture exposes multi-character, interaction, continuity, repetition, recovery, and isolated-rerender behavior.
- All redistributable artifacts have verified provenance and compatible licenses.
- Expected outcomes are defined before candidate adapter work.
- The Project Owner approves the fixture without selecting a renderer or orchestration architecture.

## Stop Conditions

- Stop if required assets lack provable redistribution rights.
- Stop if expected results can be satisfied only through one candidate's private representation.
- Stop and revise the fixture if a material production risk has no observable assertion.
