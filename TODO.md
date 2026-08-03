# RigTale Work Tracker

This file is the canonical progress index. Detailed evidence, experiments, and decisions live in the linked documents and must not be duplicated here.

## Status Model

`queued` -> `active` -> `blocked` | `completed` | `rejected`

An item may be marked `completed` only when its linked exit criteria are satisfied and its evidence is committed.

## Active

| ID | Type | Item | Evidence | Status |
|---|---|---|---|---|
| RGT-S003 | Fixture spike | Define the representative multi-character production fixture | `docs/spikes/SPIKE-F001-reference-production-fixture.md`, `docs/quality/fixture-risk-matrix.md`, `fixtures/` | `active` since 2026-08-03. Method steps 1–3 done: 31-risk matrix, and the cast. Outstanding: production brief, contract and failure corpus, diagnostic-shot manifests, calibration plan, approving decision record |

## Blocked

| ID | Type | Item | Blocked by | Evidence |
|---|---|---|---|---|
_No item is blocked._

## Closed by Owner Decision

`RGT-S009B` is `rejected`. `RGT-O001` and `RGT-O002` are owner decisions rather than spikes, so they are `resolved` rather than carrying a spike status.

| ID | Result | Reason | Evidence |
|---|---|---|---|
| RGT-S009B | Rejected by owner decision, 2026-08-02. Exit criteria not met and will not be met. | Project Owner is the sole decision-maker and implementer and will conduct no interviews or evaluations with external participants. Recorded as `charter.md` Charter Revision 1, because `SPIKE-W001` states that Part B carries a charter obligation and cannot be waived by an evidence-state transition. | `docs/requirements/charter.md` (Charter Revisions), `docs/spikes/SPIKE-W001-production-workflow-and-business-evidence.md` |
| RGT-O002 | Resolved by recorded deviation, 2026-08-02. Blind-review requirement waived. | A solo project with no external participants cannot supply a reviewer who does not know which workflow produced an output. Quality scoring is owner-performed and non-blind; the Objective 4 rubric result carries that limitation. | `docs/requirements/charter.md` (Charter Revisions), `docs/research/manual-baseline-protocol.md`, `docs/quality/quality-system.md` |
| RGT-O001 | Resolved by owner decision, 2026-08-03. Two asset tiers established. | Internet-sourced assets may be downloaded and used for local technical experiments in the ignored `.sandbox/` workspace, under their own licence or terms. They are never fixtures, approval evidence, or release content. Official evidence must be reproduced on assets with provable redistribution rights. The originate/commission/adapt route is decided **per asset** inside `RGT-S003` method step 4 rather than as a separate blocking decision, because the binding constraint — redistributability — is now fixed. | `.sandbox/README.md`, `docs/spikes/SPIKE-F001-reference-production-fixture.md` |

The consequences of the `RGT-S009B` and `RGT-O002` rows are recorded once, in `docs/requirements/charter.md` under Charter Revision 1. The `RGT-O001` policy is recorded once, in `.sandbox/README.md`.

## Queue

| ID | Type | Item | Depends on | Evidence |
|---|---|---|---|---|
The queue is topologically ordered: no row depends on a row below it. The `Depends on` column is the **union** of tracker dependencies and the linked spike's own stated preconditions. When either changes, both must be reconciled in the same commit.

