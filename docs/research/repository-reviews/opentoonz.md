# Repository Review: OpenToonz

**Screened under:** `SPIKE-C001` (`RGT-S001`), read-only static source inspection with full commit history.

**Repository:** https://github.com/opentoonz/opentoonz

**Inspected commit:** `5f6beab3fa31c81b74b4a92a6e1cca9193e749a4` (2026-08-02). 5,121 commits. Application version 1.8 (`toonz/sources/include/tversion.h:22-23`); scene-format version 71.1 (`toonz/sources/toonzlib/toonzscene.cpp:65`).

**Licence:** BSD 3-Clause core (`LICENSE.txt`, "Copyright (c) 2016 - 2026, DWANGO Co., Ltd."), with `thirdparty/` and the mypaint brushes carved out.

**Disposition:** `reference`, trending `adapt`. Escalation gated on four executable spikes.

## Why This Is the Most Significant Result of the Screening Round

OpenToonz answers RigTale's hardest question affirmatively.

**Exclusivity claim withdrawn.** This line previously read "and it is the only candidate that does so." A cross-record audit refuted it: `synfig.md` documents the same conjunction — a genuine in-tree saver (`savecanvas.h:55-59`), an external program that demonstrably writes valid `.sif` (an 82-line Python plugin), a headless CLI that calls no GTK or X11, `--begin-time`/`--end-time` range rendering, and **absolute** output-sequence numbering (`trgt_png.cpp:115,149`), which is precisely what isolated shot rerender needs. `mlt-glaxnimate-lottie.md` makes a comparable claim for MLT. The difference between OpenToonz and Synfig is licence (BSD-3 versus GPL-3) and rig portability, not the existence of the authoring path.

**A program can author a complete production scene — layers, hierarchy, rig, keyframes, camera, and effect graph — as human-readable text, with no GUI and no proprietary tool, and then render an arbitrary frame range headlessly. Both halves are BSD-3 and in-tree.**

That is RigTale's thesis, already shipped in a production tool.

## Programmatic Authoring: Yes, Decisively

`.tnz` is uncompressed, indented, human-readable, XML-like plain text.

The load-bearing fact is `toonz/sources/toonzlib/toonzscene.cpp:620`: `TOStream os(scenePathTemp, false);` — the second argument is `compressed`, explicitly false. The header at `toonz/sources/include/tstream.h:225` calls compression "verified to be unsafe… deprecated".

**Writer:** `ToonzScene::save` (`toonzscene.cpp:583`). Root tag at `:641` with `version` and `framecount` attributes, then children in fixed order: `generator`, `properties`, `levelSet`, `xsheet`, `history` (`:643-678`).

**Reader:** `ToonzScene::loadTnzFile` (`:434`), accepting root tag `"tab"` or `"tnz"` (`:442`), parsing the version (`:444-454`), then dispatching tag by tag with unknown tags throwing (`:455-502`). A hand-rolled recursive-descent parser, not an XML library.

Verified against a committed artifact written by the same serialiser: `stuff/studiopalette/Global Palettes/Default Palettes/Cleanup_Palette.tpl` is plain, indented, diffable text.

Scene structure is fully declarative. `TXsheet::saveData` (`toonz/sources/toonzlib/txsheet.cpp:1266`) writes columns, pegbars — the stage-object tree — effect nodes, column fan, notes, and navigation tags. **Drawings are not in the `.tnz`**; levels are external files referenced by path. A generator can author scene, rig, and animation as text while treating artwork as opaque assets, which matches RigTale's intended split exactly.

### Two complications a generator must handle

1. **It is XML-*like*, not XML.** Escaping is backslash-based, handling only backslash and quote (`toonz/sources/common/tstream/tstream.cpp:22-38`). A standard XML parser will not reliably read it.
2. **Object identity is assigned at write time.** `TOStream::operator<<(TPersist*)` (`tstream.cpp:561-580`) assigns monotonically increasing integer ids on first write and emits back-references thereafter. Cells reference levels by that id (`toonz/sources/toonzlib/txshlevelcolumn.cpp:232`), and cells are additionally run-length encoded as row, count, level, frame id, increment (`:193-235`). A generator must reproduce both.

