# Repository Review: Godot Engine

**Screened under:** `SPIKE-C001` (`RGT-S001`), read-only static source inspection.

**Repository:** https://github.com/godotengine/godot

**Inspected commit:** `eda2a482e9ce82e4056cfffae0ea98c1954605a1` (authored 2026-07-31). Version reported by `version.py` as `4.8.0-dev`. The local clone is `blob:none` partial with no tags fetched, so the commit's relationship to a released version is not verified.

**License:** MIT/Expat (`LICENSE.txt`). Third-party inventory in `COPYRIGHT.txt` lists 106 stanzas covering Apache-2.0, BSD, BSL-1.0, CC0, CC-BY-4.0, Expat, MPL-2.0, OFL-1.1, Zlib and others. No GPL, LGPL, or AGPL. MPL-2.0 applies only to `thirdparty/certs/ca-bundle.crt` and one further stanza; CC-BY-4.0 covers `misc/logo/*` and is avoidable by not redistributing the logo. Obligation profile for redistribution is attribution plus licence-text inclusion.

**Disposition:** `adapt`. Revised upward from `reference` after the authoring self-correction recorded below. The `libgodot` windowless-capture question remains the gate on any selection, but it does not gate the screening disposition. See the Conclusion.

## Purpose and Production Model

General-purpose 2D/3D game engine with an integrated editor. The production model is editor-authored scene graph driving a runtime main loop. There is no offline render-job concept: rendering happens as a side effect of iterating the main loop (`Main::iteration()`, `main/main.cpp:4817`). Movie output is a recorder attached to that loop, not a renderer invoked over a time range.

This mismatch — game loop versus render job — is the structural finding of this review.

## 2D Cutout Capability

Source-verified and strong.

| Capability | Source |
|---|---|
| `Bone2D` with rest transform, length, parent, skeleton index | `scene/2d/skeleton_2d.h:38-97` |
| `Skeleton2D` with parent index, accumulated transform, rest inverse, local pose override, modification stack | `scene/2d/skeleton_2d.h:111-124`, `scene/resources/2d/skeleton/skeleton_modification_2d.h` |
| Per-vertex bone weights on deformable polygons | `scene/2d/polygon_2d.h:42-52,68` (`struct Bone { NodePath; Vector<float> weights }`) |
| GPU skinning through the rendering server | `servers/rendering/rendering_server.h:297,302,852` |
| Layer ordering, y-sort, clip children | `scene/main/canvas_item.h:74-78,107-147` |
| Independent canvas layers with their own transform | `scene/main/canvas_layer.h:44-106` |
| Group compositing with fit and clear margins | `scene/2d/canvas_group.h:35-52` |
| Camera with offset, zoom, anchor, limits, smoothing | `scene/2d/camera_2d.h:62-136` |
| Parallax | `scene/2d/parallax_2d.*`, `parallax_background.*`, `parallax_layer.*` |
| Animation graph, state machines, blend spaces | `scene/animation/animation_tree.*`, `animation_node_state_machine.*`, `animation_blend_space_1d/2d.*` |

`AnimationMixer` carries an explicit `deterministic` property with `set_deterministic()`/`is_deterministic()` (`scene/animation/animation_mixer.h:329,423-424`) and a `ANIMATION_CALLBACK_MODE_PROCESS_MANUAL` mode (line 57). The engine already anticipates externally driven stepping.

## Data Contracts

Text serialization is real and parser-backed. `ResourceLoaderText` and `ResourceFormatSaverText` (`scene/resources/resource_format_text.h:40-218`) write INI-style headers `[gd_scene format=N uid=...]`, `[ext_resource ...]`, `[sub_resource ...]`, `[node ...]` (`resource_format_text.cpp:1033-1923`), parsed by `VariantParser`. Production state is therefore human-readable, diffable, and writable from outside the editor. The saver sorts external resources before writing, which is determinism-friendly, though full byte stability is not verified from source.

Animation track types are `TYPE_VALUE, TYPE_POSITION_3D, TYPE_ROTATION_3D, TYPE_SCALE_3D, TYPE_BLEND_SHAPE, TYPE_METHOD, TYPE_BEZIER, TYPE_AUDIO, TYPE_ANIMATION` (`scene/resources/animation.h:49-57`). There are no dedicated 2D transform tracks; 2D rigs animate through generic `TYPE_VALUE` property tracks. Per-track update modes `CONTINUOUS/DISCRETE/CAPTURE` distinguish interpolated from stepped properties, which cutout sprite swapping needs.

## Determinism and Rendering

