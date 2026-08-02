# Repository Review: Synfig

**Screened under:** `SPIKE-C001` (`RGT-S001`), read-only static source inspection with full commit history.

**Repository:** https://github.com/synfig/synfig

**Inspected commit:** `eedebcfc4e4f18e638b14b2c3b8e996803730490` (2026-08-02). 12,512 commits since 2005-03-21. Declared version 1.5.5.

**Licence:** GPL-3.0 per `LICENSE`, `synfig-core/LICENSE`, `synfig-studio/LICENSE`, and the README — **but see the header discrepancy below.**

**Disposition:** `defer`, leaning `reference`.

## It Clears the Decisive Bar

Synfig satisfies the properties RigTale's architecture actually needs, and they are rare in combination.

**A genuine open-source saver exists in the core library.** `synfig-core/src/synfig/savecanvas.h:55-59` declares `save_canvas` and `canvas_to_string`; the implementation (`savecanvas.cpp:1029-1071`) builds an XML document and writes it **pretty-printed and indented**. The compressed variant is the same XML gzipped. The loader counterpart is at `loadcanvas.cpp:3151`.

**Round-tripping is a first-class supported operation, not a reverse-engineering exercise.** This is the property Rive lacked entirely and Inochi2D left half-finished.

**An external program demonstrably generates valid `.sif`.** The shipped plugin `synfig-studio/plugins/add-skeleton-simple/add-skeleton-simple.py` is an 82-line external Python program that splices a template's definitions and layers into a target file with id renaming. Crude line-level text munging — but shipped, working proof that an out-of-process generator is a supported pattern.

**The CLI is headless and renders arbitrary single times.** `synfig-core/src/tool/main.cpp` calls no GTK and no X11; `tool/CMakeLists.txt:24` links only the core library, which itself links only sigc++, glibmm, giomm, libxml++, FFTW, zlib, ltdl, threads, and intl.

Verified flags (`optionsprocessor.cpp:152-172`): target, width, height, threads, input, output, renderer, **canvas**, fps, **time**, begin-time, end-time. `--time` sets both ends of the range (`renddesc.cpp:369-374`), so total frames becomes one — **a genuine single arbitrary-time render.**

**Sequence numbering is absolute, not relative.** `modules/mod_png/trgt_png.cpp:115` seeds the counter from the range start, and filenames use that global index (`:149`). Re-rendering frames 240 to 360 writes correctly numbered files — exactly what isolated shot rerender needs.

**The renderer is CPU-only by construction.** The OpenGL subdirectory is **commented out of the build** (`rendering/CMakeLists.txt:19`), GL registration sits behind a disabled flag, and `configure.ac:380-384` explicitly special-cases Darwin to disable OpenGL. The default engine is software. **Best-case determinism substrate.**

**Randomness is seeded and serialised.** `quick_rng.h:43-60` is a plain linear congruential generator with an explicit seed setter, and noise layers expose a `seed` parameter stored in the file (`mod_noise/noise.cpp:402-404`). No wall-clock or entropy seeding in the render path.

## The Blocking Finding: Bones Do Not Cross Files

**Cross-episode rig reuse — an explicit RigTale requirement — is structurally unsupported.**

The bone registry is a file-static map keyed to the **root** canvas (`valuenode_bone.h:64-65`, `valuenode_bone.cpp:74,276`). `loadcanvas.cpp:3336-3337` errors with "Inline canvas cannot have a `<bones>` section". And **every stored bone identifier is XORed with the runtime root-canvas identifier on both write and read** (`savecanvas.cpp:665,731,755`; `loadcanvas.cpp:2575`), while canvases never persist their own identifier — so a bone reference from one file can never resolve in another.

There is no import-skeleton and no bind-foreign-bone mechanism anywhere.

