# Repository Review: Blender

**Screened under:** `SPIKE-C001` (`RGT-S001`), read-only static source inspection.

**Repository:** https://github.com/blender/blender

**Inspected commit:** `a3afe6326e5f6279fda15db1e6c088bbdda66220` (2026-08-02). The clone is shallow and sparse; commit history and contributor counts are not derivable from it.

**Version as declared in source:** `source/blender/blenkernel/BKE_blender_version.h:23-31` — version 503, cycle `alpha`. This is a 5.3-alpha development commit, not a release. Grease Pencil 3 APIs are still churning at this revision.

**Disposition:** `defer` — deep review warranted, commitment blocked on three executable questions and one owner decision.

## Licensing: Unresolved and Requires an Owner Decision

The repository describes its own licence inconsistently.

| Source | What it says |
|---|---|
| `COPYING:1-8` | "Blender uses the GNU General Public License… Apart from the GNU GPL, Blender is not available under other licenses." Points to `doc/license/GPL-license.txt`, which is **GPL version 2**. |
| `README.md` | "Blender as a whole is licensed under the GNU General Public License, **Version 3**." |
| `release/license/license.md:18-20` | "Blender itself is released under [GPL 3.0 or later]" |
| Per-file SPDX in `source/blender/` | 7,017 `GPL-2.0-or-later`, 2 `GPL-3.0-or-later`, plus Apache-2.0 (167), MIT (9), Zlib, BSD-3-Clause |

**No linking exception exists.** A search across `COPYING`, `README.md`, `doc/license/`, and `release/license/` for "linking exception" or "additional permission" returns only verbatim GPLv3 §7 boilerplate.

This is a statement of what the files say, not legal advice. The consequence for RigTale is that any integration deeper than a subprocess boundary raises a distribution question the Project Owner must decide deliberately. It is recorded as an open decision, not resolved here.

## Why This Is the Strongest Capability Match Found

Blender is the only system screened in this round with a purpose-built 2D cutout layer model.

### Grease Pencil is layer-native and time-native

`DNA_grease_pencil_types.h:441-483` defines a layer tree of leaves and groups (`:313-404`). Each `GreasePencilLayer` carries:

- `blend_mode` — NONE, HARDLIGHT, ADD, SUBTRACT, MULTIPLY, DIVIDE (`:106-113`);
- `opacity` and a `masks` list;
- `parent` plus `parsubstr`, documented as "Can be an armature in which case the `parsubstr` is the bone name" (`:361-364`);
- `parentinv` and independent translation, rotation, and scale (`:344-386`).

Frames are an explicit sorted keyframe map from frame number to drawing index (`:255-290`).

### Per-layer routing to named render targets

`char *viewlayername` — "Only include Layer in this View Layer render output" (`:376-377`), exposed as `layer.viewlayer_render` (`rna_grease_pencil.cc:1229-1234`) with `use_viewlayer_masks` (`:1236-1240`), enforced in the engine (`gpencil_engine_private.hh:345-354`). Combined with `GREASE_PENCIL_AS_SEPARATE_PASS` on `ViewLayer::grease_pencil_flags` (`DNA_layer_types.h:80-82,284`), a single character can be split into separate render passes for external layered compositing.

This is the primitive RigTale's isolated-layer rerender requirement would build on, and no other candidate has it.

### Bone-driven cutout deformation

`GreasePencilArmatureModifierData` with `deformflag = ARM_DEF_VGROUP` (`DNA_modifier_types.h:3230-3238`) plus GP vertex-group weights (`BKE_grease_pencil_vertex_groups.hh:19-41`), over a full armature stack: `DNA_armature_types.h`, 31 constraint types including `CONSTRAINT_TYPE_KINEMATIC` and `CONSTRAINT_TYPE_ARMATURE`, and two IK solvers. Twenty-seven Grease Pencil modifiers exist, including `Time` with offset, scale, custom range, and segments (`DNA_modifier_types.h:3268-3287`).

### Frame-exact CLI addressing

`--render-frame` accepts single frames, comma lists, `A..B` ranges, and relative `+N` from start or `-N` from end (`creator_args.cc:2493-2500`, `parse_int_relative` at `:163-199`). Each frame is rendered by an **individual** `RE_RenderAnim(re, …, frame, frame, …)` call, with the source comment at `:2547-2548`: "We could pass in frame ranges, but prefer having exact behavior as passing in multiple frames."

That is isolated-shot rerender semantics, stated by the implementation rather than inferred from a feature list.

### Authoring needs no UI context

The Grease Pencil data API is non-operator RNA: `bpy.data.grease_pencils.new()`, `.layers.new/remove/move`, `.mask_layers.new`, `drawing.add_strokes/remove_strokes/resize_strokes/reorder_strokes/set_types`, `frames.new/remove` (`rna_grease_pencil_api.cc:773-1009`), exercised in `tests/python/bl_pyapi_grease_pencil.py`.

