# RigTale Production System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` only after the Project Owner authorizes execution. This v1 plan is evidence-gated and must be revised after each accepted spike or architecture decision.

**Status:** v1 draft.

**Execution authorization:** Not authorized. Evidence work begins only after the documentation baseline is approved; implementation begins only after the relevant evidence and decision gates pass.

**Goal:** Build a production-ready, local-first system that directs reusable 2D cutout rigs through structured agent-authored productions and deterministically delivers editable, publication-ready multi-character videos.

**Architecture:** Product surfaces call use-case APIs over versioned production contracts. The Studio and Red-Team agents use typed tools, while deterministic services validate assets and plans, compile semantic direction into animation state, render through an adapter, and preserve manifests and review evidence. Local macOS operation is primary; CLI, MCP, future web, cloud, and renderer alternatives reuse the same contracts.

**Technology baseline:** Swift and SwiftUI/AppKit for the macOS product surface; TypeScript and Vite for the future web surface; Vitest for applicable TypeScript tests. Renderer, server/core languages, schema tooling, IPC, storage, queue, media stack, and agent framework remain blocked on evidence and decision records.

## Global Constraints

- Do not implement a renderer, server, or rig model before its required evidence and decision gate passes.
- Do not use black-box text-to-video as the core rendering path.
- Keep agent output structured, capability-aware, bounded, and independently reviewable.
- Keep predictable validation, compilation, rendering, caching, and media work deterministic.
- Preserve asset identity, provenance, licensing, production editability, and isolated shot rerendering.
- Existing approved productions must render without an AI provider.
- Every change must include focused automated tests, fixture evidence, documentation updates, and a reviewable commit.
- Build complete vertical behavior against the reference production before adding optional platforms or generalized features.

## Plan Lifecycle

This document owns build order and evidence gates. It does not duplicate detailed spike methods or accepted architecture decisions.

After each spike or decision:

1. update affected requirement classifications and thresholds;
2. update contracts, system design, quality rules, and operational constraints;
3. replace the affected phase below with an executable subsystem plan containing exact files, interfaces, tests, commands, and commits;
4. review contradictions and dependency order; and
5. obtain approval before implementation begins.

## Proposed Repository Responsibility Map

The names below define ownership boundaries, not selected languages or build tools. An accepted monorepo decision may refine them without merging responsibilities.

| Path | Responsibility |
|---|---|
| `apps/macos/` | Native local studio UI and macOS integration. |
| `apps/web/` | Future browser studio using remote application APIs. |
| `apps/cli/` | Automation and operator commands. |
| `adapters/mcp/` | MCP exposure of scoped application tools. |
| `contracts/` | Versioned schemas, examples, compatibility, and migrations. |
| `core/artifacts/` | Artifact repository, dependency graph, publication, and provenance. |
| `core/assets/` | Asset pack inspection, registry, capability, compatibility, and publication. |
| `core/production/` | Pipeline gates, application use cases, and orchestration. |
| `core/animation/` | Renderer-neutral validation and animation compilation. |
| `core/quality/` | Deterministic validators, findings, rubrics, and quality reports. |
| `adapters/renderers/` | One isolated adapter per renderer backend. |
| `adapters/providers/` | Language, speech, music, alignment, and future provider integrations. |
| `workers/` | Resumable compile, render, media, validation, and migration job execution. |
| `fixtures/` | Contract, asset, animation, failure, migration, and production fixtures. |
| `reference-assets/` | Redistributable, provenance-audited example packs. |
| `docs/decisions/` | Evidence-backed accepted technical choices. |
| `docs/research/` | Primary evidence and repository reviews. |
| `docs/spikes/` | Reproducible experiment definitions and results. |

## Phase 0 — Documentation Baseline

**Purpose:** Establish coherent v1 drafts without treating hypotheses as facts.

**Required outputs:**

- approved charter;
- draft product requirements, production contracts, production pipeline, agent system, system design, quality system, operations, and this plan;
- research plan, candidate index, bounded evidence specifications, and canonical tracker; and
- traceable links from every material unknown to evidence work.

**Exit gate:** Project Owner accepts the v1 set as a research baseline. Acceptance authorizes evidence collection, not product implementation. Accepted under `RGT-D000` at commit `e82c45b`.

## Phase 1 — Workflow, Business, and Competitive Screening

**Tracker:** `RGT-S009` and `RGT-S001`.

**Actions:**

