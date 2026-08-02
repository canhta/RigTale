# Repository Review: Inochi2D and Inochi Creator

**Screened under:** `SPIKE-C001` (`RGT-S001`), read-only static source inspection with full commit history.

| | Runtime | Editor |
|---|---|---|
| Repository | https://github.com/Inochi2D/inochi2d | https://github.com/Inochi2D/inochi-creator |
| Inspected commit | `ec702261dd6428141bfd0b174a015f8af872d3ed` (2026-08-01) | `dba60811cff224f8cc9ce367b1d9291bfa5f7640` (2025-03-12) |
| Licence | BSD-2-Clause (`LICENSE`, `dub.sdl`) | BSD-2-Clause (`LICENSE`, `dub.sdl`) |
| Disposition | `reference`, leaning `adapt` | `reject` as a component, `reference` for design |

## Why This Pair Was Screened

Documentation screening suggested Inochi2D might be the only 2D deformation system whose authoring editor is also open source — refuting the pattern that disqualified Rive, Spine, DragonBones, Live2D, and Creature.

**The claim survives verification at the licence level. Both halves really are BSD-2-Clause.** But it buys less than it appears to, for a reason worth stating precisely.

## The Headline Finding

**An open-source editor does not make rigs programmatically authorable. It makes them GUI-authorable — in this case by an application that has not been touched in seventeen months and can no longer build against the current runtime.**

What actually helps RigTale here is different and more durable: **a fully documented, BSD-2-licensed binary format with real writer primitives in the source.** That is a genuine differentiator against Rive, and it is exploitable without the editor at all.

## Programmatic Authoring: Writers Exist, But the Last Link Is a Stub

This is not the Rive failure mode — writers are present — but it is not a solved path either.

**What exists.** Container writers are complete: `modules/inp/source/inp/format/inp2/writer.d` (`writeINP2`), `inp1/writer.d`, `json/writer.d`, dispatched from `modules/inp/source/inp/format/package.d`. Model-level serialisation is real: `source/inochi2d/puppet.d:484` `Puppet.serialize()`, emitting `properties`, `nodes`, `param`, and `animations` (`puppet.d:237-241`). Per-node writers exist for textures, tint, opacity (`nodes/visual/part.d`), z-sort (`nodes/visual/package.d:65`), mask mode (`nodes/visual/mask.d:45`), and the animation types (`animation/animation.d:80,142,293`).

**What is missing.** `Puppet.toStream` (`source/inochi2d/puppet.d:465-476`) builds the data node, comments `// Serialize data`, and returns `false`. It never calls `serialize()`, never encodes the texture section, and never calls `writeINP`. There is no wired end-to-end save at HEAD.

**The C FFI is read-only.** `include/inochi2d.h` exposes 101 functions including `in_puppet_load` (`:403`) and `in_puppet_load_from_memory` (`:420`). Searching the header for save, write, serialise, or export matches only documentation prose. `in_node_new` (`:692`) and `in_parameter_set_value` (`:674`) allow in-memory construction and driving, but nothing can persist the result.

**The only shipped writer requires the GUI.** The editor writes through `inochi-creator/source/creator/package.d:313`, calling a symbol from `inochi2d ~>0.8.7`. The editor's entry point `source/app.d:50` has no option parsing and no headless mode; the sole command-line affordance is `app.d:85`, a project file to open in the GUI.

**Verdict.** A program *can* author an Inochi2D puppet without a GUI and without a proprietary tool, by building a node tree and calling `writeINP2`, or by independently implementing the documented format. Nothing is locked. But no such path is wired today, and RigTale would be completing `toStream` and writing its own FFI writer.

## The Format Is the Real Asset

`.inx` is the editor project and `.inp` the distributable model; they share a container, and the runtime loads `.inx` directly (`examples/ada-static.inx`).

INP2 is a little-endian, 32-bit-aligned tagged binary format with magic `TRNSRTS2`, **fully documented in-repo**: `tech-docs/inp2.md` covers the tag table, string, blob, array and object encoding, and CRC-32 on blobs; `tech-docs/inp2-puppet.md` covers `INP_SECT`, `TEX_SECT`, and `EXT_SECT`, with PNG, TGA and BC7 texture IDs. INP1 wrapped a JSON payload (`inp2-puppet.md:14-15`). Readers exist for both with format detection (`format/package.d`), and there is a round-trip test (`modules/inp/source/inp/format/inp2/tests.d`).

The documentation is precise enough to reimplement independently. Compare Rive, where the format has no in-repo specification and no writer at all.

## Deformation Model

