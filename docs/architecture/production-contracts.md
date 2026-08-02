# RigTale Production Contracts

**Status:** v1 draft.

## Purpose

This document defines the renderer- and provider-neutral production objects that connect users, agents, deterministic tools, editors, validators, and render backends. It defines responsibilities and invariants, not a final serialization format or engine-specific rig model.

## Contract Principles

- Every durable object has a stable ID, schema version, content version, provenance, and dependency references.
- Published assets are immutable. Changes create a new version and explicit dependency updates.
- Agents exchange typed artifacts through tools; chat history is not production state.
- Semantic intent and compiled animation state are separate artifacts.
- Unsupported capabilities and incompatible versions fail explicitly.
- Approved productions remain inspectable, editable, and renderable without an AI provider.
- Renderer-specific data may exist inside an adapter package but must not leak into episode authoring.

## Canonical Object Graph

```text
Production
├── CreativeBrief
├── Script / Lyrics
├── AudioTimeline (optional by content type)
├── Episode
│   ├── Sequence
│   └── ShotPlan[]
├── AssetLock
│   ├── CharacterPack[]
│   ├── ScenePack[]
│   ├── PropPack[]
│   └── MotionPack[]
├── CompiledShot[]
├── ValidationReport[]
├── ReviewReport[]
├── RenderJob[]
└── DeliveryManifest
```

## Common Envelope

Every versioned artifact must expose the logical equivalent of:

| Field | Requirement |
|---|---|
| `schemaVersion` | Selects the contract schema and migration path. |
| `id` | Stable identity independent of file location. |
| `version` | Monotonic or immutable content version. |
| `status` | Lifecycle state defined below. |
| `createdAt` | Machine-readable timestamp. |
| `createdBy` | User, agent, importer, compiler, or engine identity. |
| `sourceRefs` | Inputs from which this artifact was derived. |
| `dependencies` | Exact IDs, versions, and content digests consumed. |
| `provenance` | Origin, license, attribution, and transformation history where applicable. |
| `extensions` | Namespaced optional data that cannot redefine core semantics. |

The storage encoding, ID format, schema language, and digest algorithm are decision-pending under `SPIKE-CS001` and `RGT-D012`, using contract, migration, corruption, dependency, and archive fixtures.

## Lifecycle

```text
working -> review -> approved -> published -> superseded
                    \-> rejected
```

- `working` artifacts may change in place within a local work session.
- `review` artifacts are frozen while findings are recorded.
- `approved` means a user or defined gate accepted the content.
- `published` means downstream artifacts may reference the immutable version.
- `superseded` preserves history but is not selected for new work.
- `rejected` preserves evidence and review reasons.

## Creative and Timing Contracts

### `Production`

Owns the durable project boundary: selected brief and creative artifacts, episode versions, working and published asset references, review state, delivery history, project configuration, collaborators or local operator identity where applicable, and audit events. A production may contain several episode versions and deliveries without conflating them with one mutable timeline.

### `CreativeBrief`

Owns audience, intent, subject, educational or creative goals, target duration, tone, safety constraints, platform requirements, language, and supplied source material.

### `Script`

Owns narration, dialogue, lyrics when applicable, structural beats, factual citations, speaker roles, and approval state. It references the brief and must preserve changes as versions.

### `AudioTimeline`

Represents optional but authoritative synchronized media. It may contain audio assets, stems, sections, beats, bars, word intervals, phonemes, visemes, cues, and silence regions. It never replaces semantic scene direction.

### `Sequence`

Groups an ordered set of shots that share narrative, educational, musical, spatial, or continuity context. It owns ordering, intended duration range, transition expectations, continuity constraints, and references to its current shot-plan versions. It does not own character or scene assets directly; those resolve through the episode asset lock.

### Time Model

Authoring contracts must support human-readable time plus an exact frame or rational-time representation. Compiled output must avoid cumulative floating-point drift. Frame rate, sample rate, rounding rules, and boundary ownership belong to the project configuration and render manifest.

## Asset Contracts

### `CharacterPack`

Owns a reusable character's visual resources, rig description, drawable bindings, skins, expressions, mouth shapes, attachment points, interaction anchors, preview media, capability manifest, compatibility, provenance, and license.

The following remain hypotheses pending `SPIKE-A001`:

- one universal rig graph can cover every archetype;
- semantic actions should never expose bone-level parameters;
- motion layers and procedural constraints can satisfy all required interactions;
- preview and final backends can consume one rig representation directly.

### `ScenePack`

Owns reusable backgrounds, foregrounds, compositing layers, placement regions, depth or parallax metadata, cameras or camera presets, collision or exclusion regions, lighting or style metadata where supported, and capabilities.

### `PropPack`

Owns reusable props or vehicles, drawable or rig resources, attachment anchors, state variants, interaction capabilities, and optional motion behavior.

### `MotionPack`

Owns reusable motion definitions and compatibility constraints. It must declare roles, required rig features, occupied channels, duration behavior, loop behavior, synchronization markers, root-motion policy, parameters, contact events, and quality status.

### `CapabilityManifest`

Declares supported semantic actions, parameters, constraints, required companion assets, incompatible combinations, and fallback policy. A fallback must be explicit and reviewable; silently substituting a visibly different action is prohibited.