| ID | Type | Item | Depends on | Evidence |
|---|---|---|---|---|
| RGT-S002 | Competitive spikes | Deep-review shortlisted repositories using approved fixture cases | RGT-S001, RGT-S003 | `docs/research/repository-reviews/` |
| RGT-S010 | Asset spike | Validate layered-asset ingestion and rig publication | RGT-S001, RGT-S003 | `docs/spikes/SPIKE-A002-asset-ingestion-and-rig-authoring.md` |
| RGT-S011 | Foundation spike | Validate contract tooling, migration, content identity, and local storage | RGT-S001, RGT-S003 | `docs/spikes/SPIKE-CS001-contract-and-local-storage.md` |
| RGT-S012 | Renderer gate | Determine whether `tcomposer` renders headless on macOS with no window server | RGT-S001, RGT-S003 | `docs/spikes/SPIKE-R001-renderer-backends.md` |
| RGT-S013 | Determinism gate | Measure byte-level reproducibility of the shortlisted rasterisers **and compositors** on macOS across runs, thread counts, architectures, and **compiled-in instruction set** | RGT-S001, RGT-S003 | `docs/spikes/SPIKE-R001-renderer-backends.md` |
| RGT-S008 | Orchestration research | Compare renderer-independent orchestration contracts using throwaway harnesses | RGT-S002, RGT-S003, RGT-S010 | `docs/spikes/SPIKE-A001-animation-orchestration.md` |
| RGT-S004 | Production-engine spike | Execute shortlisted orchestration and renderer pairings | RGT-S003, RGT-S008, RGT-S012, RGT-S013 | `docs/spikes/SPIKE-R001-renderer-backends.md` |
| RGT-D001 | Qualification | Qualify orchestration and renderer pairings for parity and platform tests | RGT-S004 | Planned qualification record |
| RGT-S005 | Preview spike | Measure preview and final-render parity | RGT-S004, RGT-D001 | `docs/spikes/SPIKE-R002-preview-final-parity.md` |
| RGT-S006 | Integration spike | Compare Swift-to-renderer integration boundaries | RGT-S004, RGT-S005 | `docs/spikes/SPIKE-I001-swift-renderer-integration.md` |
| RGT-D015 | Decision | Accept a renderer determinism policy and a determinism class for the qualifying final-render path | RGT-S013, RGT-D001 | Planned architecture decision record |
| RGT-D010 | Decision | Select the primary production engine, preview, and Swift integration boundaries | RGT-D001, RGT-S005, RGT-S006, RGT-D015 | Planned architecture decision records |
| RGT-D012 | Decision | Select core languages, contract tooling, and local storage baseline | RGT-S006, RGT-S011, RGT-D010 | Planned architecture decision records |
| RGT-D009 | Requirements | Reconcile core and local product requirements from accepted evidence | RGT-S009, RGT-S010, RGT-D010, RGT-D012 | `docs/requirements/product-requirements.md` |
| RGT-D013 | Design | Approve application-tool and long-running-job contracts | RGT-D009 | `docs/architecture/agent-system.md`, `docs/architecture/production-contracts.md` |
| RGT-S007 | Agent spike | Validate MCP host-operated and embedded-agent execution | RGT-D013 | `docs/spikes/SPIKE-M001-mcp-and-embedded-agent-execution.md` |
| RGT-D011 | Decision | Select MCP and embedded-agent execution strategy | RGT-S007 | Planned architecture decision records |
| RGT-D014 | Requirements | Reconcile MCP and embedded-agent requirements from accepted evidence | RGT-D011 | `docs/requirements/product-requirements.md` |

## Completed