`--fixed-fps N` forces the process delta (`main/main_timer_sync.cpp:433-434`) and bypasses the wall-clock frame delay (`main/main.cpp:5066-5068`). `--write-movie` auto-sets `fixed_fps = 60` when unset and forces the dummy audio driver with threading disabled (`main/main.cpp:1888-1895`, `2756-2760`), so audio mixes in lockstep with frames (`servers/movie_writer/movie_writer.cpp:244`). `RenderingServer::draw(bool swap_buffers, double frame_step)` is script-exposed as `force_draw` (`servers/rendering/rendering_server.h:971`), giving an explicit render-one-frame hook.

Pixel-level reproducibility across runs, builds, or GPU backends is not verified from source and is not tested upstream.

## Blocking Weaknesses

These are architectural, not configuration issues.

1. **Headless does not rasterize.** `DisplayServerHeadless::get_rendering_drivers_func()` returns only `"dummy"` and `has_feature()` returns `false` unconditionally (`servers/display/display_server_headless.h:44-58`). The dummy rasterizer is a no-op (`servers/rendering/dummy/rasterizer_dummy.h:91`) and its texture store returns the source image rather than a rendered result (`servers/rendering/dummy/storage/texture_storage.h:108-112`). `--headless` gives logic without pixels.
2. **The movie writer is bound to a real main window.** `MovieWriter::add_frame()` resolves the viewport from `MAIN_WINDOW_ID` and mutates the window title each frame (`servers/movie_writer/movie_writer.cpp:197-202`). `--headless --write-movie` is not a supported offline path from what the source shows.
3. **No time-range or start-frame rendering.** Output is a zero-indexed sequence from process start plus one monolithic WAV (`servers/movie_writer/movie_writer_pngwav.cpp:66-86`); no range argument exists in `main/main.cpp`. Isolated shot rerendering — a charter requirement — must be built outside the engine.
4. **No pixel-level regression testing.** The 234-file suite under `tests/` runs against the dummy rasterizer (`tests/display_server_mock.cpp:37-39`). There are no golden-image tests. `tests/data/images/*` are decoder fixtures.
5. **Zero 2D-skeletal test coverage.** No `test_skeleton_2d.cpp` and no `test_polygon_2d.cpp` exist, though `test_skeleton_3d.cpp` does. The subsystem RigTale would depend on most is the one with no upstream tests.
6. Audio/video sync is best-effort and warns when `mix_rate % fps != 0` (`servers/movie_writer/movie_writer.cpp:128-130`).

## Correction: Rig Authoring Is Fully Scriptable

An earlier draft of this review recorded weight painting as editor-only, on the basis that a weight-painting mode exists in `editor/scene/2d/polygon_2d_editor_plugin.h:62-171`. **That inference was wrong, and the disposition below is revised because of it.**

Verified directly at the pinned commit, `doc/classes/Polygon2D.xml` exposes to script:

| Method | Signature |
|---|---|
| `add_bone` | `(path: NodePath, weights: PackedFloat32Array)` — "Adds a bone with the specified path and weights" (`:12-17`) |
| `set_bone_weights` | `(index, weights: PackedFloat32Array)` (`:61-64`) |
| `set_bone_path` | (`:53`) |
| `get_bone_weights`, `get_bone_count`, `clear_bones` | (`:46`, `:33`, `:20`) |

`doc/classes/Bone2D.xml:10` confirms the intent explicitly: "If in the editor, you can set the rest pose of an entire skeleton using a menu option, **from the code, you need to iterate over the bones to set their individual rest poses**." The documentation treats code-driven rig construction as a supported path, with the editor menu as the convenience.

Combined with `PackedScene.pack(node)` and saving, a rig — bone hierarchy, rest poses, per-vertex weights, and the containing scene — is **constructible and serialisable entirely from code**.

**Consequence.** Godot is a fully programmatic 2D cutout rig path: scriptable bone creation, scriptable per-vertex weights, scriptable scene serialisation, and a diffable text scene format. That is a rare combination and it materially strengthens the case for the embedding path below.

**The remaining gap is different from what this review first recorded.** It is not authoring; it is portability. **The rig is a Godot scene, not a portable format.** RigTale would be committing its rig representation to one engine's scene graph unless it keeps its own canonical rig data and generates scenes as build artifacts — the same shape recommended for Blender.

## The Finding That Could Change the Disposition

`core/extension/libgodot.h:60,71` exports `libgodot_create_godot_instance` and `libgodot_destroy_godot_instance` (verified directly at the pinned commit). `GodotInstance` (`core/extension/godot_instance.h:36-58`) exposes `initialize / start / is_started / iteration / stop / pause / resume`, and `GodotInstance::iteration()` calls `Main::iteration()` directly (`godot_instance.cpp:81-83`). The build gate is `library_type=shared_library` requiring `"library"` in the platform's supported list (`SConstruct:600-604`); macOS declares `["library", "metal", "mono"]` (`platform/macos/detect.py:86-91`) and ships `platform/macos/libgodot_macos.mm`.

