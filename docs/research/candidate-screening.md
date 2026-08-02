# Candidate Screening Evidence

**Screened under:** `SPIKE-C001` (`RGT-S001`). Read-only. No candidate code, dependency, or setup script was executed.

This document holds documentation-level verification for candidates that were not source-inspected from a local clone. Source-inspected candidates have dedicated records under `docs/research/repository-reviews/`.

All URLs accessed 2026-08-02.

## Evidence Rules Applied

Official reference documentation and repository source files are treated as primary evidence. Marketing pages, README positioning, and star counts are discovery signals only and are labelled as such. Where a fact could not be verified from a primary source it is recorded as "not verified" rather than inferred.

## Licensing Finding: Remotion Is Source-Available, Not Open Source

Verified twice, independently of the screening agent. This is a constraint to carry forward, not a screening rejection.

| Claim | Primary source |
|---|---|
| GitHub classifies the licence as `NOASSERTION` with `license.key = "other"` | `https://api.github.com/repos/remotion-dev/remotion` |
| "No. Remotion is source-available software, but it is not open-source software according to the Open Source Initiative's Open Source Definition" | `https://www.remotion.dev/docs/license/faq` |
| Free License covers "an individual", "a for-profit organization with up to 3 employees", "a non-profit or not-for-profit organization", and evaluation use | `https://raw.githubusercontent.com/remotion-dev/remotion/main/LICENSE.md` |
| "It is not allowed to copy or modify Remotion code for the purpose of selling, renting, licensing, relicensing, or sublicensing your own derivate of Remotion." | same file, verbatim |
| Company License required for organisations of four or more people, from USD 100/month; Enterprise from USD 500/month | `https://www.remotion.pro/license` |

The word "open source" does not appear in `LICENSE.md` at all.

### What the terms do and do not prohibit

The prohibition is scoped to copying or modifying Remotion code in order to sell, rent, licence, relicence, or sublicence a derivative of Remotion. **Depending on Remotion as an unmodified package is not that act.** RigTale would neither fork it, vendor its source, nor redistribute a derivative, so the sublicensing clause does not apply and the charter's open-source redistribution constraint on RigTale's own source and bundled assets is not breached.

Two real obligations remain, and both are downstream-user obligations rather than blocks on RigTale:

1. **Headcount gate.** Free use covers individuals, non-profits, and for-profit organisations with up to three employees. The charter's stated initial users include "small animation studios with approximately two to five team members". **A four- or five-person studio in RigTale's own target profile would need a paid Remotion Company License to run RigTale**, from USD 100/month. That is a concrete conflict with the target-user profile, not a hypothetical one.
2. **The obligation transfers to every RigTale user**, who must qualify independently. RigTale could not describe its stack as fully free to that segment.

Neither obligation blocks evaluation. Both must be visible when `RGT-D010` chooses, and the second is a business decision for the Project Owner rather than a research finding.

**Discovery-signal contrast worth recording.** The repository presents as mainstream open source — 55,260 stars, a conventional README — with one soft sentence of licence warning, while its own documentation states plainly that it is not open source. Screening that accepted repository presentation as evidence would have carried an unexamined licensing obligation into a later decision. This is the concrete justification for the research plan's rule that README claims are not sufficient technical evidence.

**Disposition:** `defer`. Eligible for executable evaluation. Its frame-range API is the closest documented match to RigTale's isolated-rerender requirement of any candidate screened, which is reason enough to test it rather than screen it out. Route to `SPIKE-R001` with the licensing obligations recorded as a decision input for `RGT-D010`.

## Second Finding: The "Skia Canvas" Index Entry Is Wrong

`docs/research/landscape.md` carried a single row, "Skia Canvas — server-side 2D renderer, off-screen frame rendering from Node.js". That entry conflates at least four distinct projects with different licences, rendering backends, and maintenance states.

Most materially, **`Automattic/node-canvas` is Cairo-backed, not Skia-backed** (`https://github.com/Automattic/node-canvas`). Any reasoning that assumed a shared Skia backend across "server-side Node canvas renderers" was factually wrong.