1. Establish the source-cited workflow map, gate evidence status, and ranked problem hypotheses under `RGT-S009`.
2. Define the comparable manual cutout workflow and hands-on time-capture protocol before product evaluation.
4. Verify canonical repositories, licenses, releases, and exact inspected commits.
5. Perform read-only source screening for production models, rig systems, timelines, render boundaries, tests, packaging, and agent workflows.
6. Route executable claims to later fixture-based reviews or technical spikes.
7. Update workflow requirements, fixture priorities, candidate landscape, and bounded repository-review plans.

**Tests of completion, Part A (`RGT-S009`, `RGT-S001`) — met:** workflow claims distinguish facts from hypotheses; every pipeline gate carries an explicit evidence status; the manual baseline protocol is drafted and its bias controls are recorded; every competitive claim cites primary evidence and exact source revisions; no candidate code was executed during screening.

**Part B (`RGT-S009B`) was rejected by Project Owner decision on 2026-08-02** (`docs/requirements/charter.md`, Charter Revision 1). No user-value evidence will be collected. The manual baseline protocol is approved with its tool-class, cast-size, and revision-behaviour assumptions owner-selected rather than evidence-confirmed, and with blind review waived.

**Phase 1 is complete on Part A alone.** `RGT-D010` and `RGT-D012` now select a production architecture without user-value evidence and must state that limitation in their decision records.

**Exit gate:** Workflow/business and competitive reports are approved. No technology is selected solely by this phase.

## Phase 2 — Fixture, Repository Deep Reviews, and Asset Evidence

**Tracker:** `RGT-S003`, followed by `RGT-S002`, `RGT-S010`, and `RGT-S011`.

**Actions:**

1. Specify a legal, redistributable reference cast with biped, quadruped, vehicle, props, and layered scenes.
2. Define short diagnostic shots for motion composition, interaction, masks, draw order, camera, parallax, and failure handling.
3. Define the complete 150–210 second episode needed to expose repetition, continuity, cache, recovery, and performance behavior.
4. Produce approved expected poses, contact frames, compositions, timing, delivery profiles, and quality assertions.
5. Version all source assets, licenses, expected artifacts, and measurement procedures.
6. Deep-review shortlisted repositories and execute code only through bounded fixture-based scopes.
7. Compare layered-asset ingestion, source-of-truth, rig preparation, capability authoring, derived conversion, and immutable publication workflows.
8. Measure preparation effort and failure behavior across biped, quadruped, vehicle, prop, and scene assets.
9. Compare schema, serialization, exact-time, content-identity, migration, local object storage, metadata indexing, corruption recovery, and archive restoration approaches against the fixture corpus.

**Tests of completion:** Candidate implementations receive identical inputs and objective assertions; the fixture contains no protected imitation or unknown-license asset; short tests and the full production share contracts; repository executions cite exact revisions; required asset archetypes complete a measured publish flow or have reproduced blockers; contract/storage combinations pass or reproducibly fail migration, corruption, dependency, index-rebuild, and archive cases.

**Exit gate:** The Project Owner approves the fixture, visual references, repository shortlist, provisional asset-publication inputs, and evidence package for later contract/storage selection before orchestration or renderer adapter experiments begin.

## Phase 3 — Orchestration Model Research

**Tracker:** `RGT-S008`; specification: `SPIKE-A001`.

**Actions:**

1. Compare semantic compilation, direct typed timeline control, and engine-native graphs or scripts from primary evidence.
2. Express identical fixture semantics and invalid cases through competing provisional contracts.
3. Compare capability rejection, conflict representation, source mapping, state-trace determinism, correction size, and invalidation behavior without claiming rendered quality.
4. Identify backend assumptions and hand visible, performance, recovery, and packaging claims to Phase 4.
5. Shortlist at least two orchestration/backend pairings for joint execution.

**Tests of completion:** Exact sources, competing contract examples, invalid cases, deterministic state traces, and correction/invalidation evidence are reproducible; renderer-dependent claims remain explicitly unresolved.

**Exit gate:** Provisional contract candidates and pairings are approved for executable comparison. No orchestration or renderer decision is accepted in this phase.

## Phase 4 — Joint Production-Engine and Preview Spikes

**Tracker:** `RGT-S004`, `RGT-D001`, and `RGT-S005`; renderer specification: `SPIKE-R001`.

**Actions:**

1. Implement the smallest isolated adapter required for every qualified orchestration/backend pairing.
2. Compare visible orchestration, renderer quality, deterministic frame access, diagnostics, masks, deformation, interactions, camera, headless operation, packaging, and licensing.
3. Render repeat attempts and isolated ranges on clean environments.
4. Measure preview latency and final throughput, memory, storage, startup, and cache behavior.
5. Compare preview and final timing, scene state, interaction, composition, and permitted raster differences.