Bone hierarchies and parameter-driven mesh deformation coexist in one node graph — unusual and valuable. Registered node types across `source/inochi2d/nodes/`: `Node`, `Visual`, `Part`, `AnimatedPart`, `Composite`, `Solo`, `Mask`, `Deformer`, `MeshDeformer`, `LatticeDeformer`, `Bone`, `BoneModifier`, `SimplePhysics`. `nodes/bone/bone.d:26` documents bones as building "skeletal hirearchies that deform other nodes via the use of bone weights", applied as weighted vertex offsets in `onUpdate`.

**Serious caveat.** The parameter-binding layer is largely commented out at HEAD: `param/bindings/deform.d` has 125 of 175 lines commented, `node.d` 169 of 226, `property.d` 96 of 140. The core of parameter-driven deformation is disabled mid-rewrite.

**Fixed-cast fit.** A `Puppet` is one character per file. There is no multi-character scene container. A fixed cast would be N `.inp` files plus a host-side scene graph RigTale must own. Reusable published rigs are expressible; a scene is not.

## Timeline: Real, But Parameter-Bound

Authored motion exists — this is not live-puppeteering only. `source/inochi2d/animation/animation.d` defines `Animation` with timestep, additive flag, weight, lanes, length, lead-in and lead-out; `AnimationLane` with frames, interpolation and merge mode; `Keyframe` with frame, value and tension; and interpolation modes nearest, stepped, linear, cubic, and quadratic. All serialise and deserialise. `animation/player.d` provides `AnimationPlayer.update(float delta)` with `snapToFramerate`.

**The constraint that matters:** lanes bind only to a `Parameter` plus target axis (`animation.d:110-122`, resolved through `puppet.findParameter`). An arbitrary node transform cannot be keyframed — it must first be exposed as a parameter.

`[INFERENCE]` For RigTale this is a poor fit as-is. Camera moves, parallax offsets, and shot-level transform control need direct keyframing, not indirection through pre-declared parameters.

## Rendering: Bring Your Own

There is no renderer in the repository. The runtime emits draw commands (`core/render/drawlist.d`) with eight texture sources and an explicit `DrawState` covering normal draw, mask definition, masked draw, and composite begin/end/blit, plus blend and masking modes and 64 bytes of per-node variables. `examples/basic-gl/main.c` is a reference OpenGL consumer, and `tech-docs/building-a-renderer.md` documents the contract.

There is no headless or offscreen path in-repo. Frame stepping is host-controlled: `in_puppet_update(obj, float delta)` and `in_puppet_draw(obj, float delta)` (`include/inochi2d.h:526,535`) take a caller-supplied delta, so deterministic fixed-step is achievable by the host — but all pixel output would be RigTale's own renderer. The editor's offline render (`creator/io/videoexport.d`, shelling out to ffmpeg) is GUI-driven only.

## Layers, Masks, Draw Order, Camera

Draw order is `Visual.zSort_`, serialised as `zsort` (`nodes/visual/package.d:65,78`) with `zSortRender` combining node and property values (`:169`). Masks are a first-class node (`nodes/visual/mask.d:77`) with masking modes (`core/render/state.d:171`) and push/pop in the draw list. Layered compositing uses `Composite` nodes with `beginComposite`/`endComposite`/`blit` (`drawlist.d:147-163`) — nested framebuffers. `Solo` (`nodes/visual/solo.d`) gives exclusive-child switching, directly useful for cutout part swaps.

**Camera is not in the runtime.** It is an editor extension: `inochi-creator/source/creator/ext/nodes/excamera.d` defines `ExCamera : Node` with a 1920×1080 viewport, registered at `:118`. **Parallax is not verified from source** in either repository.

## Integration Cost

D with LDC 1.40 or later; DMD and GDC explicitly disabled. The C FFI is substantial and in-repo: `source/inochi2d/cffi.d` at 1,799 lines and `include/inochi2d.h` at 1,569 lines, 101 functions, with a dynamic-library configuration. Godot GDExtension, WASM, and TypeScript bindings also exist.

A Swift or C++ host links the dynamic library, includes the header, and implements a renderer from draw commands. **The read and play path is turnkey; the dominant cost is owning a Metal renderer, not the D boundary. The write path is absent from the FFI**, so authoring means embedding D or reimplementing INP2 from the specification.

## Maintenance Health — The Decisive Weakness

Numbers from full git history.

**Runtime:** 800 commits total, 229 in the last 12 months, 254 in 24, 20 distinct authors all-time. Recent authors: one person with 224 of 229. All-time, the top two identities are the same person at 649 of 800 — **81%, bus factor 1**. Last commit 2026-08-01. Latest tag `v0.8.7` dated 2024-10-02: roughly **22 months of unreleased rewrite sitting on main**.

