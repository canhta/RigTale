# RigTale Work Tracker

This file is the canonical progress index. Detailed evidence, experiments, and decisions live in the linked documents and must not be duplicated here.

## Status Model

`queued` -> `active` -> `blocked` | `completed` | `rejected`

An item may be marked `completed` only when its linked exit criteria are satisfied and its evidence is committed.

## Active

| ID | Type | Item | Evidence | Status |
|---|---|---|---|---|
_No item is active. `RGT-S003` is the next eligible item; see the note below the queue._

## Blocked

| ID | Type | Item | Blocked by | Evidence |
|---|---|---|---|---|
| RGT-S009B | Workflow spike | Conduct and synthesize five target-user problem interviews | Project Owner authorization to contact participants | `docs/spikes/SPIKE-W001-production-workflow-and-business-evidence.md` |
| RGT-O001 | Owner decision | Decide the provenance and licence of the reference cast, scenes, props, and music: originate, commission, or adapt | Project Owner decision; no research can resolve it | `docs/spikes/SPIKE-F001-reference-production-fixture.md` |
| RGT-O002 | Owner decision | Appoint an independent reviewer for blind quality scoring, or accept a recorded deviation from the blind-review requirement | Project Owner decision | `docs/research/manual-baseline-protocol.md`, `docs/quality/quality-system.md` |

`RGT-S009B` carries the charter Objective 5 interview requirement. It cannot be satisfied by desk research. Technical evidence work may proceed while it is blocked, but `RGT-D010` and `RGT-D012` must not select a production architecture before it is accepted.

`RGT-O001` blocks the completion of `RGT-S003` and therefore every fixture-dependent spike. It was previously recorded only as prose under the queue and had no owner or status.

`RGT-O002` exists because the baseline protocol requires a reviewer who does not know which workflow produced an output, while the charter fixes the project at one developer. As written the requirement is unsatisfiable, and it gates the charter's headline metric.

## Queue

| ID | Type | Item | Depends on | Evidence |
|---|---|---|---|---|
The queue is topologically ordered: no row depends on a row below it. The `Depends on` column is the **union** of tracker dependencies and the linked spike's own stated preconditions. When either changes, both must be reconciled in the same commit.