| ID | Result | Evidence | Commit |
|---|---|---|---|
| RGT-C001 | Project charter approved | `docs/requirements/charter.md` | `1ca3e47` |
| RGT-D003 | Product requirements v1 drafted | `docs/requirements/product-requirements.md` | `e593958` |
| RGT-D004 | Production contracts v1 drafted | `docs/architecture/production-contracts.md` | `e593958` |
| RGT-D005 | Production pipeline v1 drafted | `docs/architecture/production-pipeline.md` | `e593958` |
| RGT-D006 | Agent system v1 drafted | `docs/architecture/agent-system.md` | `e593958` |
| RGT-D002 | System design v1 drafted | `docs/architecture/system-design.md` | `e593958` |
| RGT-D007 | Quality system v1 drafted | `docs/quality/quality-system.md` | `e593958` |
| RGT-D008 | Deployment and operations v1 drafted | `docs/operations/deployment-and-operations.md` | `e593958` |
| RGT-P001 | Evidence-gated implementation plan v1 drafted | `docs/plans/implementation-plan.md` | `e593958` |
| RGT-D000 | v1 documentation baseline reviewed and evidence work authorized | `docs/README.md`, `docs/plans/implementation-plan.md` | `e82c45b` |
| RGT-S001 | Competitive screening complete: 19 candidates source-inspected at pinned commits plus 29 documentation-verified, 15 review records, four groups, no candidate code executed | `docs/spikes/SPIKE-C001-competitive-landscape.md`, `docs/research/landscape.md`, `docs/research/repository-reviews/` | `9296ffd`, `3cc60c2`, closed at `b2da9ad` |
| RGT-S009 | Workflow Part A complete: labelled workflow map, gate evidence status, manual baseline protocol | `docs/spikes/SPIKE-W001-production-workflow-and-business-evidence.md`, `docs/research/small-studio-workflow.md`, `docs/research/manual-baseline-protocol.md` | closed at `b2da9ad` |
| RGT-S014 | Ingestion screening complete: PSD/PSB and OpenRaster pass the `PR-A003` write gate, `.kra` fails for want of any published specification. Source artwork is layered raster, but the prior shortlist was screening the right libraries on the wrong axis — tiny-skia is a CPU raster compositor. New requirement `PR-R008` created; 18 propagation rows applied | `docs/research/source-artwork-formats.md` | evidence at `089cf41`, propagation applied on closure |

## Notes on the Active Item

`RGT-S003` (`SPIKE-F001`, the reference fixture) is active. Two constraints govern it.

- **Fixture priorities rest on desk research plus owner judgement.** `RGT-S009B` was rejected, so they reflect documented and hypothesised production failures rather than observed ones. This matters because the fixture is what every later spike measures against.
- **Official fixture assets must have provable redistribution rights.** Sandbox assets may bootstrap technical experiments but can never become fixture or approval evidence; `SPIKE-F001` stop-conditions enforce this, and any result promoted to official evidence must be reproduced on official assets. See `.sandbox/README.md`.

`RGT-S012` and `RGT-S013` must not run before the fixture is approved. `SPIKE-F001` states the reason: a convenient demo scene can make a weak architecture look successful.

## Open Contradictions Awaiting an Owner Decision

These are recorded rather than silently resolved. Each is a real conflict between two committed documents.

| # | Contradiction | Options |
|---|---|---|
| 1 | `docs/plans/implementation-plan.md` fixes Swift/SwiftUI/AppKit and TypeScript/Vite as a "Technology baseline", while `RGT-D012` is scoped to "select core languages", `docs/architecture/system-design.md` states languages "are not selected without evidence", and no decision record exists. `SPIKE-I001` is named for Swift and `SPIKE-CS001` measures every candidate across Swift, so the unrecorded choice already constrains the decision meant to make it. | (a) Record the macOS-surface language decision now and narrow `RGT-D012` to core/server language, schema tooling, and storage; or (b) strike the baseline line, rename `SPIKE-I001`, and remove Swift from `SPIKE-CS001`. Doing neither means `RGT-D012` is decided by inertia. |
| 2 | **Closed 2026-08-02 by Charter Revision 1.** No published time baseline exists, so the owner selected the self-produced-baseline branch. Objective 5 now states the baseline is owner-produced and that the self-comparison circularity is a permanent limitation of the metric. | Closed. |
| 3 | Charter constraint "Source code and bundled reference assets must permit legal open-source redistribution" (`charter.md`) has **no product requirement**, therefore no traceability row, no gate, and no phase — while screening produced the project's largest body of licensing evidence. | Add a dependency-licensing requirement, or record why the constraint is unenforced. |

## Owner-Stated Commercial Scale

`[OWNER-STATED]` The project's commercial target is approximately **one million USD**, not venture scale. Recorded here because it changes how business evidence is weighed, and because an independent review reached the opposite conclusion by assuming a scale the charter never states.

