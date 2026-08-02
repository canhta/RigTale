# Competitive and Technology Landscape

**Status:** Screened under `SPIKE-C001` (`RGT-S001`). This document indexes candidates and records their screening disposition. Inclusion is not endorsement, and **no candidate is selected**. Detailed evidence lives in `docs/research/repository-reviews/` and `docs/research/candidate-screening.md`; detailed conclusions must not be duplicated here.

**Screening method:** static source inspection at pinned commits for cloned candidates, primary documentation for the rest. No candidate code, dependency, or setup script was executed.

## Disposition Vocabulary

`adopt` · `adapt` · `reference` · `reject` · `defer`, per the research plan. A disposition is a screening outcome, not a technology selection.

## The Pattern That Organises This Index

Screening surfaced one distinction that most candidate lists obscure: **a permissively licensed runtime does not mean an open authoring path.** An agent cannot produce content for a format it cannot write.

| Authoring path | Candidates |
|---|---|
| **Open — a program can author content without a GUI or a proprietary tool** | OpenToonz, Synfig, Glaxnimate, Lottie (via open writers), DragonBones (format only), Inochi2D (format only, writer incomplete) |
| **Closed — runtime is open, authoring is not** | Rive (editor is paid SaaS), Spine (each end user needs a paid editor licence), Live2D (core is a closed binary absent from the repository), Lottie by default (After Effects plus a plugin), Creature, Spriter |

This distinction, not the runtime licence, is what determines fit with RigTale's premise.

## Source-Inspected Candidates

Each has a review record under `docs/research/repository-reviews/`.

| Candidate | Pinned commit | Licence | Disposition |
|---|---|---|---|
| OpenToonz | `5f6beab3` | BSD-3-Clause core | `reference`, trending `adapt` |
| MLT Framework | `8c092fd1` | LGPL-2.1 core, GPL modules optional | `adapt`, leaning `adopt` for compositing |
| Blender | `a3afe632` | GPL, no linking exception | `defer` |
| Godot | `eda2a482` | MIT | `reference`, `adapt` open for embedding |
| DragonBones | `64b6c69a` | MIT | `adapt`, with a decision gate |
| OpenTimelineIO | `0eebd211` | Apache-2.0 | `reference` (strong), `adapt` for versioning |
| Inochi2D runtime | `ec702261` | BSD-2-Clause | `reference`, leaning `adapt` |
| Inochi Creator | `dba60811` | BSD-2-Clause | `reject` as component, `reference` for design |
| Lottie specification | `4b559574` | CSL 1.0 spec, MIT code | `adopt` as validation contract, with a profile |
| Glaxnimate | `eb1c92bd` | GPL-3.0-or-later | `reference`, defer |
| HyperFrames | `74fadf69` | Apache-2.0 | `reference`, `adapt` for determinism layer |
| rlottie | `2365f567` | MIT with vendored carve-outs | `reference`, leaning reject as dependency |
| Rive Runtime | `4ac7b327` | MIT runtime, **paid proprietary editor** | `reference` |
| Motion Canvas | `7b91435c` | MIT, GPLv3 on one package | `reference` |
| Revideo | `b5de67a0` | MIT | `reference`, leaning `defer` |
| OpenMontage | `c36e4122` | **AGPL-3.0** | `reference`, code reuse blocked |
| ViMax | `05a48943` | MIT | `reject` architecture, `reference` two mechanisms |
| Code2MP4 | `91d7ba45` | Apache-2.0 | `reference` |
| Synfig | `eedebcfc` | GPL-3.0 | screening in progress |

## Documentation-Verified Candidates

Evidence in `docs/research/candidate-screening.md`.

