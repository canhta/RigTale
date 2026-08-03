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
- Skeletal add-ons carry licence obligations. `@esotericsoftware/spine-pixi-v8` declares a non-SPDX `LicenseRef-LICENSE`; the governing terms require that "each user of the Products must obtain their own Spine Editor license". As with Remotion, this is a downstream-user obligation rather than a block on RigTale's redistribution — but it is a heavier one, because it requires a paid **authoring tool** to produce assets at all, which conflicts with RigTale's premise that users supply their own layered artwork. Recorded as a cost and workflow risk for `RGT-D010`. `pixijs-userland/spine` is `NOASSERTION` and was last pushed 2025-03-24. `DragonBones/DragonBonesJS` is MIT and was last pushed 2026-01-23, and has 82 open issues.

  **Correction.** An earlier draft of this line added "and no verified PixiJS v8 binding." That was wrong and is refuted by the clone at the pinned commit `64b6c69a`: `Pixi/8.x/` exists with `src/`, `libs/`, `out/`, and its own `package.json`, and the commit that created it is titled `add pixi 8 runtime` (2025-05-24). The claim was made from search-index signals rather than from the source that had already been cloned, and it wrongly weakened PixiJS's skeletal story in this record. The 2026-01-23 date is defensible — it is the tip of `origin/6.0.2` — and the fact that nobody followed that date to that branch is the same defect that produced the withdrawn "DragonBones is dead" verdict in its review record.
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

## Determinism: The Renderer Evidence

Determinism is graded on what each project's own test infrastructure asserts, not on what it claims. Ranked by strength of evidence.

### resvg and tiny-skia — claim corrected against source

**This section previously read "the strongest evidence found" and concluded "This is the most credible determinism posture in the entire screening round." Both are withdrawn.** The original claim was made from documentation and search results **without cloning or reading the source**, in a screening round whose own rule is that documentation is a discovery signal and not sufficient technical evidence. It was the top-ranked determinism candidate in `TODO.md`, and it was the one candidate whose central claim was never source-inspected.

Verified directly at `linebender/resvg` commit `68b14c4c3bccdb60344c777406486b54c36ec1a4`:

**1. The comparison is tolerance-based, not byte-exact.** `crates/resvg/tests/integration/main.rs:152` sets `const DIFF_THRESHOLD: u8 = 1;`, and `:213-226` defines:

```rust
fn is_pix_diff(pixel1: &Rgba<u8>, pixel2: &Rgba<u8>, threshold: u8) -> bool {
    if pixel1.a == 0 && pixel2.a == 0 {
        return false;
    }
    let mut different = false;
    different |= pixel1.r.abs_diff(pixel2.r) > threshold;
    // g, b, a identical
    different
}
```

`assert_eq!(render(...), 0)` therefore means "no pixel differs by **more than** 1/255 on any channel." Every pixel may differ by ±1 on every channel and the test still passes. **Fully transparent pixels are exempted from comparison entirely** — RGB under zero alpha is never checked, which for a layered cutout compositor is precisely where premultiplication defects hide.

This collapses the comparative ranking built on it. resvg sits on the **same axis** as candidates ranked beneath it — Blender's 4/255 at 1%, ThorVG's max-diff 5 — merely tighter. Vello was demoted in this same document for a stated tolerance of 1–2 on its CPU paths; resvg's is 1 and was described as zero.

**2. The suite never runs on macOS.** `.github/workflows/` contains exactly `main.yml` and `tagged-release.yml`. In `main.yml`, `cargo test --all --release` appears in exactly one job (`build`, line 41), which is `runs-on: ubuntu-latest`. The `windows` job runs `cargo build` only. **There is no macOS runner anywhere in the project.** RigTale's primary and currently only supported platform has zero upstream evidence of reference-matching output — the exact gap for which Vello was demoted, except Vello documented its Apple divergence and resvg has never looked.

**3. Two facts the original screening did not record.** resvg has no animation support and states it has no plans to add any (`README.md:75`), so using it means serialising and re-parsing a complete SVG document per frame — roughly 5,040 times for the benchmark production, a per-frame cost never estimated for the top-ranked candidate. And its goldens are self-baselines: `crates/resvg/tests/README.md` describes the directory as "a collection of SVG files used during *resvg* regression testing." That establishes self-consistency across commits, which is what regression testing is for; it is not evidence of correctness or of cross-platform reproducibility.

**What survives.** resvg/tiny-skia remains a strong candidate: CPU-only with no GPU driver variance, permissively licensed, very active, and a ±1/255 tolerance with one explicitly quarantined SIMD case is genuinely tighter discipline than its peers. **What does not survive is the superlative and the ranking derived from it.**

`RGT-S013` is re-scoped accordingly: the question is no longer only "does determinism hold with unpinned fonts" but **"does resvg reproduce its own Linux goldens on macOS arm64 at all."**

### Verified facts

`https://github.com/linebender/resvg` (Apache-2.0 OR MIT) and `https://github.com/linebender/tiny-skia` (BSD-3-Clause). Both moved owner: `RazrFalcon/resvg` now redirects to `linebender/resvg`. Among the most active projects surveyed — resvg v0.48.0 released 2026-08-02, tiny-skia last committed 2026-07-31.