**What this settles.** A red-team review argued the commercial case was already dead: the nearest comparable vendor's entire business is roughly USD 9M per year and shrinking, the commissioning market it depends on is contracting, and competing tools are free or near-free. At venture scale that is a ceiling problem. **At the stated target it is the opposite** — it is evidence that the segment exists, pays, and is served by products whose vendors have stopped investing in them. Screening already established the standing-still part from primary sources: one vendor states publicly it will not build AI features, another dropped its cutout product from its roadmap, and a third is in maintenance mode.

The finding is therefore **recorded and not actioned**. It must not be reintroduced as a stop signal without first stating which revenue scale it assumes.

**What this does not settle.** Two risks are independent of revenue ambition and remain fully open:

- **Output quality.** A smaller target does not make weak output acceptable. The assumption that an agent can write structured direction that yields publishable animation still has **no evidence of any kind**, and is currently first tested in implementation Phase 11 — after the contracts, the assets, the compiler, the renderer, and `RGT-D010`.
- **Solo feasibility.** A smaller target does not shrink the scope already committed: roughly thirteen throwaway implementations across the executable spikes, nine executable repository reviews, and three complete hand-made productions that no tracker item creates.

**Strategic consequence: prefer proven prior art over original construction.** The working hypothesis that RigTale must own its rig representation was reached **by elimination** — the weakest available basis for the largest engineering commitment in the project — and the elimination ran before several production-proven permissive schemas were on the candidate list. `RGT-S014` and the second screening pass must test adoption before construction.

**Scope of "clone", stated precisely so it is not mistaken later.** Product model, workflow shape, feature decomposition, pricing, and onboarding may be studied and reproduced freely; that is ordinary competitive design work. Published permissively licensed **formats** may be adopted directly. Proprietary competitors publish no source, so there is nothing there to copy. Copyleft source may be read but not incorporated, because `PR-P005` and the charter's redistribution constraint bind the dependency stack. Adopting a format is not the same act as vendoring a codebase, and only the first is on the table by default.

## Open Evidence Gaps from Independent Review

Found by red-team review of the closed spikes. Each is verified; none is closed.

| Gap | Status |
|---|---|
| **Colour management and alpha semantics** — working space, straight versus premultiplied alpha, blend space, output transfer. | **Closed by `RGT-S014`.** The gap now has evidence and an owner: `docs/architecture/production-contracts.md` carries the Colour and Alpha Contract, required before `SPIKE-R001` executes. `OpenColorIO` is a `reference` candidate for the working-space half. |
| **Encoder** — which encoder ships, under what licence, and whether it is deterministic. Named only inside repository reviews; absent from requirements, contracts, spikes, and decisions. x264 is GPL; FFmpeg splits GPL and LGPL builds; VideoToolbox on macOS is a hardware encoder and hardware encoders are not bit-reproducible, which `hyperframes.md` already established for another project and RigTale never generalised. | No owner. Binds `PR-P005` and `PR-R007`. |
| **Throughput** — no candidate has a frames-per-second figure. The benchmark is 3,600–5,040 frames and will be rendered dozens of times by one developer. | No owner. Whether that is a two-hour loop or a two-week loop determines buildability. |
| **Fonts and text** — no licensing position (fonts are bundled assets and the charter requires redistributability), no shaping requirement, no fallback, no internationalisation. | No owner, while the charter's long-term scope names localisation. |
| **Loudness** — no LUFS, EBU R128, or true-peak requirement for a music product on platforms that normalise. | No owner. |
| **Photosensitive-epilepsy screening** — zero mentions, for children's content. | No owner. A real broadcast QC gate. |
| **Failure semantics as a screening criterion** — the best failure finding in the corpus (silent exit-0 on render error) was found by accident. No other candidate was asked how it reports failure. For an agent-operated system where nobody watches the terminal, exit-code honesty is a selection criterion. | Add to `SPIKE-R001` criteria. |
| **Untrusted-asset ingestion security** — `system-design.md` declares assets untrusted; no candidate parser was assessed. | **Closed by `RGT-S014`.** The attack surface is now named in `system-design.md` Security Boundaries and in the `SPIKE-A002` required cases: path traversal, decompression ratio, nesting depth, length-field overflow, and a memory-safety justification for the parser choice. No fuzzing corpus or security audit exists for any candidate reader, which stays open. |
| **glTF may refute "Lottie is the only animation format with a published machine validator"** and unlike Lottie expresses skins, joints, and weights. | **Unverified.** Direct primary-source retrieval required before it is relied on — the same failure mode that produced the withdrawn resvg claim. |
| **Candidates never screened** — an independent sweep surfaced populations the round missed entirely, including Japanese/Korean production formats and academic systems with released code. | `RGT-S014` covered the source-artwork and raster-compositing populations, including `.clip`, `.sai`, and `.mdp`. The animation and production-system populations remain unscreened and still need a second screening pass. |

