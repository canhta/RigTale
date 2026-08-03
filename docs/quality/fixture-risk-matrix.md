# Fixture Risk-to-Requirement Matrix

**Owner:** `SPIKE-F001` (`RGT-S003`). Method steps 1 and 2.

**Purpose.** Map every material production risk to at least one isolated fixture assertion, before any asset or adapter is written. `SPIKE-F001` states the reason: a convenient demo scene can make a weak architecture look successful. A risk with no assertion is a stop condition, not an omission.

Risks are derived from the charter, the v1 requirements, the quality gates, and the accepted findings of `RGT-S001`, `RGT-S009`, and `RGT-S014`. Each row names where the risk is evidenced, so no row is a guess dressed as a finding.

**Fixture layer** is one of `contract` (small valid and invalid artifacts), `diagnostic` (short shot isolating one behaviour), or `production` (the complete 150–210 second run). Short diagnostic output cannot replace full-duration evidence.

## Ingestion and Publication

| ID | Risk | Evidenced by | Endangers | Assertion | Layer |
|---|---|---|---|---|---|
| RISK-01 | The source tool destroyed structure before RigTale saw the file, so the input is well-formed and already lossy | `RGT-S014` §1.8: Clip Studio rasterises and drops vector-layer pixel data on PSD export | `PR-A003` | A PSD exported from a vector-layer source imports with an explicit data-loss diagnostic, distinct from a malformed-input error | contract |
| RISK-02 | Structure cannot be preserved uniformly, so "preserve" silently means "flatten" | `RGT-S014` §1.11: Live2D requires masks removed; Inochi Creator maps unsupported blend modes to Normal | `PR-A003`, `PR-C003` | A PSD carrying a clipping mask and a non-W3C blend mode either imports with a recorded diagnostic or fails explicitly. Silent flattening fails the assertion | contract |
| RISK-03 | Untrusted archives carry attacker-controlled paths and sizes | `RGT-S014` §1.13; `system-design.md` Security Boundaries | `PR-A003`, `PR-P005` | Four named cases — path traversal, decompression ratio, nesting depth, length-field overflow — each rejected with an actionable diagnostic | contract |
| RISK-04 | A rig revision invalidates finished shots, and the system cannot say which | `RGT-S009` §13: shots must pin asset versions; `RGT-S001`: rig-change propagation is unsolved or lossy in every system examined | `PR-O03`, `PR-A001`, `PR-Q004` | Publish v1, reorder the rig hierarchy in v2, and the dependency graph names exactly the affected shots — no more, no fewer | contract |
| RISK-05 | A capability manifest claims an action the rig cannot perform | `PR-A002`; `RGT-S001` capability findings | `PR-A002`, `PR-C003` | A pack declaring an unsupported action fails at compile, before render | contract |
| RISK-06 | A published pack carries no provenance or licence metadata | `PR-P005`; charter redistribution constraint | `PR-P005`, `PR-A001` | Publication blocks when licence or provenance is missing | contract |
| RISK-07 | A sandbox asset reaches official evidence | `SPIKE-F001` stop conditions; `.sandbox/README.md` | `PR-P005` | No fixture manifest, expected-evidence record, or approval artifact resolves to a `.sandbox/` path | contract |

## Orchestration and Choreography

| ID | Risk | Evidenced by | Endangers | Assertion | Layer |
|---|---|---|---|---|---|
| RISK-08 | Multiple instances of one character lose distinct identity, placement, or role | Charter Objective 1: at least three simultaneous instances | `PR-C001` | A three-instance shot where each instance holds a distinct role, placement, and action through a camera move | diagnostic |
| RISK-09 | Concurrent tracks conflict and are silently blended | `PR-C002`, `PR-C005` | `PR-C002`, `PR-C003`, `PR-C005` | Locomotion, upper-body action, expression, gaze, viseme, and prop tracks run together; a deliberate same-channel conflict is rejected, not averaged | diagnostic |
| RISK-10 | An interaction's contact frame drifts | `PR-C005`; quality metric "interaction contact and foot-stability tolerance" | `PR-C005`, `PR-Q002` | A two-character role-based interaction holds a visible contact frame. Tolerance is evidence-pending and calibrated, not invented | diagnostic |
| RISK-11 | Attachment parenting is lost across a shot boundary | `PR-A004`, `PR-C001` | `PR-C001`, `PR-A004` | A character-to-prop handoff survives a cut with parenting and draw order intact | diagnostic |
| RISK-12 | Quadruped ground contact slips | Charter Objective 1 requires one quadruped | `PR-A004`, `PR-R002` | Locomotion-critical contacts hold across a cycle | diagnostic |