The index is corrected to list `skia-canvas` and `node-canvas` as separate rows, with Skottie and CanvasKit recorded as related but different.

## Verified Candidate Records

### PixiJS

- Repository `https://github.com/pixijs/pixijs`; docs `https://pixijs.com/8.x/guides` and `https://pixijs.download/release/docs/index.html`.
- Licence MIT (`https://raw.githubusercontent.com/pixijs/pixijs/dev/LICENSE`).
- Latest release `v8.19.0`, 2026-06-04; most recent commit 2026-07-13.
- Compositing verified from the API reference: `Container` documents `mask`, `setMask` with channel options, `filters`, `zIndex`, `sortableChildren`, `sortChildren()`, `blendMode`, `alpha`. `ExtractSystem` provides `canvas()`, `base64()`, `image()`, `pixels()`, `download()`.
- **No skeletal system in core.** The mesh guide documents `Mesh`, `MeshSimple`, `MeshRope`, `MeshPlane`, `PerspectiveMesh` — free-form and grid deformation only.
- **Headless Node execution is not in core.** It requires the userland package `pixijs-userland/node`, which is outside the `pixijs` organisation, has 49 stars, was last pushed 2026-04-19, does not state its supported PixiJS version, requires native `gl` and `canvas` with a Homebrew dependency chain on macOS, and whose README advises using `xvfb` as a virtual frame buffer in headless environments.
- Determinism: not verified. No documentation asserts reproducible pixel output. There is no timeline concept, so frame addressing would be RigTale's responsibility.
- Audio: not in core; `pixijs/sound` is WebAudio and browser-only.
- Skeletal add-ons carry licence obligations. `@esotericsoftware/spine-pixi-v8` declares a non-SPDX `LicenseRef-LICENSE`; the governing terms require that "each user of the Products must obtain their own Spine Editor license". As with Remotion, this is a downstream-user obligation rather than a block on RigTale's redistribution — but it is a heavier one, because it requires a paid **authoring tool** to produce assets at all, which conflicts with RigTale's premise that users supply their own layered artwork. Recorded as a cost and workflow risk for `RGT-D010`. `pixijs-userland/spine` is `NOASSERTION` and was last pushed 2025-03-24. `DragonBones/DragonBonesJS` is MIT and was last pushed 2026-01-23, but has 82 open issues and no verified PixiJS v8 binding.
- **Relevance: medium. Route to `SPIKE-R001`, not a dedicated review.** It is a drawing library, not a production system; the dedicated-review question reduces to the renderer question.

### Remotion

Licence position recorded above. Technical facts:

- Frame addressability is verified and is the best documented of any candidate: `--frames=0,30,60` for specific frames, `--frames=0-99,150-199` for concatenated inclusive ranges, `--every-nth-frame`; the Node API `frameRange` accepts a single frame, `[start, end]`, `[number, null]`, or a list of ranges; `renderStill({ frame })` renders one zero-indexed frame.
- Headless rendering is verified via `renderMedia()` with `browserExecutable` or `puppeteerInstance`.
- Audio support is substantial: trimming in frames, static or per-frame callback volume, pitch adjustment.
- **Determinism is enforced on the user, not guaranteed by the renderer.** The documentation states that because rendering runs on multiple threads and opens the page multiple times, `Math.random()` will not agree across threads; a seeded `random()` is provided instead. No page asserts bit-identical output across machines.
- No skeletal, bone, or mesh-deformation API exists. Layering, masks, camera, and parallax are inherited from DOM, CSS, and SVG with no Remotion-specific API.
- Latest release `v4.0.503`, 2026-07-31; pushed 2026-08-02. Actively maintained.

### Manim

Two real projects with different canonicity.