By contrast `bpy.ops` routes through `WM_operator_poll_context` (`bpy_operator_function.cc:288-300`), several operators hard-bail in background mode (`wm_operators.cc:2386-2388,2404-2406,3806-3812`), and `bpy.context.temp_override` can only validate real windowing data, never fabricate it (`bpy_rna_context.cc:180-290`).

### Compositor runs headlessly on CPU

`COM_context.hh:62-63` exposes `use_gpu()`; `render/intern/compositor.cc:851-871` falls back to CPU with no GPU context; `pipeline.cc:1298-1303` confirms that in background mode the compositor executes and File Output nodes are the requested output. Multi-slot File Output writes either one file per slot or one multilayer EXR layer per slot with `####` frame substitution (`node_composite_file_output.cc:459-584`).

## Determinism: Partial Evidence, No Contract

**Evidence for.** Grease Pencil antialiasing is deterministic by construction: `Instance::antialiasing_sample_get()` (`gpencil_antialiasing.cc:172-190`) is a pure Halton(2,3) function of sample index with no RNG, no seed, and no time input. EEVEE is the same (`eevee_sampling.cc:173-189`), and its temporal reprojection is viewport-only and forced off for renders (`eevee_sampling.cc:129-138`). Cycles' seed is explicit with `use_animated_seed` defaulting to false (`intern/cycles/blender/addon/properties.py:898-909`). Grease Pencil is never path-traced — Cycles skips GP objects (`intern/cycles/blender/sync.cpp:949-956`) and GP is always rasterised by its own draw engine (`draw/engines/gpencil/gpencil_render.cc:390-400`).

**Evidence against.** There is no `--deterministic` flag and no bit-comparison test anywhere. `use_deterministic_guiding` exists in Cycles precisely because the alternative is not deterministic. Adaptive sampling is on by default (`intern/cycles/scene/integrator.cpp:141`), and `time_limit` makes output wall-clock dependent when enabled. Source comments admit nondeterminism: `draw/intern/draw_pass.hh:17` says draw order is "not even deterministic"; `eevee_shadow_shared.hh:162` notes a non-deterministic loop.

**The project's own unresolved contradiction.** `tests/python/eevee_render_tests.py:452-455` loosens the Grease Pencil tolerance to 6/255 at 0.1% with the comment `# TAA dependent look? To be investigated.` Blender itself has an open question about GP render stability.

Whether `--threads`, device choice, or GPU driver version changes pixels is not statically verifiable.

## Test Strategy: Tolerance-Based, Not Bit-Exact

303 gtest files colocated with source. Render regression uses golden images with tolerances: `tests/python/modules/render_report.py:126-229` shells out to `oiiotool --fail --failpercent --diff` with defaults of `fail_threshold = 0.016` (about 4/255) and `fail_percent = 1` (`:303-304`). Per-suite, per-vendor, and per-backend overrides span 2/255 to 10/255 and 0.01% to 6%, including Metal-specific relaxations (`eevee_render_tests.py:400,412,419-421,468`) and a Darwin-only loosening in `workbench_render_tests.py:143`.

If `oiiotool` is absent, **all render tests are silently skipped** (`tests/python/CMakeLists.txt:24`).

Grease Pencil is covered: `tests/files/render/grease_pencil/` holds 7 scenes across 4 engines, and `tests/files/grease_pencil/grease_pencil_suzanno_cutout.blend` exists.

The regime tolerates cross-platform pixel drift by design. It does not assert reproducibility.

## Blocking Weaknesses

1. **`.blend` is an opaque pointer-address dump.** `blenloader/intern/writefile.cc:10-32` describes an "IFF-style structure (but not IFF compatible!)" where each block header carries "old pointer (the address at the time of writing the file)" and a struct index into an embedded DNA table. No diff, no merge, no external deterministic edit, no meaningful review. This is fundamentally incompatible with RigTale's requirement that production state be inspectable and editable as structured data.
2. **Silent-success failure mode.** Render errors that only call `BKE_report` appear to exit 0 (`creator_args.cc:2537-2541`, `creator.cc:639-651`). Without `--python-exit-code`, even an uncaught Python traceback exits 0 (`:2745-2749,2847-2874`).
3. **Argument order is load-bearing.** `creator_args.cc:872-883` documents that `--render-frame` before `-o`, or `-o` before the `.blend`, silently renders to the wrong place.
4. **Grease Pencil always requires a GPU context, even in background mode.** `wm_init_exit.cc:154-172` lazily initialises a GPU backend and offscreen context when running headless, and GP has no CPU rasterisation fallback. Whether this works on a macOS session with no logged-in window server is the go/no-go question for this entire path.
5. **The `bpy` pip module has no CLI layer.** `WITH_PYTHON_MODULE` is annotated "only enable for development", gtests are force-disabled with it (`CMakeLists.txt:1629`), and the entire CLI layer is `#ifndef WITH_PYTHON_MODULE` (`creator_args.cc:3426`) — so `bpy` exposes no `--render-frame`, no `-o`, and no exit-code surface.
6. **Scale is wrong for a solo maintainer to own.** Roughly 4.3 million lines across 20,359 tracked files; `build_files/build_environment/cmake/versions.cmake` pins about 147 third-party versions across roughly 105 external projects with 69 patch files. On macOS the build hard-errors without a precompiled library submodule (`platform_apple.cmake:49-58`) and requires Xcode 16.3 or later.