## Render, Blend, and Determinism

| ID | Risk | Evidenced by | Endangers | Assertion | Layer |
|---|---|---|---|---|---|
| RISK-13 | Artwork uses a blend mode no backend implements | `RGT-S014` §2.4: Photoshop defines 28 keys, W3C 16, no library screened implements the extra twelve | `PR-R008`, `PR-C003` | A layer set to Linear Light fails explicitly against the declared profile. Substitution to Normal fails the assertion | contract |
| RISK-14 | Two backends both claim a mode and disagree visibly | `RGT-S014` §2.4: Krita ships four soft-light implementations, Photoshop and SVG variants among them | `PR-R003`, `PR-R008` | A soft-light case renders on two qualified backends within the accepted parity model | diagnostic |
| RISK-15 | Alpha semantics mismatch produces edge haloing | `RGT-S014` §2.5 and the Colour and Alpha Contract: PNG and XCF straight, EXR and Skia and tiny-skia premultiplied, PSD straight per layer | `PR-R003`, `PR-R005` | A cutout edge at low alpha over a contrasting background shows no haloing through each qualified path | diagnostic |
| RISK-16 | 8-bit premultiplication loses precision exactly where haloing lives | `RGT-S014` §2.5: resvg premultiplies into an 8-bit pixmap, in the region its own goldens exempt | `PR-R007` | The alpha-gradient golden compares transparent and near-transparent regions rather than exempting them | diagnostic |
| RISK-17 | Output varies with thread count, architecture, or compiled-in instruction set | `RGT-S014` §2.6: tiny-skia's README ties portability to SIMD level; pixman states no equivalence | `PR-R007`, `RGT-S013` | Repeat renders across the matrix meet the declared determinism class | diagnostic |
| RISK-18 | The compositing stage is non-deterministic even when the rasteriser is not | `RGT-S014` §2.7: no compositing candidate makes a determinism claim | `PR-R007` | Determinism is measured at the compositing stage, not inferred from the rasteriser | diagnostic |
| RISK-19 | Textured mesh deformation is unsupported, or seams at shared edges | `RGT-S014` §2.3 and §2.5: every rig system deforms a textured mesh; SVG has no mesh primitive | `PR-R002`, `PR-R005` | A deformed textured mesh renders without seams at shared triangle edges | diagnostic |
| RISK-20 | An isolated correction rebuilds too much, or too little | `PR-R004`, `PR-Q004`; charter Objective 3 | `PR-R004`, `PR-Q004` | One structured correction invalidates exactly the expected artifact set | production |
| RISK-21 | Frame addressing is off by one, or a range render disagrees with the full render | `PR-R004` | `PR-R004`, `PR-R001` | A rendered frame range is identical to the same frames taken from the full render | diagnostic |

## Full-Duration Production

| ID | Risk | Evidenced by | Endangers | Assertion | Layer |
|---|---|---|---|---|---|
| RISK-22 | Continuity breaks across shot boundaries | `PR-O04`, `PR-Q002` | `PR-O04`, `PR-Q002` | Continuity holds across every cut in the complete production | production |
| RISK-23 | Repetition reads as a templated series | `RGT-S009` §13: YouTube prohibits a highly similar storyline template across multiple videos while allowing a recurring cast | Charter positioning, `PR-O01` | Repeated sections carry controlled variation, and the second production differs on the narrative axis | production |
| RISK-24 | Throughput at 3,600–5,040 frames is unknown | `RGT-S001` defect 5: not one frames-per-second measurement exists across fifteen review records | `PR-R006` | Full-duration render records throughput, memory, disk, and cache efficiency | production |
| RISK-25 | An interrupted job cannot resume | `PR-P004` | `PR-P004`, `PR-R004` | A render killed mid-run resumes without rebuilding completed work | production |
| RISK-26 | An archive does not restore on a clean machine | `PR-P004`, charter success criteria | `PR-P004`, `PR-R006` | A clean supported machine installs, restores, opens, edits, and re-renders the production | production |