## Headless Range Rendering: Real

`toonz/sources/tcomposer/tcomposer.cpp:602-615` declares the argument surface: a source file, `-o` target, `-range`, `-step`, `-shrink`, `-multimedia`, `-farm`, `-nthreads`, `-maxtilesize`, plus generated path qualifiers.

`RangeQualifier` (`toonz/sources/common/tapptools/tcli.cpp:736-756`) declares itself as `-range from to | -frame fr` and parses both forms. **`-range` renders a genuine arbitrary frame range**: `tcomposer.cpp:907-913` applies it over the scene's output range, and `generateMovie` (`:436-441`) converts to zero-based and clamps. Output frames are named from the **absolute scene frame** (`:289`).

That is precisely the isolated-shot-rerender primitive RigTale needs, already built and already using absolute numbering.

**But it is not GUI-free.** Line 655 constructs `QApplication`, not `QCoreApplication`; the build links Qt Gui, Widgets, and the Toonz Qt layer. The render path needs a GL context — `toonz/sources/common/tfx/trenderer.cpp:1430` creates a `QOffscreenSurface`, paired with a `QOpenGLContext` at `toonz/sources/common/tvrender/qtofflinegl.cpp:165-169`. Whether an offscreen platform plugin yields a usable GL context on macOS is unresolved from source.

**This is the gating question for the entire path.**

## The Cutout Rig Model

There is **no persistent rig object**. `Skeleton` (`toonz/sources/include/toonz/skeleton.h:24`) is a transient view built on demand from the column parenting graph (`toonz/sources/toonzlib/skeleton.cpp:54-113`) with no serialisation.

**The rig is the column parenting graph.** Persistence lives in `TStageObject::saveData` (`toonz/sources/toonzlib/tstageobject.cpp:1604-1661`): parent id, handle, parent handle, name, centre (pivot plus offset), status, then animatable channels written **only when non-default** (`:1632-1642`), plus cycle and plastic deformation.

Handle and parent handle are the attach points — centre or one of eight hooks (`toonz/sources/include/toonz/tstageobject.h:261-277`). **Hooks are stored on the level, not the scene** (`toonz/sources/toonzlib/hook.cpp:339`, invoked from `txshsimplelevel.cpp:1773`), capped at 99.

### Cross-scene rig reuse: partial and weak

Hooks travel with the level and are genuinely reusable. **The skeleton — hierarchy, pivots, handle assignments, and all animation curves — is embedded in the `.tnz` with no library, preset, or import format.** The only reuse mechanism imports another scene as a child level, which is a copy, not a link.

`[INFERENCE]` For RigTale this is tractable precisely because the format is text: per-episode rig reuse would be implemented by RigTale emitting the stage-object subtree from its own canonical rig data. But it is RigTale's work, not something inherited.

This also independently corroborates the workflow finding that rig reuse across episodes is unsolved by existing tools — see `docs/research/small-studio-workflow.md` section 5.

## Plastic Mesh Deformation

Mesh geometry is a separate level type with per-vertex rigidity (`toonz/sources/include/tmeshimage.h:43-50`). The rig is `PlasticSkeleton` (`toonz/sources/include/ext/plasticskeleton.h:100-105`), a persistable mesh whose vertices carry name, number, parent index, angle limits, and an interpolate flag (`:62-96`).

Animation is `PlasticSkeletonDeformation` (`toonz/sources/include/ext/plasticskeletondeformation.h:186`), serialised inline into the `.tnz` (`tstageobject.cpp:1645`). Per vertex it animates exactly three channels — angle, distance, and stacking order — each a keyframed parameter (`:53-63`).

**Vertices are keyed by name and hook number, not index** (`:85-92`), explicitly so keyframes survive being pasted onto a different skeleton. Multiple skeletons per deformation are switchable over time (`:238`).

**This is the single best idea in the codebase for RigTale.** Name-keyed deformation is exactly what makes reusable motion survive rig revision — the failure mode documented in the Harmony workflow evidence.

## Layers, Masks, Camera, Parallax

