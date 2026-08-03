# RigTale Quality System

**Status:** v1 draft.

## Purpose

RigTale treats quality as versioned production evidence rather than a final subjective inspection. Quality checks begin with creative intent and assets, continue through planning and compilation, and block delivery when deterministic, Red-Team, or human review finds an unresolved critical defect.

## Quality Dimensions

| Dimension | Examples |
|---|---|
| Structural | Schema, IDs, versions, dependencies, compatibility, stale artifacts. |
| Asset | Missing layers, broken bindings, deformation, pivots, anchors, capabilities. |
| Animation | Motion conflicts, foot sliding, contact drift, discontinuity, unsupported action. |
| Composition | Framing, safe areas, occlusion, draw order, masks, parallax, camera behavior. |
| Temporal | Shot boundaries, pacing, repetition, beats, dialogue, lip sync, duration. |
| Creative | Brief alignment, clarity, story progression, readable action, emotional intent. |
| Audience | Factual accuracy, educational clarity, safety, low-stimulation intent, accessibility. |
| Media | Missing frames, corrupt output, audio peaks, silence, captions, codec and profile. |
| Legal | Provenance, license compatibility, attribution, consent where applicable. |
| Operational | Determinism, performance, recovery, archive restore, clean installation. |

## Finding Model

Every finding records rule or rubric ID, severity, category, artifact version, shot or time range, evidence, expected behavior, actual behavior, suggested remediation, reviewer or validator version, disposition, and resolution artifact.

Severity levels:

- `blocking`: delivery or downstream publication cannot proceed.
- `major`: visible or operational defect requiring correction unless explicitly waived.
- `minor`: localized defect that does not invalidate the production but should be reviewed.
- `advisory`: improvement or uncertain automated observation.

Waivers require a reason, scope, user identity, expiration or version boundary, and audit event. Deterministic corruption, missing license, unsupported capability, and incomplete delivery cannot be waived for publication.

## Quality Gates

### Gate 1 — Creative intent

Checks audience, purpose, duration, factual source expectations, safety constraints, and success criteria before production planning.

### Gate 2 — Script and synchronized media

Checks script structure, factual claims, lyrics or narration, language, duration, audio integrity, timing alignment, and required approvals. Audio-specific rules apply only where the production uses synchronized audio.

### Gate 3 — Asset publication

Checks provenance, license, package schema, dependencies, rig and drawable integrity, expressions, anchors, capabilities, preview evidence, and supported renderer features.

### Gate 4 — Shot plan

Checks duration coverage, cast and asset existence, capabilities, continuity, action conflicts, interactions, camera and safe areas, repetition, and expected visual assertions.

### Gate 5 — Compilation

Checks deterministic output, exact timing, resolved dependencies, source mapping, motion conflicts, constraints, fallbacks, unsupported features, and cache identity.

### Gate 6 — Preview review

Checks visible motion, interaction contacts, gaze, expression, layer order, masks, framing, occlusion, camera, parallax, synchronization, pacing, and continuity across adjacent shots.

### Gate 7 — Final render and delivery

Checks frame completeness, corruption, duration, audio/video alignment, captions, delivery profiles, checksums, manifests, licenses, QC reports, and archive restoral.

## Validation Layers

### Deterministic validators

Run from contracts and measurable media. Their results must be reproducible from the same inputs and validator versions. Examples include schema validation, capability lookup, timing coverage, frame count, dependency digests, safe-area bounds, missing assets, media probing, and license completeness.

### Render-analysis validators

Analyze produced frames or motion telemetry for likely occlusion, clipping, contact drift, off-screen placement, visual discontinuity, frozen motion, or preview/final differences. Their thresholds require fixtures and may begin as advisory.

### Red-Team review

Independently evaluates meaning and visible outcome. The Red-Team Agent uses a versioned rubric and must attach evidence. It cannot approve its own authored changes.

### Human review

Owns creative approvals and final publication judgment. The human rubric uses a five-point scale for visual quality, educational or narrative clarity, pacing, synchronization, and repetition, with the charter-required average threshold and no blocking finding.

## Reference Fixtures

`docs/quality/fixture-risk-matrix.md` maps every material production risk to the fixture assertion that exposes it, and records the residual risks no fixture can assert. It is the input to the corpus below, not a summary of it.

The test corpus must include:

- valid and invalid production-contract examples;
- character packs for biped, quadruped, and vehicle behavior;
- motion conflicts and valid layered combinations;
- group choreography and role-based interaction with contact frames;
- mask, draw-order, parallax, camera, and safe-area cases;
- corrupted media, missing frames, bad timing, stale dependencies, and incompatible versions;
- interrupted jobs and restorable archives;
- approved golden frames or short sequences for visual comparison; and
- the complete 150–210 second reference production for repetition, continuity, performance, and recovery.

Golden media is versioned with the engine, renderer profile, platform tolerance, and approval record. Pixel identity may be inappropriate across different raster backends; `SPIKE-R002` owns evidence for the accepted structural and visual comparison model.

## Release Qualification

A candidate build qualifies only when:

- contract, migration, validator, compiler, renderer-adapter, CLI/API, and recovery tests pass;
- a clean supported machine installs and restores the reference production;
- repeat renders meet the accepted determinism policy;
- an isolated correction invalidates and rebuilds only expected artifacts;
- full-duration output passes automated, Red-Team, and human gates;
- every bundled or imported delivery asset has acceptable provenance and licensing; and
- known limitations are documented with no unresolved release blocker.

## Metrics Requiring Evidence

- first-pass valid shot-plan rate;
- unsupported-action and fallback rates;
- interaction contact and foot-stability tolerance;
- preview latency and preview/final parity;
- final render throughput, memory, disk, and cache efficiency;
- crash recovery and resume success;
- false-positive and false-negative rate of visual validators;
- hands-on production and revision time versus the manual baseline; and
- Red-Team finding escape rate into human review.

Numerical thresholds must come from `SPIKE-W001`, `SPIKE-F001`, `SPIKE-A002`, `SPIKE-R001`, `SPIKE-R002`, `SPIKE-I001`, and full-production evaluation. This draft must not invent them.

`SPIKE-W001` owns early human-workflow and manual-baseline evidence. `SPIKE-F001` owns the fixture assertions and calibration plan. `SPIKE-CS001`, `SPIKE-A002`, `SPIKE-R001`, `SPIKE-R002`, and `SPIKE-I001` provide storage/recovery, asset, visible-quality, parity, performance, and platform measurements from which thresholds may be proposed.

## Regression Policy

- Every fixed defect adds the smallest fixture that would have caught it.
- Contract and migration fixtures remain permanently versioned while supported.
- Visible changes require updated review evidence, not automatic golden replacement.
- Performance results record hardware and workload; regressions are compared only against compatible baselines.
- Flaky tests are treated as defects and cannot be hidden by unlimited retry.
- A backend adapter may add stricter tests but cannot disable core quality gates.

## Evidence Integration

Each spike report lists affected quality rules and proposed thresholds. Accepted changes update this document, validator specifications, fixture manifests, and product requirements together. Quality conclusions unsupported by artifacts, exact versions, and reproducible commands remain advisory.