**Editor:** 1,257 commits, **zero in the last 12 months**, 123 in 24, 41 distinct authors all-time, **zero authors in the last 12 months**. Last commit 2025-03-12. Last tag `v0.8.6`.

**The gap, quantified.** The editor pins `inochi2d ~>0.8.7` while the runtime HEAD is a 0.9 rewrite with an incompatible format and a rewritten node and parameter API. **The editor cannot build against runtime HEAD.** The shipped editor produces INP1; the actively developed runtime treats INP1 as deprecated (`puppet.d:439-443`). **There is no released, buildable editor for 0.9.**

The "runtime and editor are both open source" claim is true but temporally split. They are two projects that no longer interoperate.

## Governance Constraint

`inochi2d/AGENTS.md` and `inochi2d/CLAUDE.md` both state that the project does not allow AI agents to interface with the source, and that doing so "will get your operator banned."

BSD-2-Clause permits use and forking regardless. But an agent-operated studio has no viable upstream contribution path, and RigTale should not attempt one. Recorded as a project constraint, and respected.

## Test Strategy

Runtime tests cover format round-trip and SIMD maths only — unit tests in vector, memory pool, SIMD, and the INP format modules, with CI running `dub test` on macOS, Linux, and Windows. There are no puppet-level, golden-file, or render tests.

Editor: **zero unit tests.** Its test CI job invokes `dub test` with nothing to run; it is effectively a build check.

## macOS Support

First-class in both. The runtime CI builds `arm64-apple-darwin` and `x86_64-apple-darwin` on macOS with tests, and produces universal binaries via `lipo`; `dub.sdl` carries aarch64 NEON flags. The editor has macOS app-bundle configurations, `Info.plist`, entitlements, a full iconset, universal build and DMG scripts, and a macOS CI job.

## Patterns to Adopt or Adapt

- **The INP2 container design** — tagged, aligned, CRC'd blobs with clean section separation and a vendor-extension section keyed by reverse domain. An excellent model for a published rig format, and the extension section is exactly where RigTale-specific direction data could ride alongside a standard rig.
- **The draw-command contract** — explicit state transitions for mask definition, masked draw, and composite begin/blit. A clean renderer-agnostic boundary worth copying wholesale.
- **`Solo` nodes** for exclusive-child switching, the natural primitive for cutout part swaps.
- **Format-version detection with an explicit upgrade path and a warning sink.**
- **Documenting the format to reimplementable precision in-repo.** This is what makes BSD-2 meaningful; a permissive licence over an undocumented format is worth much less.

## Patterns to Avoid

- **Binding animation exclusively to named parameters.** RigTale needs direct transform and draw-order keyframing for camera, parallax, and shot control.
- **Camera as an editor-only extension outside the standard.**
- **One-puppet-per-file with no scene container.**
- **Shipping a format rewrite without an editor that can produce it.** This is the concrete failure state of this project today.
- **Zero-test GUI editors as the sole authoring path.**

## Questions Requiring Executable Evidence

| Question | Route |
|---|---|
| Does `writeINP2` plus `Puppet.serialize` round-trip a real puppet if `toStream` is completed — is texture-section encoding the only missing piece? | `SPIKE-A002` |
| Can `examples/ada-static.inx` load and render through the 0.9 runtime today, or is the commented-out binding layer fatal? | `SPIKE-A002` |
| Are 0.8 editor outputs readable by 0.9's deprecation path with deformations intact? | `SPIKE-A002` |
| Is `in_puppet_update(delta)` bit-deterministic across runs given the SIMD paths? | `SPIKE-R001` |
| What does a minimal Metal renderer against the draw-command contract cost in practice? | `SPIKE-I001` |
| Can a fixed cast be composited by a host scene graph with correct cross-puppet draw order? | `SPIKE-A001` |
| Licences of the `gamut`, `nulib`, `numem`, `nurt`, and `numath` dependencies, which are not vendored | `SPIKE-R001` licensing check |

## Conclusion

**Runtime: `reference`, leaning `adapt`.** The format specification, node taxonomy, and draw-command contract are the most reusable open-source 2D-deformation design artifacts found in this screening round, and BSD-2-Clause permits full appropriation. But adopting the runtime as a dependency means betting on an unreleased, mid-rewrite, bus-factor-one codebase with a stubbed writer and a disabled binding layer.

**Editor: `reject` as a component, `reference` for design.** It genuinely refutes the claim that 2D rig authoring is always proprietary — on this evidence Inochi2D is the only candidate pair where both halves are permissively licensed. But it is seventeen months unmaintained, has zero tests, has no headless surface, and cannot build against the current runtime. It cannot serve an agent-operated authoring requirement in any form.

The transferable value is the documented format, not the editor.