**CPU-only rasterisation.** tiny-skia is a pure-Rust subset of Skia; resvg renders into its pixel buffer. No GPU, therefore no driver variance. Inherently headless, with a library, a C API, and a CLI.

**Golden-image tests.** `crates/resvg/tests/integration/render.rs` contains roughly 1,600 generated tests of the form `assert_eq!(render("tests/filters/feBlend/mode=multiply"), 0);`, where the function returns the count of pixels differing by more than 1/255 on any channel. One radial-gradient focal-point case is quarantined in the generator's ignore list as a SIMD rounding difference.

**Caveat:** text rendering depends on the resolved font set, so reproducibility requires pinning fonts. The harness does exactly that with a fixed font database. Cross-machine text determinism with unpinned system fonts is unproven.

### Vello — documents non-exact output on Apple platforms

`https://github.com/linebender/vello` (Apache-2.0 OR MIT), v0.9.0 released 2026-05-15, very active. The README self-describes the project as "in an alpha state".

`vello_tests/README.md` states verbatim that snapshot tests "have a non-exact comparison metric, because of small differences between rendering on different platforms. **This includes differences from 'fast math' on Apple platforms.**"

**That is a documented admission that GPU output is not bit-identical across platforms, naming RigTale's primary target explicitly.**

The CPU path is not bit-exact either: the test macros set default tolerances of 2 for the u8 CPU path and 1 for SIMD and hybrid, with only the f32 CPU path at zero.

A new `vello_cpu` crate published 2026-07-29 is the path that avoids GPU-driver variance and is worth re-evaluating when the project exits alpha. **For now, the documented Apple divergence is a known disqualifier for the GPU path and must be recorded as such.**

### ThorVG — ships a non-reproducibility detector

`https://github.com/thorvg/thorvg` (MIT), v1.1.0 released 2026-07-22, committed 2026-08-01. Very active, and its headless and frame-addressable capabilities are real and documented.

But it makes no reproducibility claim, and its regression tooling argues against assuming one. `test/regression/settings_comparison.toml` uses a maximum-difference threshold of 5 — similarity, not exact match — comparing a branch build against a development build rather than against golden references. More tellingly, `test/regression/check_same_image_size.py` renders the same input repeatedly and compares output file sizes, emitting the message "POSSIBLE_PROBLEM - Converting svg to png is not reproducible".

**A project that ships a run-to-run non-reproducibility detector has, by construction, experienced run-to-run non-reproducibility.** Determinism is not verified; RigTale must measure it before trusting it.

### Others

**Cairo** (LGPL-2.1 or MPL-1.1, note MPL **1.1** not 2.0) releases roughly annually, most recently 1.18.4 on 2025-03-08. No determinism statement exists anywhere in the repository — a grep of the full clone at `bd04e43e` for "deterministic\|reproducib" returns zero hits. No test-suite evidence located.

**Blend2D** (Zlib) is a fast CPU rasteriser, but it is "Powered by a JIT Compiler" — runtime code generation specialised per detected CPU feature set is a structural determinism concern. Flag, do not adopt blind.

**Skia** (BSD-3-Clause) has a CPU backend but is heavyweight to build or vendor for a solo maintainer. tiny-skia is the pragmatic subset.

## Structured Animation State: Theatre.js

`https://github.com/theatre-js/theatre`. **Dual-licensed, and the split matters:** `@theatre/core` is Apache-2.0, `@theatre/studio` is **AGPL-3.0-only**. The README states that a project's final bundle includes only the core, so only Apache applies. That is favourable — RigTale would never ship the editor — but the trap is invisible from the repository's top-level licence badge.

**The state format is genuinely data.** `packages/core/src/types/private/core.ts` defines a persisted tree of projects, sheets, static overrides, and a positional sequence carrying **`length`** — duration is a **stored field, not computed by running the animation**. Keyframes are `{id, value, position, handles, connectedRight, type}`. A real on-disk instance in the playground is plain JSON with a `definitionVersion`.

**This directly contrasts with Motion Canvas and Revideo**, where duration is discoverable only by executing the animation. Theatre.js demonstrates the property RigTale requires is achievable in a JavaScript timeline library.

`sequence.position` is a real getter and setter documented as the current time in seconds — arbitrary-time seek.

**Two limitations:**

1. **There is no public keyframe-authoring API in the Apache-2.0 core.** Keyframe mutation lives in the AGPL studio. RigTale's write path would be to emit the JSON directly, then load it. Issue 506 confirms this and was closed without rebuttal.
2. **There is no shipped runtime schema validation.** The schema is declarative and typed, but RigTale would supply its own validator.

**Maintenance: dormant.** The core's last release was 0.7.2 on 2024-05-19; the last public commit was 2024-04-11, adding a notice that development moved temporarily to a private repository for a 1.0 rewrite. A community issue asking whether the project continues has been open since 2025-05-14, with a maintainer reply only via a screenshotted chat message. Every repository in the organisation is stale.