**The available workaround changes the architecture.** External canvas references do work: `Canvas::surefind_canvas` resolves `file.sif#canvasid` with caching (`canvas.cpp:729-764`), a group layer's canvas parameter loads through that path, and the referenced file keeps its own bones — so an externally referenced rigged character animates correctly.

But that is **instancing a whole character file, not sharing a rig.** For RigTale that is a design decision requiring an explicit choice, not an assumption.

Intra-file rig duplication is supported via bone-aware clone remapping.

## A Smell Worth Recording

**No `.sif` anywhere in the repository contains a `<bones>` section.** More pointedly, `stickman.sif` — the asset behind a plugin literally named "Add Skeleton" — has zero bones. It rigs via 39 exported value nodes driving nested rotate, stretch, and translate layers.

**Synfig's own shipped skeleton tooling bypasses the bone system entirely.** The bone XML shape in this review had to be reconstructed from the encoders rather than read from an example. That is a strong signal the bone path is less exercised than the layer path.

## Rig Model

Two distinct weighting models exist.

**Explicit linear blend skinning.** `boneweightpair.h:51-68` pairs a bone with a weight, feeding a transform accumulation that sums weighted animated matrices and normalises by total weight (`valuenode_boneinfluence.cpp:233-269`).

**Automatic distance falloff.** `layer_skeletondeformation.cpp:283-297` is a grid mesh warp with 32 subdivisions by default, weighting by inverse square distance from a capsule falloff (`bone.cpp:221-225`).

`Layer_Skeleton` itself performs no deformation — it is a display gizmo excluded from rendering (`layer_skeleton.cpp:88`) that only holds the bone list.

Bones serialise in a section written before the definitions, **topologically ordered parents first**, and only for non-inline canvases (`savecanvas.cpp:953-966`).

## Format

Genuinely XML, human-readable, diffable, with a **six-year-stable writer** — 25 commits to the saver since 2020, all refactors, typo fixes, and old-version compatibility, with no breaking changes.

Root canvas attributes cover dimensions, resolution, gamma, frame rate, time range, antialiasing, view box, background, and focus. Children are definitions, bones, keyframes, metadata, name, description, author, and layers. Layers carry type, active, exclude-from-rendering, version, and description, with parameters holding either an inline value or a reference by relative id.

Value types number 22; animation uses waypoints with time, before and after interpolation, tension, continuity, and bias, over the vocabulary halt, linear, manual, constant, auto, and clamped. Roughly 60 converter node types and 57 layer types are registered, including group, switch, filter group, duplicate, skeleton, skeleton deformation, region, outline, text, import, and sound.

**There is no DTD, XSD, RelaxNG, or in-repo format specification. The loader is the specification.**

## Layers, Masks, Draw Order, Camera

Draw order is list order plus per-layer depth; the saver writes layers in reverse iteration order. Universal parameters are depth, opacity, and blend method.

**25 blend methods** are enumerated (`color/color.h:253-278`). Masking behaviour comes from the onto and straight-onto methods, which maintain the destination alpha, plus alpha and alpha-intersection.

Grouping exposes origin, transformation, **time dilation**, and **time offset** (`layer_pastecanvas.cpp:318`) — a usable reusable-clip primitive. A switch layer provides indexed layer selection, the natural cutout mouth and hand swapper.

**There is no camera layer.** The viewport is the canvas render description. **Parallax is achievable only by animating per-group transformations at different rates** — no depth-based camera exists.

## Time Model

`Time` wraps a **double of seconds** (`time.h:50-154`) — not rational, not frames. Comparison is quantised through a tick of 5e-5 with equality defined on rounded ticks (`:120-141`).

Serialisation is inconsistent by site: keyframes and canvas time bounds use a frame-aware string form, while **waypoints serialise as decimal seconds** (`savecanvas.cpp:448`). At 24 fps a frame-1 waypoint round-trips as `0.04166667s`, off by about 7e-10 seconds — well inside the tick, so ordering and equality are stable, but the on-disk text is not an exact frame index.