## Screening Shortlist

`RGT-S001` produced these deep-review candidates, covering four candidate groups. Selection remains blocked on `RGT-D010`.

| Candidate | Why shortlisted | Gating question |
|---|---|---|
| OpenToonz | Only candidate with both an agent-writable text scene format and a headless frame-range renderer | `RGT-S012` — does `tcomposer` run headless on macOS? |
| MLT Framework | Only verified timeline-scope frame-exact range render; LGPL-2.1-only build retains 2D compositing | Does a GPL-free build work on Apple Silicon? |
| tiny-skia | **CPU raster compositor**, re-scoped by `RGT-S014` from "vector rasteriser" — it composites pixmap-on-pixmap with the full W3C blend set and no path involved. Permissive, CPU-only. | `RGT-S013` — does per-triangle `Pattern`-shader fill give acceptable mesh deformation, and does compiled-in SIMD level change output? |
| Skia | Only candidate with the textured-mesh primitive (`drawVertices`) **and** the full W3C blend set. BSD-3-Clause. | Deterministic headless mesh compositing on macOS arm64, and binding cost from Swift or Node. |
| libvips, pixman | Added by `RGT-S014` as raster-compositing candidates. libvips LGPL-2.1+, pixman MIT. | Is either bit-reproducible across SIMD dispatch and thread count? |
| resvg | SVG front end, **role narrowed** by `RGT-S014` — relevant only if the pipeline has a vector stage. The "zero-pixel-difference" claim was withdrawn earlier. | `RGT-S013` — does it reproduce its own Linux goldens on macOS arm64 at all? Its CI has no macOS runner. Its 8-bit premultiply on image load is lossy exactly where haloing appears. |
| PSD / PSB via `ag-psd` | Only layered source format every ingesting tool accepts and every target painting tool exports; MIT reader and writer, headless. | Does `ag-psd` output open cleanly in Photoshop, Clip Studio, Krita, and Live2D? Requires execution. |
| DragonBones | Only MIT skeletal format recoverable from source; skin overlay matches the fixed-cast premise | Does multi-skin work? No shipped sample exercises it. |
| Godot 2D skeleton stack | Only candidate with every authoring link verified: scriptable bones, scriptable per-vertex weights, scriptable scene serialisation, diffable text IR | Does `libgodot` capture windowless on macOS? Rig is a scene, not a portable format. |
| Blender Grease Pencil | Only purpose-built 2D cutout layer model with per-layer render-target routing | Does it render headless on macOS given the unconditional GPU dependency? |
| Lottie specification | Only animation format with a published machine validator | Can a strict RigTale profile close the permissive unknown-type holes? |
| OpenTimelineIO | Most mature open per-type schema versioning and migration implementation | Design reference only; no gating question |
| HyperFrames | Only candidate whose determinism claim is backed by byte-equality tests | Do those tests run on macOS, or silently skip? |

## Tracker Rules

- Every active item must link to a document with explicit exit criteria.
- Spikes remain queued until the production documentation baseline and implementation plan are approved.
- Unknowns remain spikes; they must not be silently converted into architecture decisions.
- Competitive claims must cite an exact repository commit, source path, release, or official document.
- A spike result may recommend, reject, or defer a candidate. It must not force a positive selection.
- Accepted technical choices are recorded once in an architecture decision record and then referenced by the system design.