| Candidate | Licence | Disposition and routing |
|---|---|---|
| resvg + tiny-skia | Apache-2.0 OR MIT / BSD-3-Clause | **Enter index. Strongest determinism evidence found** — CI-enforced zero-pixel-difference golden tests, CPU-only. Route to `SPIKE-R001`. |
| Theatre.js | Apache-2.0 core, **AGPL studio** | `reference` for the state format. Format is data with stored duration; project dormant since 2024. |
| ThorVG | MIT | `defer`. Headless and frame-addressable, very active — but ships a run-to-run non-reproducibility detector. Route to `SPIKE-R001`. |
| Remotion | **Source-available, not open source** | `defer`, eligible for spiking. Best documented frame-range API of any candidate. Four-employee gate conflicts with the charter's target studio size; recorded as an `RGT-D010` input. |
| Vello / `vello_cpu` | Apache-2.0 OR MIT | `defer`, watch-list. Its own tests document non-exact output **on Apple platforms**. Alpha. |
| PixiJS | MIT | `reference`. Route to `SPIKE-R001`; headless Node execution is a userland package outside the organisation. |
| node-canvas | MIT | Route to `SPIKE-R001`. **Cairo-backed, not Skia-backed** — the index previously conflated it. |
| skia-canvas | MIT | Route to `SPIKE-R001`. GPU by default with no documented CPU parity; no commits for roughly ten months. |
| Skottie | BSD-3-Clause | `reference` for its seek-then-render API shape. Consumes After Effects-derived JSON. |
| CanvasKit | BSD-3-Clause | `defer`, fallback. Official docs contain no Node story. |
| Cairo | LGPL-2.1 or **MPL-1.1** | `defer`. No determinism evidence beyond a design-intent statement. |
| Blend2D | Zlib | `defer`. JIT-compiled per CPU feature set — a structural determinism concern. |
| XDTS | in-repo in OpenToonz | **Enter index.** A JSON exposure sheet with cell, dialogue-timing, and camerawork fields. The closest existing standard to agent-authored production direction. Route to `SPIKE-A001`. |
| Tahoma2D | BSD-3-Clause | **Enter index.** OpenToonz lineage with verified native Apple Silicon packages. |
| FilmAgent | MIT | `reference`. Closed-vocabulary JSON direction plus a deterministic engine, with reusable critic patterns. |
| Code2Video | MIT | `reference`. A separate project from Code2MP4; emits executable Manim code. |
| OpenUSD | TOST-1.0, no SPDX id | `reference` for its layering and override model only. Route to `SPIKE-A001`. |
| Natron | GPL-2.0 | `reference` for its headless frame-range CLI pattern. |
| Ruffle | Apache-2.0 OR MIT | `reference` for its frame-exact export CLI. |
| Spine | **Not OSI; each end user needs a paid editor licence** | `reject` as a dependency. Recorded as a licence trap that looks permissive at a glance. |
| Live2D Cubism | Proprietary core, revenue-gated | `reject`. Core is a closed binary not in the repository. |
| GSAP | **Proprietary, no SPDX, no redistribution grant** | `reject`. Field-of-use clause targets tools that let users build animations without code. |
| anime.js | MIT | `reject`. Healthy and clean-licensed, but timeline callbacks make state executable — same basis as Motion Canvas. |
| Manim | MIT | **Remove from index.** Addresses animation indices, not frames or timecodes; no rig concept. |
| lottie-web | MIT | **Remove from index.** Dormant since 2024; browser-bound; After Effects authoring. |
| Creature, Spriter/SCML | proprietary editors | **Remove from index.** Dead runtimes, no macOS build, unreadable specification. |
| MovieAgent, Anim-Director, AutoStudio | **no licence file** | `reference` in prose only. All rights reserved by default; never vendor. |
| wgpu | MIT OR Apache-2.0 | Route to `SPIKE-R001` as a rendering substrate. Supplies no animation, rig, layer, or timing semantics. |
| SkelForm | GPL-3.0 editor, MIT runtimes | `reference` for the format-and-runtime split. No headless path; bus factor one; format has no published specification. |

## Index Corrections Made During Screening

1. The single "Skia Canvas" row conflated four distinct projects with different licences and backends. Split, with the Cairo-versus-Skia error corrected.
2. Remotion's entry carried no licence caveat despite the project not being open source.
3. Rive's entry recorded the MIT runtime without the paid proprietary editor.
4. Manim was retained despite an architectural mismatch that no renderer-level work could resolve.
5. XDTS, Tahoma2D, MLT, Glaxnimate, resvg, tiny-skia, ThorVG, Theatre.js, Inochi2D, DragonBones, OpenTimelineIO, and HyperFrames were absent entirely.

## Open Screening Items

- Synfig source screening is in progress.
- Star and fork counts are not recorded as evidence anywhere in this screening; several were unobtainable, several conflicted between sources, and none bears on whether a candidate meets a requirement.