Layers are xsheet columns with typed variants including mesh columns (`toonz/sources/include/toonz/txshcolumn.h:109-116`). Persisted per column: status word carrying preview-visible, camstand-visible, locked and masked flags, opacity, filter colour, cells, and effects.

**Masks are a trap.** `TXshColumn::isMask()` (`toonz/sources/toonzlib/txshcolumn.cpp:685`) is consumed in exactly one place — `toonz/sources/toonzlib/stage.cpp:719`, the viewer visitor. It does not appear in `scenefx.cpp`. **The final render path does not honour column masks.** Compositing masks must be built from effect nodes, of which 135 are registered.

Camera is a stage object serialising size, resolution, X prevalence, and interest rect (`toonz/sources/toonzlib/tcamera.cpp:145-151`), animating through the same channels as any column. Multiple cameras are supported.

**Parallax is native.** Z accumulates through the parent chain (`tstageobject.cpp:1423-1426`), and a no-scale-Z compensation (`:1443-1444`) lets a layer be pushed in Z without changing apparent size. Stacking order is a separate animatable channel.

## ToonzScript Is a Dead End

The engine is Qt Script (`toonz/sources/toonzlib/scriptengine.cpp:180`), a hard required dependency (`toonz/sources/CMakeLists.txt:291`). **Qt removed QtScript in Qt 6.**

There is a non-menu entry point, but it is an extension sniff on the main application's positional argument (`toonz/sources/toonz/main.cpp:481`), not a flag. Three killers: the full GUI object graph is constructed *before* the script branch (`:676`); the success path returns 1, identical to both failure paths (`:695`, `:710`, `:716`), so automation cannot branch on the exit code; and there is no script flag or script-runner target anywhere.

The API surface (`toonz/sources/toonzlib/scriptbinding.cpp:164-194`) can create and load levels, insert columns, and set cells. **It cannot touch stage objects, keyframes, camera, frame rate, the effect graph, or output properties.** No sample scripts and no scripting documentation ship in the repository.

**Direct `.tnz` emission is the viable path; ToonzScript is not.**

## Determinism: No Guarantee, With Evidence Against

- **No hashing or checksumming of output.** The only matches are temp-filename generation.
- **No golden or reference-image comparison, no image diff, no regression harness.**
- **Unseeded global `rand()` in a render-reachable path**: `toonz/sources/toonzlib/tcenterlinevectorizer.cpp:79-87` perturbs stroke extremities; `tcenterlineskeletonizer.cpp:612` uses it for tie-breaking.
- **Three effects call `srand()` on global state mid-render** (`sandor_fxs/patternmap.cpp:218`, `sandor_fxs/calligraph.cpp:159`, `stdfx/iwa_soapbubblefx.cpp:825`) — a cross-effect side effect.
- **Thread count defaults to host CPU count** (`toonz/sources/toonzlib/outputproperties.cpp:42`, mapped at `tcomposer.cpp:930`) **and is persisted per scene** (`sceneproperties.cpp:268`). The same scene file renders with different thread counts on different machines.

Counter-evidence: a seeded random class exists (`toonz/sources/include/trandom.h:20`), modern effects expose a `random_seed` parameter, and the ToonzScript renderer pins threads to 1 — the only place that does.

## Test Strategy: None

**There are no automated tests.** No CTest, GoogleTest, Catch2, QTest, or boost.test anywhere; no first-party tests directory. CI runs no tests. Testing is manual and GUI-driven per `doc/how_to_test_prs.md`.

A bespoke harness exists and is dead: `toonz/sources/include/ttest.h:19-41` declares a test base class, and `ttest.cpp` implements a registry with **golden-comparison helpers for rasters, vector images, levels, and palettes** (`ttest.h:45-51`). It is compiled into the base library and has **zero subclasses**; the runner is never called. Someone intended render-regression testing and abandoned it.

Two orphaned files remain in tree, one including a pre-standard header that cannot compile today.

**1,076 first-party source files with no automated verification.**

## Maintenance Health: Healthy

From full git history: 5,121 commits, 3,508 non-merge on HEAD, 144 distinct authors all-time.