| ID | Type | Item | Depends on | Evidence |
|---|---|---|---|---|
| RGT-S014 | Ingestion screening | Screen source-artwork formats and settle the vector-versus-raster question. Apply the `PR-A003` criterion to the **read** side: which layered container can a program write without a GUI or proprietary tool | RGT-S001 | `docs/spikes/SPIKE-A002-asset-ingestion-and-rig-authoring.md` |
| RGT-S003 | Fixture spike | Define the representative multi-character production fixture | RGT-S001, RGT-S009, RGT-S009B, RGT-S014, RGT-O001 | `docs/spikes/SPIKE-F001-reference-production-fixture.md` |
| RGT-S002 | Competitive spikes | Deep-review shortlisted repositories using approved fixture cases | RGT-S001, RGT-S003 | `docs/research/repository-reviews/` |
| RGT-S010 | Asset spike | Validate layered-asset ingestion and rig publication | RGT-S001, RGT-S003 | `docs/spikes/SPIKE-A002-asset-ingestion-and-rig-authoring.md` |
| RGT-S011 | Foundation spike | Validate contract tooling, migration, content identity, and local storage | RGT-S001, RGT-S003 | `docs/spikes/SPIKE-CS001-contract-and-local-storage.md` |
| RGT-S012 | Renderer gate | Determine whether `tcomposer` renders headless on macOS with no window server | RGT-S001, RGT-S003 | `docs/spikes/SPIKE-R001-renderer-backends.md` |
| RGT-S013 | Determinism gate | Measure byte-level reproducibility of the shortlisted rasterisers on macOS across runs, thread counts, and architectures | RGT-S001, RGT-S003 | `docs/spikes/SPIKE-R001-renderer-backends.md` |
| RGT-S008 | Orchestration research | Compare renderer-independent orchestration contracts using throwaway harnesses | RGT-S002, RGT-S003, RGT-S009B, RGT-S010 | `docs/spikes/SPIKE-A001-animation-orchestration.md` |
| RGT-S004 | Production-engine spike | Execute shortlisted orchestration and renderer pairings | RGT-S003, RGT-S008, RGT-S012, RGT-S013 | `docs/spikes/SPIKE-R001-renderer-backends.md` |
| RGT-D001 | Qualification | Qualify orchestration and renderer pairings for parity and platform tests | RGT-S004 | Planned qualification record |
| RGT-S005 | Preview spike | Measure preview and final-render parity | RGT-S004, RGT-D001 | `docs/spikes/SPIKE-R002-preview-final-parity.md` |
| RGT-S006 | Integration spike | Compare Swift-to-renderer integration boundaries | RGT-S004, RGT-S005 | `docs/spikes/SPIKE-I001-swift-renderer-integration.md` |
| RGT-D015 | Decision | Accept a renderer determinism policy and a determinism class for the qualifying final-render path | RGT-S013, RGT-D001 | Planned architecture decision record |
| RGT-D010 | Decision | Select the primary production engine, preview, and Swift integration boundaries | RGT-D001, RGT-S005, RGT-S006, RGT-D015, RGT-S009B | Planned architecture decision records |
| RGT-D012 | Decision | Select core languages, contract tooling, and local storage baseline | RGT-S006, RGT-S011, RGT-D010, RGT-S009B | Planned architecture decision records |
| RGT-D009 | Requirements | Reconcile core and local product requirements from accepted evidence | RGT-S009, RGT-S009B, RGT-S010, RGT-D010, RGT-D012 | `docs/requirements/product-requirements.md` |
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
| RGT-S009 | Workflow Part A complete: labelled workflow map, gate evidence status, manual baseline protocol, interview instrument | `docs/spikes/SPIKE-W001-production-workflow-and-business-evidence.md`, `docs/research/small-studio-workflow.md`, `docs/research/manual-baseline-protocol.md` | closed at `b2da9ad` |

## Next Eligible Item

`RGT-S003` (`SPIKE-F001`, the reference fixture) **may be drafted but cannot be approved.** The distinction was previously blurred and is now explicit.

- **May proceed on Part A.** `SPIKE-W001` Downstream Gating permits `RGT-S003`, `RGT-S002`, `RGT-S010`, and `RGT-S011` to gather technical evidence on Part A alone. The brief, cast, diagnostic shots, risk matrix, and acceptance criteria can be specified now.
- **Cannot be approved on Part A.** `SPIKE-F001` precondition requires that `SPIKE-W001` has established "target-user workflow, gate, **and value evidence**." Part A established none of the three cleanly and says so. `SPIKE-W001` Part B exit criteria require that "fixture priorities reflect frequent and costly **real** production failures" — which only interviews can supply. Fixture approval therefore requires `RGT-S009B`.
- **Cannot be measured at all** without `RGT-O001`. The fixture requires original or compatibly licensed characters, backgrounds, props, and music; `SPIKE-F001` stop-conditions require halting if assets lack provable redistribution rights.

An earlier version of this note claimed `RGT-S003` was simply "unblocked" by silently reducing the precondition "workflow, gate, and value evidence" to "workflow evidence." That was wrong.

`RGT-S012` and `RGT-S013` must not run before the fixture is approved. `SPIKE-F001` states the reason: a convenient demo scene can make a weak architecture look successful. Their `Depends on` column previously listed only the completed `RGT-S001`, which contradicted this paragraph in the same file; it now lists `RGT-S003`.

## Open Contradictions Awaiting an Owner Decision

These are recorded rather than silently resolved. Each is a real conflict between two committed documents.