## Episode and Shot Contracts

### `Episode`

Owns production-wide configuration, references to approved creative artifacts, sequences, asset lock, aspect and timing profiles, delivery profiles, and current review state.

### `AssetLock`

Owns the exact published versions and content digests of every character, scene, prop, motion, font, and synchronized media asset selected for an episode build. It also records compatibility results and any approved backend-specific derived conversions. A new asset version creates a new lock; an existing lock is immutable.

### `ShotPlan`

Owns a bounded time range, scene selection, character and prop instances, semantic actions, choreography, interactions, camera direction, transitions, audio cues, continuity references, and expected validation assertions.

Each character instance must have independent identity, asset version, role, placement, visibility, and action tracks. Shared choreography references instances by role rather than by display name.

### Semantic Action

A semantic action states intent, participants, time range, parameters, synchronization cues, and required capabilities. Its final grammar is evidence-pending. Agent-authored actions must be bounded by the selected asset lock and validated before compilation.

### Interaction

An interaction must identify participant roles, required anchors or spatial relationships, synchronization events, acceptable tolerances, interruption behavior, and failure policy. Whether it compiles to authored paired clips, constraints, inverse kinematics, procedural correction, or a hybrid remains decision-pending under `SPIKE-A001`.

## Compiled Contracts

### `CompiledShot`

The animation compiler's immutable output for a specific shot and dependency lock. It resolves semantic direction into renderer-consumable scene state without discarding the source plan.

It must include:

- exact shot and frame boundaries;
- resolved asset and motion versions;
- concrete character, prop, camera, layer, mask, expression, and timing tracks;
- deterministic parameters and random seeds;
- warnings, applied fallbacks, and compiler diagnostics;
- source mapping from compiled elements to authoring instructions; and
- a content digest suitable for cache invalidation.

The concrete track representation is not accepted until `SPIKE-A001` demonstrates it.

### `RenderJob`

Requests rendering of an episode, shot, or frame range against an exact compiled artifact, backend profile, quality profile, output specification, and resource limits. It owns status, attempts, progress, diagnostics, logs, and produced artifacts.

The stable application-tool schemas for submitting, polling, cancelling, resuming, and inspecting long-running jobs are approved under `RGT-D013` after the contract and local-storage baseline is selected.

### `RenderManifest`

Records engine and adapter versions, dependency digests, configuration, seeds, frame range, output checksums, timing, resource measurements, warnings, and environment identity needed to reproduce the result.

## Review and Delivery Contracts

### `ValidationReport`

Contains machine-produced findings with rule ID, severity, artifact location, affected time or frame range, evidence, remediation hint, and validator version.

### `ReviewReport`

Contains Red-Team or human findings with reviewer identity, rubric version, severity, evidence artifact, affected shot or time range, disposition, and resolution reference.

### `DeliveryManifest`

Records approved source versions, final media, captions, thumbnails where applicable, codecs and profiles, checksums, QC reports, attribution, licenses, and archive metadata.

## Error Contract

All deterministic tools must return structured errors with:

- stable error code and severity;
- stage and artifact reference;
- precise field, shot, frame, or dependency location;
- whether retry can change the result;
- safe remediation guidance; and
- preserved diagnostics without secrets.

Errors are either validation failures, incompatibilities, resource failures, transient execution failures, or internal defects. Agent retries are permitted only for errors marked repairable or transient.

## Compatibility and Migration

- Readers must reject unsupported major schema versions explicitly.
- Compatible additions require defaults and round-trip preservation.
- Migrations create new artifacts and retain source digests; they do not rewrite published history silently.
- Asset and motion compatibility must be checked before shot compilation.
- Renderer adapters declare exactly which contract and feature versions they support.
- A fixture corpus must test current schemas, previous supported versions, invalid inputs, and migration idempotency.

## Evidence Required for Validation

- `SPIKE-C001`: established patterns and failure modes from comparable systems.
- `SPIKE-W001`: real workflow gates, artifact handoffs, and manual baseline.
- `SPIKE-F001`: contract, failure, quality, recovery, and invalidation fixtures.
- `SPIKE-CS001`: schema tooling, canonical serialization, exact time, content identity, migrations, local storage, and archive restoration.
- `SPIKE-A002`: source assets, layered ingestion, rig publication, capability, and versioning.
- `SPIKE-A001`: provisional action, motion composition, interaction, compiled timeline, and invalidation models.
- `SPIKE-R001`: visible execution, renderer boundary, supported features, headless operation, recovery, and reproducibility.
- `SPIKE-R002`: preview and final parity.
- Production fixtures: schema evolution, isolated correction, cache invalidation, and full-duration behavior.

## v1 Draft Exit Criteria

- Every contract has one owner and a defined lifecycle.
- Authoring intent, compiled animation, render execution, validation, and delivery are distinct.
- Renderer-specific and provider-specific data cannot redefine core semantics.
- Unknown representation choices are linked to evidence work.
- Product requirement IDs can be traced to the contracts that satisfy them.

The canonical traceability matrix lives in `docs/requirements/product-requirements.md`; contract changes must update that matrix in the same review.