## Audio and Delivery

| ID | Risk | Evidenced by | Endangers | Assertion | Layer |
|---|---|---|---|---|---|
| RISK-27 | Vocals are mixed down and on-screen text is baked, making M&E and textless delivery impossible | `RGT-S009` §13; `PR-F003` | `PR-F003`, `PR-O04` | The audio timeline keeps sung vocals as a separate optional track, and on-screen text lives on a removable layer | contract |
| RISK-28 | Audio duration disagrees with the timeline | `PR-F003`; quality Gate 2 | `PR-F003` | A duration mismatch is a blocking structured error, not a silent trim | contract |

## Quality Validation

| ID | Risk | Evidenced by | Endangers | Assertion | Layer |
|---|---|---|---|---|---|
| RISK-29 | Visual validators report false positives or false negatives | Quality metric "false-positive and false-negative rate of visual validators" | `PR-Q002` | Known-good and known-bad golden pairs measure both rates | diagnostic |
| RISK-30 | Red-Team findings escape into human review | Quality metric "Red-Team finding escape rate" | `PR-Q003` | A seeded defect corpus measures the escape rate | diagnostic |
| RISK-31 | The fixture is biased toward one backend's private representation | `SPIKE-F001` fixture-neutrality rules and stop conditions | `PR-R005` | Every expected result is described in production semantics and visible assertions **before** any engine adapter is written | contract |

## Risks With No Fixture Assertion

These are recorded rather than hidden. Two are unassertable by construction; neither is a defect in the fixture.

| Risk | Why no fixture can assert it |
|---|---|
| The approval-gate model does not match how a small team actually works | `PR-F002` is permanently `hypothesis`. `RGT-S009B` was the only route to evidence and was rejected by owner decision. A fixture can exercise the gates RigTale implements; it cannot establish that they are the right gates |
| RigTale reduces hands-on time by at least 50% | Measured by `docs/research/manual-baseline-protocol.md` against an owner-produced baseline, not by a fixture. The self-comparison limitation is recorded in `charter.md`, Charter Revision 1 |
| Output quality reaches a publishable tier | The largest open risk in the project, and the reference production itself is the first test. A fixture asserts structural correctness, not whether the result is worth watching |

## Requirement Coverage

Every requirement is either covered above or explicitly out of fixture scope.

| Requirement | Covered by |
|---|---|
| `PR-O01`, `PR-O03`, `PR-O04` | RISK-04, RISK-20, RISK-22, RISK-23 |
| `PR-O02` | RISK-08, RISK-09 — the production is generated without per-frame keying |
| `PR-F001` | Out of fixture scope. Entry-point flexibility is a surface behaviour; `PR-P001` and `PR-P002` own it |
| `PR-F002` | Unassertable, see above |
| `PR-F003` | RISK-27, RISK-28 |
| `PR-A001`, `PR-A002`, `PR-A003` | RISK-01 to RISK-06 |
| `PR-A004` | RISK-11, RISK-12 |
| `PR-C001` to `PR-C005` | RISK-08 to RISK-12 |
| `PR-R001`, `PR-R004` | RISK-20, RISK-21 |
| `PR-R002`, `PR-R005` | RISK-19, RISK-31 |
| `PR-R003`, `PR-R008` | RISK-13 to RISK-15 |
| `PR-R006` | RISK-24, RISK-25, RISK-26 |
| `PR-R007` | RISK-16, RISK-17, RISK-18 |
| `PR-Q001`, `PR-Q004` | RISK-05, RISK-20, RISK-28 |
| `PR-Q002`, `PR-Q003` | RISK-10, RISK-22, RISK-29, RISK-30 |
| `PR-P001`, `PR-P002`, `PR-P003` | Out of fixture scope. Surface and provider-interface behaviour is measured by `SPIKE-I001` and `SPIKE-M001` |
| `PR-P004` | RISK-25, RISK-26 |
| `PR-P005` | RISK-06, RISK-07 |

## What This Matrix Does Not Yet Contain

Thresholds. Contact tolerance, parity bounds, throughput targets, and validator error rates are all evidence-pending and are calibrated by the spikes that measure them. `quality-system.md` is explicit that this draft must not invent them, and neither does this one.