| # | Contradiction | Options |
|---|---|---|
| 1 | `docs/plans/implementation-plan.md` fixes Swift/SwiftUI/AppKit and TypeScript/Vite as a "Technology baseline", while `RGT-D012` is scoped to "select core languages", `docs/architecture/system-design.md` states languages "are not selected without evidence", and no decision record exists. `SPIKE-I001` is named for Swift and `SPIKE-CS001` measures every candidate across Swift, so the unrecorded choice already constrains the decision meant to make it. | (a) Record the macOS-surface language decision now and narrow `RGT-D012` to core/server language, schema tooling, and storage; or (b) strike the baseline line, rename `SPIKE-I001`, and remove Swift from `SPIKE-CS001`. Doing neither means `RGT-D012` is decided by inertia. |
| 2 | Charter Objective 5 requires "at least a 50% reduction in hands-on layout and animation time … compared with a documented manual cutout workflow." `RGT-S009` established that **no such documented baseline exists**, making the claim currently unfalsifiable. The remedy — producing the baseline in-house, with one operator — measures the project against its own manual attempt. | The charter text is unchanged and no revision is proposed. The owner should decide whether to qualify the objective or accept a self-produced baseline with the circularity recorded. |
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
| **Colour management and alpha semantics** — working space, straight versus premultiplied alpha, blend space, output transfer. One incidental mention across all documents. | No owner. This is the most likely reason two renderer backends will disagree, and it is unrecoverable if decided late. Needs a one-page contract before `RGT-S004`. |
| **Encoder** — which encoder ships, under what licence, and whether it is deterministic. Named only inside repository reviews; absent from requirements, contracts, spikes, and decisions. x264 is GPL; FFmpeg splits GPL and LGPL builds; VideoToolbox on macOS is a hardware encoder and hardware encoders are not bit-reproducible, which `hyperframes.md` already established for another project and RigTale never generalised. | No owner. Binds `PR-P005` and `PR-R007`. |
| **Throughput** — no candidate has a frames-per-second figure. The benchmark is 3,600–5,040 frames and will be rendered dozens of times by one developer. | No owner. Whether that is a two-hour loop or a two-week loop determines buildability. |
| **Fonts and text** — no licensing position (fonts are bundled assets and the charter requires redistributability), no shaping requirement, no fallback, no internationalisation. | No owner, while the charter's long-term scope names localisation. |
| **Loudness** — no LUFS, EBU R128, or true-peak requirement for a music product on platforms that normalise. | No owner. |
| **Photosensitive-epilepsy screening** — zero mentions, for children's content. | No owner. A real broadcast QC gate. |
| **Failure semantics as a screening criterion** — the best failure finding in the corpus (silent exit-0 on render error) was found by accident. No other candidate was asked how it reports failure. For an agent-operated system where nobody watches the terminal, exit-code honesty is a selection criterion. | Add to `SPIKE-R001` criteria. |
| **Untrusted-asset ingestion security** — `system-design.md` declares assets untrusted; no candidate parser was assessed. PSD, ZIP, and font parsing are memory-safety minefields and the premise is that strangers upload layered files. | Add to `RGT-S014`. |
| **glTF may refute "Lottie is the only animation format with a published machine validator"** and unlike Lottie expresses skins, joints, and weights. | **Unverified.** Direct primary-source retrieval required before it is relied on — the same failure mode that produced the withdrawn resvg claim. |
| **Candidates never screened** — an independent sweep surfaced populations the round missed entirely, including Japanese/Korean production formats and academic systems with released code. | Route to `RGT-S014` and a second screening pass. Not yet verified by me. |

## Screening Shortlist

`RGT-S001` produced these deep-review candidates, covering four candidate groups. Selection remains blocked on `RGT-D010`.

| Candidate | Why shortlisted | Gating question |
|---|---|---|
| OpenToonz | Only candidate with both an agent-writable text scene format and a headless frame-range renderer | `RGT-S012` — does `tcomposer` run headless on macOS? |
| MLT Framework | Only verified timeline-scope frame-exact range render; LGPL-2.1-only build retains 2D compositing | Does a GPL-free build work on Apple Silicon? |
| resvg + tiny-skia | CPU-only, no GPU driver variance, permissive, very active. **The "zero-pixel-difference" claim was wrong and is withdrawn** — see `candidate-screening.md`. | `RGT-S013` — **does resvg reproduce its own Linux goldens on macOS arm64 at all?** Its CI has no macOS runner. Font pinning is the secondary question. |
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