- **`ManimCommunity/manim`** is canonical for new users. Dual MIT: copyright 3blue1brown LLC in `LICENSE` and Manim Community Developers in `LICENSE.community`. Latest release `v0.20.1`, 2026-02-27; most recent commit 2026-08-02. Its README states the community version is recommended "for its continued development, improved features, enhanced documentation, and more active community-driven maintenance."
- **`3b1b/manim`** is canonical only for reproducing 3Blue1Brown videos. MIT. Commits are current (2026-07-31) but the last tagged release is `v1.7.2` from 2024-12-13 — roughly twenty months. Anyone pinning a release gets twenty-month-old code.
- **The addressing granularity is wrong for RigTale.** Verified from source (`manim/cli/render/render_options.py`), the only range flag is `-n, --from_animation_number`, which addresses **animation indices, not frames or timecodes**. `-s, --save_last_frame` saves only the final frame. There is no arbitrary frame-range or timecode flag.
- **No skeletal, bone, rig, or mesh-deformation class exists**, verified by inspecting `manim/scene/scene.py`.
- Audio is `Scene.add_sound(sound_file, time_offset, gain)` — sound attachment, not a mixed timeline.
- Camera, parallax, and `z_index` layer ordering could not be verified: the relevant documentation pages returned HTTP 429 on four attempts. The macOS support matrix is likewise not verified.
- **Relevance: low. Remove from the index.** The mismatch is architectural — a scene graph of mathematical objects addressed by animation index — and no renderer-level investigation changes it. Retain at most as prior art for code-as-direction API ergonomics.

### skia-canvas (`samizdatco/skia-canvas`)

- Repository `https://github.com/samizdatco/skia-canvas`; docs `https://skia-canvas.org`. Licence MIT.
- **Off-screen rendering is verified**: the project describes itself as "a Node.js implementation of the HTML Canvas drawing API for both on- and off-screen rendering". Windows are optional; a closed window's canvas can still export. Export API covers `toFile`, `toBuffer`, `toURL` and synchronous variants, in `png`, `jpeg`, `webp`, `raw`, `svg`, and `pdf`. A filename containing `{}` generates a numbered sequence, one file per page — directly relevant to frame-sequence output.
- macOS is documented as supported with prebuilt arm64 and x64 binaries.
- **Determinism risk is affirmative, not merely unverified.** The documentation states rendering is hardware accelerated by default, using Metal on macOS, with `.gpu = false` selecting software rendering. No output-parity guarantee between the two paths is documented. The project simultaneously markets serverless deployment, an environment with no GPU. The default path on RigTale's primary workstation therefore differs from the CPU path used in CI, with no documented parity.
- **Maintenance risk.** Latest release `v3.0.8`, 2025-09-25; most recent commit 2025-09-26. Roughly ten months with no commits, single maintainer. This is the least active candidate verified in this round.
- No skeletal system, no camera, no parallax, no audio. Layer ordering is draw-call order.
- **Relevance: high. Route to `SPIKE-R001` as a primary subject**, with the activity gap and the GPU/CPU parity question recorded as explicit risk items.

### node-canvas (`Automattic/node-canvas`)

- Repository `https://github.com/Automattic/node-canvas`. Licence MIT.
- **Cairo-backed, not Skia-backed.** Cairo ≥ 1.10.0.
- Latest release `v3.2.3`, 2026-03-31; most recent commit 2026-07-13. Materially more active than `skia-canvas`.
- Prebuilt binaries for macOS x86-64 and macOS aarch64.
- Designed for server-side Node use; no browser required.
- Determinism not verified, but the backend is a CPU rasteriser with no GPU path, which plausibly avoids `skia-canvas`'s parity risk. Requires executable confirmation.
- No rig, audio, camera, or timeline — same Canvas2D-only scope.
- **Relevance: high. Add to the index as a distinct row and evaluate in `SPIKE-R001` alongside `skia-canvas`.** Its absence from the index was a defect.

### Skottie (`google/skia` module)

