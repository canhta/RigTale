# SPIKE-A001: Fixed-Cast Animation Orchestration

**Status:** Queued. Do not execute until the documentation baseline and implementation plan are approved.

## Question

Which production architecture can reliably coordinate multiple fixed, rigged 2D characters and compile high-level direction into deterministic rendered frames at the quality, editability, and maintainability required by RigTale?

## Why This Requires Evidence

The current concepts—semantic actions, motion layers, interaction anchors, constraint solving, a compiled timeline, and renderer adapters—are working hypotheses. Public feature lists do not prove that these mechanisms compose cleanly across several characters, survive a three-minute production, support isolated rerendering, or produce acceptable visible results.

## Questions to Resolve

1. What rig and drawable model is sufficient for biped, quadruped, vehicle, prop, expression, mask, and layered-compositing requirements?
2. Should agent direction compile through semantic actions, direct timeline operations, engine-native graphs, or a hybrid?
3. How should locomotion, upper-body action, gaze, expression, viseme, prop, and procedural tracks blend and resolve conflicts?
4. How should formations and two-character interactions represent roles, anchors, contact frames, reach limits, and failure behavior?
5. Which responsibilities belong to reusable motion assets, the animation compiler, procedural solvers, and the renderer runtime?
6. What intermediate representation preserves editability while remaining deterministic and practical to inspect, test, migrate, and cache?
7. How should frame evaluation, layer ordering, masks, cameras, parallax, audio timing, and isolated shot rendering behave?
8. What quality, preview latency, render throughput, memory, recovery, and reproducibility thresholds are achievable on a supported macOS workstation?
9. Which requirements must be shared by preview and final rendering, and where may their raster output legitimately differ?
10. Which visible failure modes emerge only across a complete 150–210 second, multi-shot production?

## Research Phase

Before writing experimental adapters:

1. Review small-studio cutout production workflows and primary documentation for relevant authoring and runtime systems.
2. Inspect shortlisted open-source repositories at exact commits, focusing on rig representation, animation evaluation, timelines, constraints, scene graphs, rendering, tests, and failure handling.
3. Record patterns that are production-proven, patterns that are merely editor features, and claims that require execution.
4. Compare at least three orchestration models without assuming a renderer:
   - semantic production program compiled into a concrete timeline;
   - direct manipulation of a typed timeline;
   - engine-native animation graphs or scripts behind a stable adapter.
5. Convert unresolved claims into explicit fixture assertions and measurements.

## Executable Phase

Use one versioned fixture across every qualified approach. It must exercise:

- at least three simultaneous character instances;
- biped, quadruped, and vehicle archetypes;
- reusable solo motion and synchronized group choreography;
- at least one role-based interaction with a visible contact frame;
- concurrent body, expression, gaze, viseme, and prop tracks;
- masks, draw-order changes, camera movement, and parallax;
- capability rejection and recoverable compilation failures;
- exact frame addressing, repeat renders, and isolated shot rerendering; and
- representative repetition and continuity across a full-length production, not only a short showcase clip.

Short diagnostic shots may isolate failures, but the final conclusion must include the complete reference-production duration.

## Measurements

- Visible motion and deformation quality against approved references.
- Contact accuracy, foot stability, occlusion, layer order, and continuity.
- Rate and severity of unsupported or conflicting instructions.
- Determinism across repeat renders and clean machines.
- Structured edit size and rerender scope for a single corrected action.
- Preview latency, final-render throughput, peak memory, and cache behavior.
- Crash recovery, resumability, diagnostics, and artifact traceability.
- Contract complexity, adapter size, automated-test coverage, and solo-maintenance cost.

## Required Outputs

- An evidence report with exact sources, repository commits, file paths, commands, and artifacts.
- A versioned representative fixture and approved visual references.
- A recommended orchestration model or a documented reason to defer selection.
- Proposed revisions to production contracts and renderer-adapter requirements.
- A failure catalogue and measurable quality thresholds.
- Updates to `product-requirements.md`, architecture documents, quality gates, implementation plan, and `TODO.md`.
- Separate decision records for any accepted architectural choices.

## Exit Criteria

- At least three orchestration models are evaluated from primary evidence.
- At least two qualified implementations execute the shared fixture, or blocking failures are reproduced and documented.
- The complete-duration reference production exposes repetition, continuity, recovery, and performance behavior.
- Every proposed requirement is classified as demonstrated, rejected, deferred, or still evidence-pending.
- No renderer or orchestration model is selected solely from documentation, popularity, or a successful short clip.

## Non-Goals

- Selecting the macOS UI design, cloud topology, or commercial model.
- Generating character artwork or final video pixels with a generative model.
- Building a general-purpose drawing or free-form keyframe editor.
