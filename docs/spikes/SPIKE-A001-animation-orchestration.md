# SPIKE-A001: Fixed-Cast Orchestration Model Research

**Tracker:** `RGT-S008`

**Status:** Queued. This spike defines provisional renderer-independent models; it does not select a production engine or claim rendered quality.

## Question

Which orchestration models are expressive, deterministic, inspectable, and bounded enough to carry into joint animation-engine and renderer execution under `SPIKE-R001`?

## Why This Is Separate from Renderer Execution

Semantic actions, direct typed timelines, engine-native graphs, motion layers, interaction anchors, and compiled tracks are hypotheses. They can first be compared through primary-source research, contract examples, invalid cases, and deterministic state traces. Visible quality, frame output, throughput, recovery, and full-duration behavior require a real backend and belong to the joint execution stage in `SPIKE-R001`.

This staging removes circularity:

```text
fixture and asset evidence
-> orchestration research and provisional contracts
-> joint orchestration/backend execution
-> production-engine decisions
-> preview parity and Swift integration
```

## Preconditions

- `SPIKE-C001` has screened relevant systems.
- `SPIKE-W001` has validated production workflow and user priorities.
- `SPIKE-F001` has published engine-neutral fixture intent and assertions.
- `SPIKE-A002` has documented viable layered-asset and rig-publication inputs.

## Models to Compare

At least these three families must be evaluated:

1. Semantic actions compiled into a concrete deterministic timeline.
2. Direct manipulation of a typed, constrained animation timeline.
3. Engine-native animation graphs or scripts behind a stable production adapter.

A hybrid may be shortlisted only when its ownership boundaries and failure behavior are explicit.

## Questions to Resolve Provisionally

1. Which direction belongs in agent-authored `ShotPlan` versus deterministic compiled state?
2. How are instances, roles, formations, actions, reactions, gaze, expression, viseme, props, cameras, masks, and layers represented?
3. How do locomotion, upper-body, facial, prop, and procedural tracks declare occupancy and conflicts?
4. How do interactions declare roles, anchors, contact events, reach constraints, interruption, and failure without assuming one solver?
5. Which rig and motion capabilities must authoring contracts expose without leaking one engine's data model?
6. How are exact time, random seeds, source mapping, diagnostics, dependency digests, and incremental invalidation represented?
7. Which claims cannot be resolved without rendered execution and must be handed to `SPIKE-R001`?

## Method

1. Inspect primary documentation and exact source revisions for shortlisted orchestration models.
2. Map each model to the fixture's semantic and invalid cases without writing renderer adapters.
3. Draft the smallest competing contract examples for the same diagnostic shots.
4. Produce deterministic state or event traces sufficient to compare timing, conflicts, source mapping, and dependency invalidation.
5. Apply one structured correction and compare edit size plus expected invalidation across models.
6. Catalogue backend assumptions, unsupported requirements, ambiguous behavior, and questions requiring visible execution.
7. Select at least two provisional model/backend pairings for `SPIKE-R001`, or record why evidence is insufficient.

## Measurements

- fixture requirements expressible without backend-specific episode logic;
- schema and contract complexity;
- invalid or conflicting instruction detection;
- source-map precision and correction size;
- deterministic state-trace repeatability;
- dependency and cache-invalidation explainability;
- number and severity of backend assumptions; and
- expected adapter and solo-maintenance burden, clearly marked as estimates until execution.

## Required Outputs

- Source-cited comparison of at least three orchestration models.
- Competing contract examples and invalid cases for the same fixture shots.
- Deterministic state traces and correction/invalidation evidence.
- Provisional production-contract revisions.
- Shortlist of at least two orchestration/backend pairings for joint execution.
- Explicit handoff matrix of visible, performance, recovery, and packaging claims for `SPIKE-R001`.
- Updates to product requirements, system design, quality rules, implementation plan, and tracker.

## Exit Criteria

- At least three models are compared from primary evidence.
- At least two models express the required fixture semantics or have reproducible blocking gaps.
- Renderer-dependent claims are handed off rather than treated as conclusions.
- Provisional contracts define deterministic inputs, outputs, failures, source mapping, and invalidation.
- No orchestration model or renderer is selected by this spike.

## Non-Goals

- Rendering final frames or measuring visible output quality.
- Measuring preview latency, final throughput, crash recovery, or clean-machine packaging.
- Selecting the macOS integration, cloud topology, or commercial model.
- Building a general-purpose drawing or free-form keyframe editor.