The render loop derives frame times by **interpolating across the range** rather than stepping by the reciprocal of the frame rate.

## Determinism: Favourable Architecture, Unverified Empirically

Positive: CPU-only by construction, seeded and serialised randomness, no entropy in the render path.

Negative: **no golden-image, frame-hash, or render-regression tests exist in this repository.** The 17 unit tests cover data structures and mathematics only. The render corpus lives in an **external** repository, and the script that uses it measures wall-clock time, not output correctness.

Residual risk: `rendering/renderqueue.cpp:101-115` spawns workers matching hardware concurrency over a task graph with per-task multithreading permission. **Whether one thread and eight threads produce byte-identical output is not verified from source.**

## Failure Mode That Matters Most for an Agent Pipeline

**The loader degrades silently.** `Layer::create` returns a mime placeholder for any unknown type name (`layer.cpp:179-182`), so a misspelled layer renders nothing with no error. Rejected parameters only warn and continue (`loadcanvas.cpp:3037-3041`).

**A malformed generated file can render a blank frame and exit zero.** For an agent-authored pipeline that is the worst possible failure mode, and it is the strongest single argument for RigTale validating its own output before handing it to any renderer.

A related instance: the video target silently rounds output dimensions to multiples of eight (`trgt_ffmpeg.cpp:126-127`), violating a resolution contract with no warning.

## Extension Surface

The plugin mechanism is confirmed to be essentially the whole story: `pluginmanager.cpp:574-655` spawns an interpreter with the script and file path. **Python is not embedded** — it is located on PATH. A newer contract adds an optional dialog and a JSON side-channel carrying canvas state (`:605-625`).

**Two hard limits:** the plugin manager lives in the GUI source tree, so **plugins are unavailable from the CLI**; and there are no callbacks, hooks, or event API.

There is a real alternative: the core is installed as a shared library with public headers and a CMake export target. No script bindings exist. So the supported programmatic surfaces are: write XML directly, drive the CLI, or link C++.

## Licence Discrepancy

The three licence files are byte-identical GPL version 3 texts, and the README claims GPL-3.0.

**But 1,267 source files carry headers saying "either version 2 of the License, or (at your option) any later version"**, and **zero files say version 3**. There are no SPDX identifiers anywhere.

Reporting file contents only, not legal advice: the discrepancy is a real question for a redistributing project. Note also that the video encoder is invoked as an **external binary via subprocess** (`trgt_ffmpeg.cpp:188-218`), not linked — a materially different integration shape from linking the core library.

## Maintenance Health

12,512 commits over 21 years, 162 authors all-time. **Last 12 months: 102 commits.** Last 24: 285.

Twenty-five distinct authors in the last year, but two identities are the same person accounting for **53 of 102 commits — 52%**, rising to 61% over 24 months. Everyone else contributed one to five commits. **Bus factor 1.**

**Activity is genuine engineering, not translation churn.** Classifying recent subjects: 33 fixes, 22 refactors and tests, 18 features, 13 build and documentation, **zero localisation**. Two releases shipped in the window. Format stability over six years is excellent.

Caveat: much recent feature work is GUI and tooling; core renderer and rig commits are sparse.

## macOS

**Apple Silicon is a gated CI target.** The workflow matrix includes two arm64 runners: one on autotools marked **required**, and a newer CMake leg — the only macOS leg that runs tests — marked **allowed to fail**. Packaging scripts and a macOS directory exist.

`configure.ac:380-384` explicitly disables OpenGL on Darwin, which incidentally guarantees the CPU renderer path there.

**A reported "unusable on Apple Silicon" issue could not be corroborated from source.** Searching the README, changelog, and legacy bug directory returns nothing relevant; the legacy tracker's four open entries are unrelated. That report would live in the GitHub issue tracker, which is not in this clone. Equally, no universal-binary handling was found, so the packaged build is presumably single-architecture — not verified from source which one.