This is precisely the boundary RigTale needs: an external deterministic orchestrator owning the clock and pumping frames one at a time. It also makes the window-bound movie writer bypassable in principle. Whether it works windowless on macOS with Metal is unverified and is the decisive executable question.

There is also a stable C ABI for GDExtension (`core/extension/gdextension_interface.json`, `core/extension/gdextension.h:139-173`).

## Patterns to Adopt or Adapt

- **Deterministic blending as a serialized property**, not an implicit mode (`AnimationMixer::deterministic`).
- **Host-owns-the-loop embedding**: engine exposes a single-step `iteration()`; the orchestrator decides when frames advance. This shape is worth keeping regardless of which renderer is eventually chosen.
- **An explicit render-one-frame-at-this-delta entry point** decoupled from presentation (`force_draw(swap_buffers, frame_step)`).
- **Text intermediate representation with a `format=N` version header and sorted external references** — versioned, diffable, sort-stable production state.
- **Group compositing**: rasterize a subtree to its own buffer, then composite with margins. The right primitive for cutout character layers.
- **UID-indirected asset references** so assets can move without breaking scene files.
- **Per-track update modes** separating interpolated properties from stepped sprite swaps.

## Patterns to Avoid

- Coupling frame capture to a display window.
- Recording as a side effect of a game loop rather than a render job over an explicit frame interval. This is the structural reason Godot has no isolated shot rerender.
- Sequence output keyed to process-start index instead of absolute timeline frame numbers.
- Testing an animation and rendering system entirely through a null rasterizer.

## Questions Requiring Executable Evidence

| Question | Route |
|---|---|
| Can a `libgodot` shared-library host on macOS arm64/Metal drive `GodotInstance::iteration()` plus `force_draw()` and read back a `SubViewport` texture with no visible window? | `SPIKE-R001`, decisive |
| Is capture bit-identical across two runs on one machine, and across Metal versus MoltenVK, for a `Polygon2D`+`Skeleton2D` scene at `--fixed-fps 24`? | `SPIKE-R001` |
| Does `AnimationPlayer.seek(t, update=true)` plus `force_draw` produce the same frame as playing forward to `t` at fixed fps? | `SPIKE-R002`, gates isolated shot rerender |
| Is `ResourceFormatSaverText` round-trip byte-stable (load then save an unmodified `.tscn` and diff)? | `SPIKE-CS001` |
| Clean-build wall time and disk footprint on Apple silicon for `library_type=shared_library`; are MoltenVK/ANGLE SDKs required for a 2D-only build? | `SPIKE-I001` |
| Does `CanvasGroup` plus `clip_children` composite correctly through an offscreen `SubViewport` chain at 1080p with 6–10 character layers, and at what per-frame cost? | `SPIKE-R001` |
| Does a rig built entirely through `add_bone` and `PackedScene.pack` round-trip and render identically to an editor-authored equivalent? | `SPIKE-A002` |

## Conclusion

**`adapt`**, revised upward from `reference` after the authoring correction above.

Godot verifies **every link in the authoring chain from primary source**: scriptable bone creation, scriptable per-vertex bone weights, scriptable scene serialisation, a diffable text intermediate representation with a real parser, an explicit deterministic-blending flag, and a single-step embedding API — all under MIT with a copyleft-free dependency graph and first-class macOS support.

**The word "only" is withdrawn from this claim.** `opentoonz.md` asserts a fully verified authoring chain for OpenToonz under BSD-3, and its load-bearing citations were independently confirmed. Godot's distinguishing properties are the MIT licence, the copyleft-free dependency graph, and per-vertex weight scripting — not exclusivity. What separates Godot from OpenToonz here is that Godot's rig is a scene rather than a portable format, and that its headless display server returns only `"dummy"`; those remain the gating facts.

It remains source-verified weak on the rendering-as-a-job half: headless builds have no rasteriser, the movie writer captures the main OS window, output has no time-range control, and there is no pixel-level regression test anywhere in a suite that itself runs against a dummy renderer. Its 2D-skeletal subsystem has **no upstream tests at all**.

Two gaps define the remaining risk, and they are different from what this review first recorded. **Portability**: the rig is a Godot scene, not a portable format, so RigTale must keep canonical rig data of its own and generate scenes as build artifacts. **Rendering**: the `libgodot` windowless-capture question is unanswered and is the gate.

No claim here rests on a demo or a feature list, and the one claim that rested on an inference rather than a citation has been corrected against source.