**Net: the format is excellent and RigTale can own it independently of upstream. The project is a single-maintainer bet with a two-year-invisible rewrite.** Take the schema shape; do not take the dependency.

## XDTS — The Most On-Thesis Format Discovered

Implemented inside OpenToonz at `toonz/sources/toonz/xdtsio.h` and `.cpp`, read and written through Qt JSON types — **it is JSON**.

The field vocabulary is literally animation direction: cell numbers, a dialogue field documented as "speaker names and line timing", and a camerawork field documented as "camerawork instructions", under a header carrying cut and scene.

This is the Japanese industry's exchange digital time sheet — **structured production direction as data for fixed-cast 2D cel and cutout animation.** It is the closest existing standard to what RigTale proposes to generate, and it was absent from the candidate index entirely.

Routed to `SPIKE-A001` as a contract-design reference.

## Licensing Red Flags From This Round

1. **GSAP is the highest-severity flag.** Its licence changed on 2025-04-30 to a "Standard 'no charge' GSAP License" with **no SPDX identifier** — the npm manifest declares a URL, not a licence id — and it is **not OSI-approved**. It contains **no redistribution or sublicensing grant at all**, which is a gap for a project that must be redistributable. Its field-of-use restriction prohibits use in "tools that allow users to build visual animations without code" that compete with a named vendor's visual animation building. **RigTale is such a tool.** Whether it competes with that vendor is arguable; the clause lands uncomfortably close. GSAP is also imperative code, so it fails RigTale's data standard independently. **Drop.**
2. **`@theatre/studio` is AGPL-3.0-only** while the core is Apache-2.0.
3. **`python-lottie` is AGPL-3.0-or-later** — the most convenient Lottie writer is copyleft-viral.
4. **Several agentic research repositories ship no licence file at all** and are therefore all rights reserved by default. Cite in prose; never vendor.
5. **Two candidates are PolyForm Noncommercial 1.0.0** — not open source, incompatible with RigTale's redistribution requirement.
6. **`Samsung/rlottie` reports no assertion**: its manifest says "basically MIT" with per-directory carve-outs including Skia. Requires a per-directory audit.

## anime.js — Rejected on the Same Grounds as Motion Canvas

MIT (`LICENSE.md`), genuinely healthy — v4.5.0 released 2026-06-22, zero runtime dependencies. But definitions are imperative, and `timeline.call(callbackFunction, position)` embeds arbitrary executable callbacks. There is no JSON representation and no documented way to obtain total duration without construction.

**Identical failure mode to Motion Canvas and Revideo. Rejected on the same basis, despite a clean licence and active maintenance.** Recorded to show the criterion is applied consistently rather than selectively.

## Screening Claims Rejected on Cross-Verification

Documentation-level screening produced three claims that contradict evidence obtained by direct source inspection of the pinned clones. Source inspection wins in each case. Recorded so the rejected claims are not reintroduced.

| Rejected claim | Contradicting evidence |
|---|---|
| "Code2MP4 is likely a mis-recorded name; no such project was found, and the index probably means `showlab/Code2Video`." | Code2MP4 exists and was inspected at commit `91d7ba45`. Its declared repository, `NOTICE`, `LICENSE`, and workspace are recorded in `docs/research/repository-reviews/code2mp4.md`. `showlab/Code2Video` is a **separate, additional** candidate, not the same project. |
| "The Revideo-as-Motion-Canvas-fork lineage is not substantiated; its README says it is zero-dep and borrows concepts from Remotion and Rive." | Source inspection at commits `7b91435c` and `b5de67a0` found byte-identical `LICENSE` files — Revideo's still reads "Copyright (c) 2022 motion-canvas" — identical `commitlint.config.js`, `tsdoc.json`, and workspace layout, and `packages/renderer/server/render-video.ts:16` importing the Vite plugin under the upstream binding name. A README self-description is a discovery signal; the licence file and import graph are evidence. |
| "The OpenMontage index entry points at the wrong repository and the licence field may be wrong." | The inspected clone is `calesthio/OpenMontage` at commit `c36e4122`, and its `LICENSE` was read directly: GNU AGPL v3, confirmed at `README.md:755`. The index is correct. |

The third claim did surface something real: near-identical copies of OpenMontage exist at other organisations advertising different licences and different feature counts. That is a reason to keep citing exact commits, not a reason to change the index.

**Star counts and fork counts from this screening round are not recorded as evidence.** Several were unobtainable due to API rate limiting, several conflicted between sources, and none bear on whether a candidate meets a RigTale requirement.

## Facts That Could Not Be Verified

- Manim's platform and macOS support matrix, its `Camera` API, parallax, and `z_index` layer ordering — `docs.manim.community` returned HTTP 429 on repeated attempts.
- `canvaskit-wasm` publish date.
- `@pixi/node`'s supported PixiJS version.
- Whether `@pixi/node` renders on macOS arm64 without a virtual frame buffer.
- Skia/Skottie's macOS support as an explicit documented claim.

Each remains an open question rather than an assumption.