The scale objection is mitigated by consuming official builds rather than building from source, but not eliminated.

## The Defensible Shape, If It Advances

Blender is not adoptable as RigTale's architecture and must not be embedded. The `.blend` opacity contradicts the charter's structured-editability requirement directly.

The shape that survives screening is: RigTale owns production state in its own text format, and treats Blender as a **replaceable, subprocess-isolated rasterisation backend** invoked as `blender --background --factory-startup --python driver.py --python-exit-code 1`, with `.blend` files as disposable build artifacts regenerated from RigTale state and never treated as source.

This is a hypothesis about an adapter shape, not a renderer selection. It must remain one implementation behind a boundary, not the boundary itself. `RGT-D010` remains the only place a renderer can be selected.

## Patterns to Adopt or Adapt

- **Path-addressed override deltas.** `IDOverrideLibraryProperty{char *rna_path; ListBase operations}` (`DNA_ID.h:313-336`) is the closest thing to a declarative, diffable production-state layer found in this round. Adopt the shape; store it in RigTale's own text format, never in a binary.
- **Layer-to-named-render-target routing** as the core primitive for isolated layer rerendering.
- **Low-discrepancy sampling indexed by sample number** rather than a seeded RNG — determinism by construction, with no seed to manage.
- **Stable numeric "forever" handles for reusable motions** alongside human-readable names (`DNA_action_types.h:1245-1300`, `ActionSlot.handle`).
- **An explicit frame list, range, and relative CLI grammar**, rendering one frame per invocation for exact isolated semantics.
- **Multi-slot output with `####` templating** and multilayer EXR as the layered-compositing handoff.
- **Golden-image regression with explicit, per-target, version-controlled tolerances** — but RigTale should default to bit-exact and treat every tolerance as a recorded exception with a reason, which Blender does not.

## Patterns to Avoid

- Binary, pointer-address-keyed state as the source of truth.
- Order-dependent CLI flags that change semantics silently.
- Exit code 0 on failure. RigTale must fail loudly by default; Blender's `--python-exit-code` behaviour should be RigTale's default, not an opt-in.
- Coupling data mutation to an operator layer that requires UI context.
- Vendoring roughly 150 dependencies.
- Tolerance-based image comparison as the primary correctness gate, and silently skipping all render tests when a comparison tool is missing.

## Questions Requiring Executable Evidence

| Question | Route | Weight |
|---|---|---|
| Does Grease Pencil render at all in `--background` on a macOS session with no logged-in window server, given the unconditional GPU dependency? | `SPIKE-R001` | **Go/no-go for this path** |
| Does `blender -b file.blend -f N -o out_####.png` produce byte-identical PNGs across repeat runs on one macOS machine for a GP scene? The Halton evidence suggests yes; the project's own TAA note contradicts it. | `SPIKE-R001` | Decisive |
| Can the full GP layer → View Layer → File Output chain be built and rendered entirely via non-operator RNA, with zero `bpy.ops`? | `SPIKE-R001` | Decisive |
| Does varying `--threads`, device, or driver version change GP output bytes? | `SPIKE-R001` | |
| Wall-clock for a 150–210 second multi-character GP scene (roughly 3,600–5,040 frames at 24fps), and per-shot rerender latency | `SPIKE-R001`, `SPIKE-R006` measurements | |
| Do render failures reliably produce non-zero exit codes, or must RigTale post-verify every output artifact? | `SPIKE-R001` | |
| Is the `bpy` wheel viable on macOS arm64 despite the development-only annotation? | `SPIKE-I001` | |
| How much GP3 API churn occurred between 4.x and 5.x? | `SPIKE-A002` | |

## Conclusion

`defer`.

Blender is the only surveyed system with a purpose-built 2D cutout layer model, per-layer render separation, frame-exact CLI addressing, and a UI-free data API — the four capabilities RigTale's benchmark actually requires. Rejecting it on scale alone would be wrong.

Committing to it now would also be wrong. Three questions are unanswered and one is a go/no-go: whether Grease Pencil renders headless on macOS at all. Determinism has suggestive evidence and an explicit unresolved contradiction in the project's own test suite. And the GPL posture, with no linking exception and three inconsistent self-descriptions in the repository, is a decision for the Project Owner rather than a research finding.