- Repository `https://github.com/google/skia`; docs `https://skia.org/docs/user/modules/skottie/`. Licence BSD-3-Clause.
- **The cleanest frame-addressable primitive found in this round.** From `modules/skottie/include/Skottie.h`: `seekFrame(double t, ...)` updates state to a frame index, `seekFrameTime(double t, ...)` to a frame time relative to duration, with `render(SkCanvas*, const SkRect* dst)`, `duration()`, `fps()`, `inPoint()`, `outPoint()`, `size()`. The normalised `seek(SkScalar t, ...)` is deprecated. Direct seek then render, with no playback-state dependency, is exactly the primitive isolated shot rerendering requires.
- **But it is a player, not an authoring runtime.** It consumes Lottie/Bodymovin JSON derived from After Effects. Adopting it would mean adopting Lottie as RigTale's intermediate representation, which is a far larger architectural commitment than choosing a renderer, and one RigTale has explicitly not made.
- Lottie carries transform hierarchies and mattes but has no skeletal system. Layer, matte, and mask modelling was not verified from a Skia primary source in this round.
- Determinism is not asserted anywhere in the documentation. macOS support is not explicitly verified. Node consumption requires C++ FFI or the WASM build.
- **Relevance: medium. Route to `SPIKE-R001` as an API design reference, not a build target.** If Lottie-as-IR is ever considered, it warrants its own spike at that time.

### CanvasKit (`canvaskit-wasm`)

- Docs `https://skia.org/docs/user/modules/canvaskit/`; package `canvaskit-wasm` v0.41.1, BSD-3-Clause. Publish date not verified.
- **Node.js support is not merely unverified — it is absent from the official documentation.** The quickstart is browser and HTML-canvas oriented and does not mention Node at all. The CommonJS entry point suggests Node loadability, but that is inference.
- `MakeSWCanvasSurface` provides a documented software-rasterisation path, which is the determinism-relevant hook. No determinism claim accompanies it.
- Still at `0.x`, which is a stability signal.
- **Relevance: medium-low. Route to `SPIKE-R001` as a fallback below `skia-canvas` and `node-canvas`.**

## Cross-Candidate Conclusion

**No candidate verified in this round has native reusable character rig, skeletal, or bone support.** PixiJS, Remotion, both Manim projects, `skia-canvas`, `node-canvas`, Skottie, and CanvasKit all lack it. The only skeletal options are third-party: Spine, which carries a per-user paid editor obligation, and DragonBonesJS, which is MIT but has no verified PixiJS v8 binding.

**Working hypothesis, not a decision:** RigTale should expect to build its rig system rather than obtain it by choosing a renderer. If that holds, the value of low-level, unopinionated drawing surfaces rises relative to opinionated frameworks. This must be tested against the source-inspected candidates — Godot has a complete 2D cutout rig model — and settled by `SPIKE-A001` and `SPIKE-R001`, not here.

## Contradictions Between Presentation and Documentation

Recorded because each one would have misled a checklist-based screening.

1. **Remotion** presents as mainstream open source and is not. See the licensing finding above.
2. **Spine's PixiJS runtime**: the `spine-runtimes` repository lists supported runtimes with no PixiJS entry, while npm publishes `@esotericsoftware/spine-pixi-v8` self-described as "The official Spine Runtimes for PixiJS v8." One is stale. The licence is the blocker regardless.
3. **`skia-canvas`** markets serverless deployment while defaulting to GPU rendering with a platform-specific backend, with no documented parity between the GPU and CPU paths.
4. **Activity signal inverts reputation.** The likely intended "Skia Canvas" candidate has had no commits for roughly ten months, while the ostensibly older `node-canvas` committed in July 2026.
5. **`3b1b/manim`** commits are current but its last tagged release is twenty months old.

## Facts That Could Not Be Verified

- Manim's platform and macOS support matrix, its `Camera` API, parallax, and `z_index` layer ordering — `docs.manim.community` returned HTTP 429 on repeated attempts.
- `canvaskit-wasm` publish date.
- `@pixi/node`'s supported PixiJS version.
- Whether `@pixi/node` renders on macOS arm64 without a virtual frame buffer.
- Skia/Skottie's macOS support as an explicit documented claim.

Each remains an open question rather than an assumption.