## Patterns to Adopt or Adapt

- **Loader and saver symmetry as a hard invariant.** Ship both directions and a round-trip property test — the thing Synfig conspicuously lacks despite having both halves.
- **Definitions plus exported-node references with a relative-id scheme.** Clean, textual, human-auditable cross-file references — but use **stable names, never runtime-derived identifiers**.
- **A file-format version attribute plus a release enum with downgrade-on-save.** Cheap, effective compatibility in both directions.
- **Absolute frame indexing in sequence output.** RigTale's isolated shot rerender should do exactly this.
- **Explicit seed parameters on every stochastic node**, with seeds in the data.
- **Group-level time offset and dilation** as the reusable-clip mechanism.
- **A subprocess plugin boundary with a JSON side-channel** — language-agnostic, crash-isolated, and a copyleft-safe boundary rather than a linking one.
- **Addressable sub-scenes** as the shot-isolation primitive.
- **Topologically ordered serialisation** so single-pass loading never needs forward references.

## Patterns to Avoid

- **Runtime identifiers XORed into the file format.** This single decision is why Synfig rigs cannot be shared across files.
- **Lenient parsing that degrades silently.** A generated file that renders blank and exits zero is the worst failure mode for an agent pipeline.
- **Scoping a subsystem's registry to the document root**, which makes reuse structurally impossible later.
- **Time as a bare double with an epsilon-comparison bolt-on.** Use exact rational or integer ticks so equality is real equality.
- **Deriving frame times by range interpolation** instead of stepping from the start.
- **Shipping a rig feature that the project's own tooling routes around.** Do not build two rig models.
- **The format's only specification being its parser.**
- **Silent output-dimension coercion.**

## Questions Requiring Executable Evidence

| # | Question | Weight |
|---|---|---|
| 1 | Render the same file with one thread and eight, hash the output, and repeat-run for stability. | **Biggest unresolved determinism question** |
| 2 | Does a hand-authored bones section actually load? No example exists in-repo; the shape here is reconstructed from encoders. Build, load, save, diff. | Decisive |
| 3 | Does Synfig round-trip its own output byte-stably? Untested anywhere. | Decisive |
| 4 | Can an exported bone be referenced across files? The type system suggests no; this needs an experiment. | Gates rig reuse |
| 5 | Does the build complete on an M-series Mac, does the CLI render, and do tests pass? | High |
| 6 | Does `--time` render exactly the requested instant for a non-frame-aligned time, matching the corresponding frame from a range render? | High |
| 7 | Is skeleton deformation at 32 subdivisions production-acceptable for a cutout character, and at what per-frame cost? | `PR-R006` |
| 8 | Wall-clock for a 150–210 second multi-character render, and does sub-scene rendering scale? | `PR-R006` |

Items 1 to 3 are cheap and decisive. Route to `SPIKE-R001` (1, 5, 6, 7, 8) and `SPIKE-A002` (2, 3, 4).

## Conclusion

`defer`, leaning `reference`.

Synfig clears the decisive bar — a real saver, a diffable format, demonstrated external generation, a headless CLI with exact single-time rendering and absolute frame numbering, and a CPU-only renderer. For an agent-writes-data, deterministic-software-animates architecture those are exactly the right properties.

Three findings block a confident `adopt`. **Cross-episode rig reuse is structurally unsupported** because bones are keyed to the defining root canvas and referenced by identifiers that cannot resolve across files. **The bone system has no in-repo example and Synfig's own rigging plugin bypasses it.** And **determinism is architecturally favourable but empirically unverified** — no golden-image tests, no round-trip tests, and a multithreaded renderer of unknown output stability.

Secondary concerns: bus factor one, no schema of any kind, a loader that fails silently on generated-file mistakes, and a licence header discrepancy that a redistributing project must resolve.

Spikes 1 to 3 are cheap and decisive and should run before any further evaluation of alternatives.