- **Last 12 months: 378 non-merge commits, 22 distinct authors.**
- Last 24 months: 707 commits, 29 authors.
- **Recent bus factor:** top author 43%, top two 63%.
- **Historical succession already demonstrated:** the all-time top contributor at 30% is now 7% of recent work. The project survived a maintainer handover.
- Cadence is continuous, not bursty-then-dead: every month from 2024-10 through 2026-08 has commits.
- Work is real: of 378 recent subjects, 153 are fixes, 48 additions, 35 features, 24 refactors, against 5 translation and about 15 CI commits. **v1.8.0 shipped 2026-06-19.**

This is materially healthier than any other rig-capable candidate screened.

## macOS: Apple Silicon Is Unbuilt Upstream

`.github/workflows/workflow_macos.yml:37` targets an Intel runner, with a comment stating it "will be the last available x86_64 image" and a TODO to move to Apple Silicon **on or before August 2027**. Deployment uses the Intel Homebrew prefix; released disk images run under translation. History shows two retreats from arm64 in 2024 and 2025.

No architecture, deployment-target, or universal settings appear in any build file. `toonz/sources/CMakeLists.txt:215` adds an i386 define unconditionally on macOS, `:219-220` passes an x86 flag to clang, and `:621-623` adds a define that makes `toonz/sources/common/tsystem/cpuextensions.cpp:12-16` **falsely report SSE support on Apple Silicon**.

**Mitigating:** all SSE intrinsics are gated behind Windows-and-x64 (`toonz/sources/common/trop/tresample.cpp:21-27`), one SSE block is commented out entirely, and all inline assembly is MSVC-only. No intrinsics reach a macOS compile; arm64 would take scalar paths — correct, slower.

**The actual blocker is one vendored binary.** `thirdparty/superlu/libsuperlu_4.1.a` is a universal binary with i386 and x86_64 slices and **no arm64 slice** — the only prebuilt archive in `thirdparty/`. The CMake finder already prefers the Apple Silicon Homebrew path, but `superlu` is **absent from the Homebrew install line in both the build documentation and CI**. Following the documentation on an M-series Mac hits exactly the linker error recorded in the 2024 retreat commit.

Qt is pinned to Qt5, and Homebrew's Qt5 is end-of-life upstream.

## Patterns to Adopt or Adapt

- **Direction-as-data, validated in production.** An entire scene as diffable text with artwork as external referenced assets.
- **Version attribute on the root tag with tolerant, tag-dispatched parsing**, including legacy attribute-name acceptance (`tcamera.cpp:158-161`). Cheap compatibility in both directions.
- **Write only non-defaults** (`tstageobject.cpp:1632-1642`), so files stay small and diffs show only authored intent.
- **Atomic save**: write to a temporary path, verify status, then rename (`toonzscene.cpp:603-686`).
- **Run-length cell encoding** as row, count, level, frame id, increment — compact and readable for held and stepped cutout timing.
- **Key deformations by vertex *name*, not index.** The single best idea here for RigTale's reusable-motion requirement.
- **Handle and parent-handle attach points** separating where a thing attaches on its parent from the transform — the right abstraction for prop and hand interactions.
- **`-range from to` and `-frame fr` with absolute output frame numbering** as the render CLI contract.
- **Explicit `random_seed` parameters** — but on *every* stochastic node, not some.

## Patterns to Avoid

- **Write-time integer object ids.** Use stable authored or content-addressed names so diffs are semantic and merges are possible.
- **A custom XML-like dialect with backslash escaping.** Use a real format any language can read without a bespoke parser.
- **Two parallel rig systems** — column-parenting bones and plastic mesh — with no shared abstraction.
- **A feature honoured in the viewer but not the renderer.** Preview and final must share one evaluator; this is `PR-R003` stated as a concrete failure.
- **Global seeding inside render nodes.** Thread a seed through explicitly.
- **Execution policy persisted in the document.** Thread count in the scene file makes output machine-dependent.
- **A test framework with no tests**, and dead files left in tree.
- **A registered writer that writes nothing.** `TLevelWriterPsd` is declared and registered, and `TLevelWriterPsd::save()` has an empty body (`toonz/sources/image/psd/tiio_psd.cpp:189`), so PSD export presents as supported and silently produces no data. Found by `RGT-S014`. It is a concrete instance of the screening failure mode this repository has twice had to correct: a capability that exists in the declaration and not in the implementation.
- **Success exit code 1.**
- **A rig that lives only inside the scene**, with copy-import as the only reuse path.