**Tests of completion:** Every candidate either produces complete artifacts with manifests or has a documented reproducible blocking failure; visual comparisons use approved references; measurements identify hardware and versions.

**Exit gate:** `RGT-D001` records which orchestration/backend pairings qualify for downstream parity and platform testing. It does not select the primary renderer. `SPIKE-R002` then records parity evidence needed by Swift integration and final selection.

## Phase 5 — Platform Integration and Final Production-Engine Selection

**Tracker:** `RGT-S006`, followed by `RGT-D010`.

### macOS integration

Compare supervised process, local service, and native library integration where relevant. Measure packaging, signing, startup, cancellation, crash isolation, progress transport, media preview, and upgrade impact.

**Exit gate:** After `SPIKE-R001`, `SPIKE-R002`, and `SPIKE-I001`, `RGT-D010` selects the primary production-engine pairing, preview path, local process, application transport, and Swift integration boundaries required by Phases 6–10.

## Phase 6 — Architecture Consolidation

**Tracker:** `RGT-D009`, `RGT-D001`, `RGT-D010`, `RGT-D012`, and `RGT-D013`. `RGT-D011` is required only for its Phase 11 scope.

**Actions:**

1. Select the evidenced monorepo layout, implementation languages, build orchestration, schema tooling, local metadata strategy, media dependencies, and test runners under `RGT-D012`.
2. Reconcile demonstrated core/local hypotheses and quantitative requirements under `RGT-D009`.
3. Finalize contract schemas, time representation, compatibility, migrations, error codes, job states, and adapter capability negotiation.
4. Approve representative application-tool schemas plus authorization, idempotency, structured errors, progress, polling, cancellation, findings, approvals, artifact references, resume behavior, and contract tests under `RGT-D013`.
5. Update system topology, security boundaries, deployment profiles, and resource floors.
6. Split Phases 7–13 into executable subsystem plans with exact files, APIs, tests, commands, and commit checkpoints.

**Exit gate:** No build task depends on an unrecorded material choice. Contract fixtures and decision records are approved.

## Parallel Evidence Track — MCP and Embedded Agent Execution

**Tracker:** `RGT-S007`, `RGT-D011`, and `RGT-D014`.

After `RGT-D013` approves stable application-tool and job contracts, validate MCP host-operated behavior, approval boundaries, long-running jobs, media references, subscription constraints, session resume, and embedded-provider credential handling. Reconcile the affected `PR-P002` and `PR-P003` requirements through `RGT-D014`.

This track may run alongside Phases 7–10. Failure or delay does not block contracts, assets, animation compilation, rendering, CLI, or the local macOS studio, but `RGT-D011` is required before implementing the MCP and embedded portions of Phase 11.

## Phase 7 — Contract and Artifact Foundation

**Deliverable:** A versioned contract package and local artifact repository that can create, validate, publish, migrate, export, restore, and trace a production without any renderer or AI dependency.

**Required behavior:**

- common envelope and canonical production objects;
- schema validation and structured errors;
- immutable publication and dependency locks;
- content digests and stale-artifact explanation;
- provenance and license metadata;
- compatible-read and migration fixtures;
- atomic storage, export, restore, and audit events; and
- CLI inspection for every canonical artifact.

**Test gate:** Valid, invalid, migration, corruption, atomicity, and archive round-trip fixtures pass on a clean machine.

## Phase 8 — Asset Publication Vertical

**Deliverable:** Import and publish the reference asset library through the same documented workflow intended for user assets.

**Required behavior:**

- one supported layered-artwork importer;
- source provenance and license capture;
- layer mapping, pivots, drawable and rig bindings;
- expression, mouth shape, attachment, interaction, and capability metadata;
- motion compatibility and deformation tests;
- immutable pack publication and version update flow; and
- asset inspection through CLI and macOS UI.

**Test gate:** Biped, quadruped, vehicle, prop, and scene packs validate, preview, version, migrate, and reject incompatible usage deterministically.

## Phase 9 — Animation Compilation Vertical

**Deliverable:** Compile semantic shots into the accepted renderer-neutral or adapter-bound compiled contract selected by evidence.

**Required behavior:**

- multi-instance placement and roles;
- solo motion and selected motion composition;
- synchronized group choreography;
- the approved bounded interaction set;
- expression, gaze, viseme, prop, camera, mask, layer, and parallax tracks;
- capability and conflict errors;
- exact time and frame behavior;
- source mapping, deterministic seeds, diagnostics, and digests; and
- incremental invalidation and isolated shot recompilation.

**Test gate:** Diagnostic fixtures and the full episode compile repeatedly with identical accepted semantics and no hidden fallback.

