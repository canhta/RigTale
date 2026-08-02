# SPIKE-R002: Preview and Final-Render Parity

**Tracker:** `RGT-S005`

**Status:** Queued. Do not execute before the orchestration contract, representative fixture, and qualified renderer candidates exist.

## Question

Can RigTale provide a responsive preview that preserves the authoritative timing, choreography, interaction, composition, and failure behavior of final rendering closely enough for users to approve shots without discovering material differences later?

## Why This Requires a Spike

Preview and final output may use different quality profiles, runtimes, or renderers. Feature claims do not establish parity. A fast preview is harmful if it hides unsupported deformation, changes draw order, drifts in timing, or accepts interactions that fail in final output.

## Preconditions

- `SPIKE-F001` has published the approved fixture and visual assertions.
- `SPIKE-A001` has established a candidate authoritative compiled representation.
- `SPIKE-R001` has produced at least one qualified final-render path and identified viable preview paths.
- Exact engine, adapter, asset-conversion, and environment versions are pinned.

## Approaches to Compare

1. One backend and one compiled representation with separate preview and final quality profiles.
2. Separate preview and final backends consuming the same compiled representation.
3. A preview-specific representation produced by a deterministic, tested conversion from authoritative compiled state.

The spike must not assume that the fastest or simplest approach provides acceptable approval confidence.

## Parity Dimensions

- shot and frame boundaries;
- character, prop, and camera transforms;
- motion phase, speed, loop count, and synchronization events;
- expression, gaze, viseme, attachment, and interaction contact timing;
- masks, layer order, visibility, clipping, and parallax;
- aspect ratio, safe areas, camera framing, and transitions;
- unsupported feature and fallback diagnostics;
- asset version and dependency identity; and
- visible raster output within evidence-backed tolerances.

Color management, antialiasing, sampling, lighting where applicable, texture filtering, and effects may legitimately differ only when the difference is documented, measurable, and cannot invalidate creative approval.

## Method

1. Render every parity-sensitive diagnostic shot through preview and final paths from identical locked inputs.
2. Capture authoritative scene-state or track-state samples at selected frames before rasterization.
3. Compare structural state exactly where contracts permit.
4. Compare visible output using approved frames, overlays, differences, and human review.
5. Repeat on clean supported environments and after process restart.
6. Introduce unsupported features, stale conversions, missing assets, and failed workers to compare diagnostics.
7. Measure the complete reference production for drift, startup, interactivity, memory, and storage behavior.
8. Have reviewers approve from preview only, then record defects discovered in final output.

## Measurements

- exact structural mismatches per sampled frame;
- timing and contact-frame drift;
- visible-difference severity by quality dimension;
- preview startup, first-frame, seek, update, and playback latency;
- final render throughput and memory for the same workload;
- rate of final defects not observable in preview;
- conversion time, cache cost, and stale-preview risk; and
- adapter complexity and regression-test burden.

Numerical pass thresholds are calibrated from the fixture and human approval study, then proposed for the quality system. They are not invented in this specification.

## Required Outputs

- Exact commands, versions, environments, and artifacts for each comparison.
- Machine-readable structural parity report.
- Visual comparisons and human-review findings.
- Catalogue of permitted and blocking differences.
- Proposed preview approval policy and parity thresholds.
- Recommendation for one-backend, dual-backend, converted-preview, or deferred architecture.
- Updates to product requirements, system design, quality system, operations, and implementation plan.
- Decision record for any accepted preview architecture.

## Exit Criteria

- All parity-sensitive fixture cases are compared.
- Structural and visible differences are reproducible and classified.
- Preview approval does not hide any unresolved blocking final-output defect in the evaluation set.
- Full-duration timing and continuity behavior are measured.
- Operational cost and maintenance burden are recorded.
- The accepted path has automated regression assertions and an explicit fallback when preview is unavailable or untrustworthy.

## Rejection Conditions

- Reject a preview path that silently drops required features.
- Reject a conversion that cannot prove freshness against authoritative compiled state.
- Reject a parity claim based only on a few selected screenshots or a short clip.
