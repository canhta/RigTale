# SPIKE-R001: Production Engine and Renderer Execution

**Tracker:** `RGT-S004`

**Status:** Queued. This is the joint executable evaluation of shortlisted orchestration models and renderer backends.

## Question

Which orchestration-model and backend pairing can compile RigTale's structured production into the highest-quality reproducible video while preserving editability, explicit failure behavior, and practical local and future headless operation?

## Preconditions

- `SPIKE-C001` has screened the candidate landscape.
- `SPIKE-F001` has published the fixture suite and expected evidence.
- `SPIKE-A002` has produced viable asset-ingestion and rig-publication inputs.
- `SPIKE-A001` has produced provisional contracts and at least two qualified model/backend pairings.
- Exact source revisions, licenses, visual features, failure cases, and measurement procedures are fixed before adapter execution.

## Candidate Families

- Existing programmable 2D or 2D/3D engines with headless control.
- DCC systems with scriptable scene, animation, compositing, and background rendering.
- Skeletal or vector runtimes where authoring and redistribution constraints permit.
- Web or native 2D render stacks combined with a code-driven timeline.
- A custom native renderer only if existing backends fail a material requirement and the maintenance case is evidenced.

Candidate inclusion and pairing are provisional until screening and `SPIKE-A001` justify them.

## Fixture Suite

Use the approved `SPIKE-F001` suite rather than one overloaded showcase shot:

1. Contract and invalid-input fixtures for capability and failure behavior.
2. Short diagnostic shots isolating rig deformation, motion composition, group choreography, interaction, masks, draw order, camera, and parallax.
3. Representative multi-character shots combining the features likely to interact.
4. The complete 150–210 second production for repetition, continuity, cache, recovery, throughput, memory, storage, and operational conclusions.

Short cases diagnose failures; only the complete production supports workload and production-readiness conclusions.

## Method

1. Implement the smallest isolated adapter for every qualified orchestration/backend pairing.
2. Compile and render identical fixture versions with exact commands and environments.
3. Compare semantic plan, compiled state, rendered evidence, diagnostics, and manifests.
4. Apply the approved single-shot correction and verify dependency invalidation plus isolated rerender.
5. Repeat renders on the same and clean environments.
6. Inject invalid capabilities, process termination, corrupt output, missing assets, incompatible versions, and resource exhaustion.
7. Render the full production and measure visible continuity, operational behavior, and maintenance surface.
8. Classify each requirement as demonstrated, rejected, deferred, or still evidence-pending.

## Measurements

- visual motion and deformation quality against approved references;
- interaction contact, foot stability, occlusion, draw order, framing, and continuity;
- ability to express the episode without backend-specific authoring logic;
- deterministic semantic and frame behavior under the accepted policy;
- structured correction size, invalidation accuracy, and isolated-rerender result;
- startup, preview support, render throughput, memory, storage, and cache behavior;
- crash isolation, resumability, diagnostics, and artifact traceability;
- macOS packaging and future Linux or headless feasibility;
- license and redistribution obligations; and
- adapter size, custom code, automated-test burden, and solo-maintenance risk.

Preview/final parity and Swift process integration receive dedicated follow-up spikes; this spike records prerequisite observations without claiming those later decisions.

## Required Outputs

- Exact source revisions, adapter code, commands, environments, manifests, and rendered artifacts.
- Structural, visual, failure, performance, recovery, licensing, and maintenance comparison.
- Catalogue of unsupported features and reproducible blockers.
- Qualified production-engine pairings for parity and Swift integration, or a documented reason that none qualifies.
- Proposed final contracts, adapter boundary, quality thresholds, and platform constraints.
- Updates to requirements, architecture, quality, operations, implementation plan, and tracker.
- A qualification record that preserves all surviving pairings and rejected alternatives without selecting the final primary renderer.

## Exit Criteria

- At least two qualified orchestration/backend pairings execute the shared fixture suite, or blocking failures are reproduced.
- Diagnostic and complete-duration evidence are both evaluated.
- The structured correction and isolated rerender behave as declared.
- Repeatability, failure recovery, headless behavior, packaging implications, and maintenance cost are recorded.
- Every material conclusion cites artifacts, commands, exact versions, and environment details.
- `RGT-D001` may qualify pairings for downstream tests but must not select the final primary renderer. Final selection waits for `SPIKE-R002`, `SPIKE-I001`, and `RGT-D010`.

## Rejection Conditions

- Reject a pairing that requires episode-specific engine scripts in authoring artifacts.
- Reject silent feature drops or visually incorrect fallback behavior.
- Reject a conclusion based only on documentation, popularity, screenshots, or a successful short clip.