## Phase 10 — Rendering and Media Vertical

**Deliverable:** Render compiled shots through the selected adapter and assemble validated deliveries.

**Required behavior:**

- adapter capability negotiation and health diagnostics;
- preview, frame-range, shot, and episode jobs;
- supervised execution, cancellation, attempt isolation, resume, and manifests;
- exact frame completeness and cache identity;
- audio and caption assembly when applicable;
- delivery profiles, checksums, QC, and archive metadata; and
- clean-machine installation and renderer verification.

**Test gate:** Repeat renders, interrupted jobs, isolated corrections, corrupt output, insufficient resources, and archive restore pass the accepted policies.

## Phase 11 — Studio and Red-Team Agent Vertical

**Deliverable:** Typed production tools that allow a Studio Agent to author and repair a complete episode and a separate Red-Team Agent to block visible or semantic defects.

**Required behavior:**

- artifact-driven resume and bounded context retrieval;
- capability-aware asset and action selection;
- schema repair with bounded retries;
- structured findings and correction links;
- provider-neutral embedded adapters;
- MCP host-operated tools;
- cost, time, call, and retry limits;
- prompt-injection and untrusted-input defenses; and
- deterministic rendering without provider access.

**Test gate:** Agent fixtures measure valid-artifact rate, unsupported requests, repair loops, context and cost, independent findings, interruption recovery, and full-production completion.

## Phase 12 — macOS Studio and Automation Surfaces

**Deliverable:** A native macOS application plus CLI/API workflow capable of completing the reference production.

**macOS workflow:** Create/open project, inspect assets, review gate state, inspect shots and media, apply structured corrections, approve artifacts, monitor jobs, diagnose failures, render delivery, export, and restore.

**Automation workflow:** Perform equivalent bounded operations through stable CLI and API commands with machine-readable output and idempotency.

**Test gate:** Unit and integration tests cover view models and application operations; UI automation covers the critical reference-production path; CLI contract tests match application behavior; a clean supported Mac completes the documented operator journey.

## Phase 13 — Quality and Production Qualification

**Deliverable:** Automated validators, Red-Team rubric, human review rubric, operational diagnostics, and reproducible release qualification.

**Required behavior:**

- all quality gates and structured finding severities;
- golden and tolerance-based visual fixtures selected by evidence;
- continuity, interaction, composition, timing, media, legal, and recovery checks;
- performance and resource baselines on supported hardware;
- install, upgrade, migration, backup, restore, and rollback procedures;
- license and dependency inventory; and
- signed release artifacts and operator documentation where applicable.

**Test gate:** The reference production and a materially different second production pass without episode-specific engine changes or manual per-frame correction.

## Phase 14 — Production Evaluation and Hardening

**Actions:**

1. Instantiate the manual comparison protocol approved in Phase 1 with the exact published assets and reference-production brief.
2. Complete two owner-operated hands-on evaluations using the manual protocol approved in Phase 1.
3. Measure hands-on layout and animation time, correction effort, failure recovery, learning cost, and visible quality.
4. Resolve blocking findings and add regression fixtures for every product defect.
5. Re-run clean installation, full production, second production, archive restore, and isolated rerender qualification.

**Exit gate:** Charter success and go/no-go criteria pass with recorded evidence. Failure triggers product-scope reconsideration rather than metric redefinition.

## Phase 15 — Web and Cloud Evolution

This phase begins only after local qualification and a separate approved plan.

Potential work includes a TypeScript/Vite web studio, remote application API, portable worker images, object and metadata storage adapters, hosted job orchestration, upload isolation, and measured cost controls. Tenancy, billing, marketplace, and organization administration require separate business justification and are not implied by remote rendering.

## Tracking and Commit Discipline

- `TODO.md` is the canonical status index.
- Each research, spike, decision, subsystem plan, and implementation task has one evidence location.
- Each implementation task begins with a failing focused test or fixture assertion, implements the minimum accepted behavior, runs relevant and broader verification, updates docs, and ends in one reviewable commit.
- No task is marked complete from code presence alone; its stated test gate and evidence must pass.
- Scope changes update the charter or product requirements before implementation changes follow.

## v1 Plan Exit Criteria

- Every charter objective and product requirement area maps to a phase.
- Research and decisions precede dependent implementation.
- Local production qualification precedes web or cloud expansion.
- Full-duration, multi-character output is the final evidence, not a short showcase.
- Deferred choices are explicit and have owners, inputs, outputs, and exit gates.
- The plan can be converted into executable subsystem plans without changing the system's core boundaries.