## Questions Requiring Executable Evidence

| # | Question | Weight |
|---|---|---|
| 1 | Does `tcomposer` run on macOS without a logged-in window server, given `QApplication` plus an offscreen surface and GL context? | **Gates everything** |
| 2 | Will a machine-generated `.tnz`, with correct object-id bookkeeping, load without error and render identically to a GUI-saved equivalent? Round-trip generate, render, open, save, diff. | Decisive |
| 3 | Is output byte-stable across two runs on one machine, and across one thread versus all, for a cutout scene with no particle or vectoriser effects? | Decisive |
| 4 | Does `-range 40 60` on a 200-frame scene produce exactly those frames with correct absolute filenames, and does frame 40 match the same frame from a full-range render? | Decisive for isolated rerender |
| 5 | Can it be built on Apple Silicon after installing SuperLU, given the i386 define and x86 flags? What is the cost of a native build? | High |
| 6 | Can a plastic deformation authored in one scene be transplanted into another by copying the subtree, given name-keyed vertices? | High |
| 7 | Per-frame render cost at 1080p for a multi-character cutout frame, and does roughly 4,500 frames fit a solo-maintainer machine budget? | `PR-R006` |
| 8 | Does column-mask state survive a round-trip and silently no-op at render, confirming masks must be effect-based? | Medium |

Route to `SPIKE-R001` (1, 3, 4, 7), `SPIKE-A002` (2, 6, 8), `SPIKE-I001` (5).

## Conclusion

`reference`, trending `adapt`.

OpenToonz answers the authoring question affirmatively **and** ships a headless range renderer with the exact semantics RigTale needs. Synfig and MLT satisfy comparable conjunctions; OpenToonz is distinguished by licence (BSD-3, almost no per-file exceptions), a production-proven cutout model, native parallax and multi-camera, and genuinely healthy multi-author maintenance with a demonstrated succession — not by being alone. The earlier "only candidate" framing is withdrawn.

### Per-layer render separation: `-multimedia`

**Recorded after an audit found this flag transcribed but never analysed.** The CLI surface section lists `-multimedia` as "Multimedia rendering mode" and stops there. In source it is a per-layer render path:

- `tcomposer.cpp:485,491-492` reads `outputSettings.getMultimediaRendering()` and, when set, constructs `MultimediaRenderer` instead of the normal movie renderer.
- `include/toonz/multimediarenderer.h:49` declares `class DVAPI MultimediaRenderer final : public QObject`, whose `Listener` interface is column-scoped throughout: `onFrameCompleted(int frame, int column)`, `onFrameFailed(int frame, int column, ...)`, `onSequenceCompleted(int column)`.
- `tcomposer.cpp:504-505` sizes the output by `getFrameCount() * getColumnsCount()`.

A column in OpenToonz is a layer. This is **headless per-layer render separation under BSD-3**, reachable from the command line. `blender.md` claims per-layer render separation as a capability "no other candidate has" and lists it among four capabilities that make Blender "the only surveyed system"; that claim is false, and this is the counter-evidence. It also bears directly on `PR-F003`'s textless-master obligation, which requires that on-screen text be renderable separately from picture.

This does not close the gating question: `-multimedia` runs through the same `tcomposer` path whose headless viability on macOS is unproven and is `RGT-S012`.

It is not adoptable as-is, for structural reasons: no automated tests against 1,076 source files, demonstrable non-determinism including machine-dependent thread count baked into the document, a renderer that constructs a GUI application object and needs a GL context, a scripting layer that cannot reach keyframes or cameras, and no upstream Apple Silicon build.

**Adopt the ideas now** — text scene format, name-keyed deformations, handle attach points, the range-CLI contract, atomic save, write-only-non-defaults. **Escalate to `adapt`** — RigTale emits `.tnz` and shells out to `tcomposer` — only if spikes 1, 2, 3, and 5 all pass. Spike 1 is a hard gate: if the renderer cannot run headless on macOS, the path closes regardless of everything else.
