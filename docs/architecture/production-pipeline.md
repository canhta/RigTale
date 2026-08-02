# RigTale Production Pipeline

**Status:** v1 draft.

## Purpose

This document defines how production artifacts move from creative intent to structured animation and delivery. It is a workflow contract, not a claim about the internal process of any referenced studio and not a selection of animation or rendering software.

## Pipeline Overview

```text
Intent intake
-> research and script
-> synchronized media preparation when applicable
-> visual and scene planning
-> asset resolution and publication
-> shot planning
-> animation compilation
-> deterministic validation
-> animatic and shot preview
-> Red-Team and human review
-> correction and isolated recompilation
-> final render and media assembly
-> QC, delivery, and archive
```

The earliest required input is a creative prompt or brief. Script, lyrics, audio, timing, and structured project artifacts are optional entry accelerators. For synchronized content, audio lock is a gate before exact shot timing; it is not the product's mandatory entry point.

## Stage Contracts

| Stage | Required inputs | Produced artifacts | Blocking gate |
|---|---|---|---|
| Intent intake | User prompt or source brief | Versioned `CreativeBrief` | intent approval |
| Research and script | Brief, supplied sources | Research notes, `Script`, lyrics or scene intent | factual and creative approval |
| Media preparation | Approved text and optional supplied media | `AudioTimeline`, timing and alignment data | media lock when synchronization is required |
| Visual planning | Approved creative artifacts | Style references, scene plan, storyboard or animatic plan | visual-direction approval |
| Asset resolution | Scene plan and asset requirements | Published packs and `AssetLock` | capability and license validation |
| Shot planning | Approved plan, timing, asset lock | Versioned `ShotPlan` set | plan validation |
| Compilation | Valid shot plans and published assets | `CompiledShot` set and diagnostics | compile validation |
| Preview | Compiled shots | Animatic or review media, preview manifest | review readiness |
| Review and correction | Plans, previews, reports | Findings, corrected artifacts, approvals | no blocking findings |
| Final rendering | Approved compiled shots | Frames, shot masters, render manifests | render completeness |
| Assembly and delivery | Shot masters and media | Final video, captions, QC and delivery manifest | delivery approval |
| Archive | Approved delivery and all source locks | Restorable production archive | restore verification |

`SPIKE-W001` validates exact gate names, mandatory versus optional handoffs, and which steps are practical to automate. Every bypass must be explicit, versioned, and visible downstream.

## Entry Modes

### Idea-led production

The user supplies a prompt or brief. The Studio Agent researches when needed, proposes the script and scene structure, then requests approval before expensive downstream work.

### Script-led production

The user supplies a script or lyrics. RigTale validates requirements, derives missing scene intent and timing, and preserves the original text as a source artifact.

### Media-led production

The user supplies locked audio or narration. RigTale derives alignment data and scene timing but still requires semantic creative intent; audio alone must not be treated as sufficient direction.

### Existing-production revision

The user opens a versioned production, changes one structured artifact, and asks the system to identify, rebuild, review, and render only affected dependents.

## Asset Preparation Flow

```text
source artwork or reusable pack
-> provenance and license capture
-> format and layer inspection
-> layer mapping and pivot proposal
-> rig and drawable binding
-> expressions, mouth shapes, anchors, and capabilities
-> deformation and motion tests
-> review
-> immutable publish
```

Initial production may use prepared reference assets to simulate user uploads. Assisted mapping and rigging can reduce repeated work, but published capability and visual tests remain mandatory. Future generated artwork must enter through the same import and publication flow.

An episode references published asset versions. Shot work never edits a published rig in place. Asset fixes create new versions, and dependency analysis identifies affected shots.

## Shot Planning and Orchestration

The Studio Agent converts approved creative artifacts into semantic shots. A plan must state:

- dramatic or educational purpose;
- exact time or section ownership;
- scene, cast, roles, props, and composition;
- actions, reactions, choreography, and interactions;
- camera, transitions, and continuity constraints;
- required capabilities and expected visible results; and
- validation assertions and fallback policy.

Before compilation, deterministic validation resolves asset versions and proves that required capabilities exist. The system returns a repairable structured finding when direction is invalid; it must not render a plausible but incorrect substitute silently.

## Animation Compilation

Compilation is the product's critical evidence-pending stage. It must transform semantic direction into a concrete, deterministic `CompiledShot` while preserving source mapping.

Candidate responsibilities include motion selection, timing, formation, motion composition, interaction solving, expression and viseme tracks, camera and layer planning, and cache dependencies. These are requirements to investigate under `SPIKE-A001`, not accepted implementation choices.

Compilation must be idempotent for identical locked inputs. Any random variation must be seeded and recorded. Warnings and fallbacks form part of the output and are reviewable.

## Preview, Review, and Correction

- Animatic output validates timing and shot structure before high-cost rendering.
- Shot previews expose motion, interaction, layer, framing, and synchronization defects.
- The Red-Team Agent reviews plans and visible output using versioned rubrics.
- Human approval is required at defined creative and delivery gates.
- Findings reference exact artifacts and time ranges.
- Corrections create new source versions; they do not patch rendered frames.

Preview and final render must consume the same authoritative compiled state unless an evidence-backed decision explicitly permits a conversion step. Parity requirements are measured later.

## Dependency and Rerender Model

Every derived artifact records exact input digests. A change invalidates only its transitive dependents:

```text
script section -> affected shot plans -> affected compiled shots -> affected previews/renders -> episode assembly
character pack -> shots using that version -> their downstream artifacts
delivery profile -> encode outputs only, unless composition requirements change
```

The system must explain why an artifact is stale. Users may not force delivery with stale or incompatible dependencies without an explicit recorded exception and blocking review.

## Failure and Recovery

- Each stage writes artifacts atomically or to an isolated attempt directory.
- Long-running jobs persist checkpoints and may resume without repeating approved upstream work.
- Transient execution failures may retry within declared limits.
- Deterministic validation failures require changed input, not blind retry.
- A failed shot must not corrupt previously approved assets or other shots.
- Logs, reports, intermediate media, and manifests remain attached to the attempt.
- Recovery behavior is tested using process termination, corrupt artifacts, insufficient storage, and incompatible dependency fixtures.

## Production Completion

A production is deliverable only when:

- every required source artifact and asset version is approved and locked;
- every shot compiles and renders with no blocking deterministic finding;
- episode duration and media alignment are correct;
- Red-Team and human review gates pass;
- delivery media, captions, manifests, attribution, and QC reports are complete; and
- the archive can be restored and an isolated shot can be reproduced.

## Evidence and Revision

- `SPIKE-W001` validates stage boundaries, artifact handoffs, user value, and the manual comparison baseline.
- `SPIKE-A002` validates asset ingestion, rig preparation, authoring effort, and publication.
- `SPIKE-F001` defines quality, recovery, invalidation, and full-duration assertions.
- `SPIKE-A001` validates provisional orchestration and compilation contracts without claiming rendered quality.
- `SPIKE-R001` validates visible orchestration, rendering, frame addressing, recovery, headless execution, and packaging.
- Quality and recovery fixtures establish measurable thresholds.

Findings must update this document and linked requirements; a spike report alone is not considered integration of evidence.
