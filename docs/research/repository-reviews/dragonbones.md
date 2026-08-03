# Repository Review: DragonBones

**Screened under:** `SPIKE-C001` (`RGT-S001`), read-only static source inspection with full commit history.

**Repository:** https://github.com/DragonBones/DragonBonesJS

**Inspected commit:** `64b6c69ae35777c2404be68c9192e2c56906079e` (2025-05-24). 416 commits.

**Licence:** MIT (`LICENSE`, "Copyright (c) 2012-2025 The DragonBones team and other contributors"), with the identical MIT header on every core source file. The root `package.json` declares MIT; all 16 sub-package manifests omit the `license` field, which reads as sloppiness rather than a carve-out since the file headers cover them. **The out-of-repo editors are not licensed by this file.**

**Disposition:** `adapt`, with a decision gate. `reference` is the honest fallback.

## Why This Matters Most

DragonBones is the strongest answer found to RigTale's largest gap: **an open, MIT-licensed 2D cutout skeletal format whose rig model maps directly onto a reusable fixed cast, and which is authorable programmatically without the editor.**

The decisive question was whether the JSON format is recoverable from source well enough to write without the closed editor. **It is, for cutout rigs.**

## Programmatic Authoring: Yes, for Cutout

Every key the parser consumes is a named constant in `DragonBones/src/dragonBones/parser/DataParser.ts:45-180`, and every read goes through exactly three accessors — `_getBoolean`, `_getNumber`, `_getString` (`ObjectDataParser.ts:36-92`) — each taking an explicit default. Almost every field is optional with a knowable default. The shipped sample confirms the sparseness: bones as terse as `{"name": "root1"}` in `Cocos/Demos/assets/resources/mecha_1004d/mecha_1004d_ske.json`.

There is **no writer or exporter anywhere in the repository** — a search for serialisation across `DragonBones/src/` and `builds/` returns one hit, writing a `tsconfig.json`. RigTale would author against an inferred contract rather than a round-trippable one, but the inference is tractable: the parser is 2,436 lines, takes `rawData: any`, and performs no schema validation.

The single hard gate is `ObjectDataParser.ts:2294-2352`: a version-string check, then a `console.assert` — which does not throw in Node or browsers — and a `null` return.

**The caveat that downgrades this from trivial to `adapt`:** skinned mesh authoring with weights requires reproducing editor-side bind-pose matrix maths. For pure cutout — image displays on slots, bone hierarchy, transform timelines, multiple skins, draw-order changes — no derived data is needed.

## Recovered Schema (`origin/master` — 5.6-era, superseded)

**Scope warning added after the maintenance correction below.** Everything in this section was read from `origin/master`. `origin/6.0.2` rewrites `ObjectDataParser.ts` by +375 lines and adds physics, path constraints, and shape skinning. This is the schema of the branch a default clone gives you, not the schema of current DragonBones. It must be re-derived before any format decision.

Root (`ObjectDataParser.ts:2294-2340`): `version`, `compatibleVersion`, `name`, `frameRate` (default 24; 0 coerced to 24), `armature[]`, `stage`, `textureAtlas`, `userData`.

`armature[]` (`_parseArmature`, `:285-471`) is consumed strictly in order: `name`, `frameRate`, `type`, `canvas`, `aabb`, `bone[]`, `ik[]`, then bone sorting, then `slot[]`, `skin[]`, `path[]`, shared-mesh linking, `animation[]`, `defaultActions`, `actions`.

`bone[]` (`:473-509`): `name`, `parent` by name, `length`, `alpha`, four inheritance flags defaulting to true, `transform`, `type`.

`transform` (`_parseTransform`, `:2037-2052`) carries the abbreviated keys: `x`, `y`, `scX`, `scY` (default 1.0), and rotation as either `rotate` plus `skew` or the legacy `skX`/`skY`. If `rotate` and `skew` are present the legacy keys are ignored entirely.

`slot[]` (`:593-622`): `name`, `parent`, `displayIndex`, `zIndex`, `alpha`, `blendMode`, `color`, `actions`. **`zOrder` is not read from the slot** — it is assigned from array position (`:380`).

`skin[]` (`:624-663`): `name`, defaulting to `"default"` when absent, then per-slot display lists. A `null` display entry is meaningful.

`animation[]` (`:878-1208`): `name`, `duration` as an **integer frame count**, `playTimes`, `fadeInTime`, `scale`, `blendType`, plus timeline containers for main/action frames, `zOrder`, bones, slots, `ffd`, `ik`, and the generic 5.6 `timeline[]` form dispatched on numeric type.

Colour offsets use short keys `aO`, `rO`, `gO`, `bO`, `aM`, `rM`, `gM`, `bM`, with multipliers as percentages (`DataParser.ts:147-154`, applied at `ObjectDataParser.ts:2054-2063`).

## Derived Data and Footguns a Naive Writer Would Hit

Recorded in detail because "the parser is legible" is not the same as "authoring is safe".

1. **Skinned-mesh bind poses.** `_parseGeometry` (`:2106-2200`) expects `slotPose` (a six-element affine matrix) and `bonePose` (seven floats per bone). It transforms each vertex by `slotPose`, then by each bone's **inverted** `bonePose`, baking bind-space offsets. `_parseSlotDeformFrame` (`:1790-1874`) repeats this per keyframe.
2. **`bonePose` indices reference raw declaration order**, not the post-sort order (`:2130`, `:2172`). Reordering the bone array silently corrupts every skinned mesh.
3. **Slot z-order is array position** (`:380`), and the `zOrder` animation timeline's index pairs (`:1579-1636`) index the same order. Reordering `slot[]` silently rewrites both static and animated draw order.
4. **Frame durations must sum to the animation duration.** `_parseTimeline` (`:1267-1305`) overrides the last keyframe's duration. Real data ends every timeline with a zero-duration sentinel. A mis-summed set does not error — it silently mis-times.
5. **Rotation continuity is unrolled at parse time** (`:1638-1674`, `:1686-1713`), accumulating previous rotation and winding across frames. The parser is stateful within a timeline, so frame order matters and angles must follow the editor's convention.
6. **Bézier easing is resampled at parse time** (`_samplingEasingCurve`, `:147-221`). The `curve` array length must satisfy `length % 3 === 1` for the omitted-endpoint form, or a different indexing path is taken. Undocumented.
7. **Bone-graph cycles hang the process.** `ArmatureData.sortBones()` (`:225-265`) is a `while (count < total)` scan that `continue`s on unsatisfied parents. A cyclic parent chain is an **infinite loop, not an error**.
8. **Silent drops everywhere.** Unknown slot name in a skin discards displays (`:640`); unknown bone in an IK constraint returns null (`:513`); a missing mesh for a deform timeline is skipped (`:945`). A writer gets no failure signal.

## Rig Model — The Fixed-Cast Fit

**Skins are the strongest fit for RigTale.** `armature.skin` is an array keyed by name (`ArmatureData.addSkin`, `:356-371`). `BaseFactory._buildSlots` (`BaseFactory.ts:177-199`) composes by taking the default skin's display map and **overlaying** the selected skin's entries, so a costume skin need only declare the slots it changes. `BaseFactory.replaceSkin(armature, skin, isOverride, exclude)` (`:860`) swaps at runtime and can pull a skin from a **different armature entirely** (`:146-155`).

That is precisely RigTale's reusable-cast wardrobe primitive.

**Red-team caveat, and it is serious.** Scanning every `*_ske.json` in the repository found **zero armatures using more than one skin**. The multi-skin demo ships three *separate armatures*, and another ships per-costume files. The feature RigTale most needs is supported by the parser and factory but exercised by no shipped data. It requires an executable spike.

**Draw order has two independent axes and is animatable.** Static `zOrder` is slot array position; `zIndex` is an explicit per-slot integer. Final sort is `a._zIndex * 1000 + a._zOrder` (`Armature.ts:46-48`), which **breaks above 1000 slots**. Draw order is animatable two ways: a `zOrder` permutation-delta timeline (`TimelineState.ts:269-287`, `Armature.ts:185-207`) and a newer per-slot z-index timeline.

**Bones** resolve by parent name with forward-reference caching (`:337-357`), so declaration order is free for parenting. Transforms are 2D affine with independent rotation and skew, not a plain matrix. **IK** supports single-bone and two-bone chains with bend direction and weight, and is animatable. **Mesh deformation** supports vertices, UVs, triangles, per-vertex bone weights, shared meshes, and a free-form surface deformer, though weighted surface deform is an unimplemented `// TODO` (`:1988`).

## Time Model and the `pose(t)` Question

Time is authored in integer frames and consumed in float seconds; the parser converts using the armature frame rate (`:881-883`). Easing is baked at parse time into none, linear, quadratic, or a resampled Bézier table.

**Verdict: not a pure `pose(t)`, but convertible to one — with real caveats.**

For: timelines receive an **absolute** time (`BaseTimelineState.ts:197-224`), frame lookup is a direct table index, `AnimationState` exposes a `currentTime` setter that resets timeline play state (`:1440-1474`), and `Animation.gotoAndStopByTime/ByFrame/ByProgress` exist as public seek APIs.

Against: the object is a **mutable state machine you seek then flush**. `_setCurrentTime` early-returns when time is unchanged (`:148-150`) and `update()` skips frame evaluation unless tweening or dirty (`:220`) — memoisations that can stale. Frame index is cached and invalidated only on state or loop transitions. Dirty flags pervade bones, slots, z-index, and z-order. Enabling the animation cache **quantises time** (`AnimationState.ts:850-875`), turning pose evaluation into a frame-quantised lookup. The z-order permutation persists until another permutation frame arrives, making backward seeks across a z-order keyframe a plausible correctness hazard.

RigTale can obtain a deterministic pose by constructing a fresh armature per shot and seeking with caching off — but that is discipline imposed *around* the library, not a property *of* it.

## Renderer Boundary

Cleanly renderer-independent. A search for engine references across `DragonBones/src/` returns exactly one hit, a doc comment. The boundary is two abstract classes, `Slot` (`armature/Slot.ts:164`) and `BaseFactory`, plus proxy and event-dispatcher interfaces. Nine backend bindings ship, each 4–18 files.

**RigTale could take the format and the animation maths without adopting a renderer**, at the cost of a Slot subclass of roughly 200–400 lines by the size of existing bindings, plus a bundling shim for the pre-module `namespace dragonBones` TypeScript style.

## Binary Format

`.dbbin` is parsed by `BinaryDataParser.ts` and is fully open: magic `DBDT`, a length-prefixed UTF-8 JSON header, then packed typed arrays. It subclasses the JSON parser and calls it on the header — **the binary header is the same JSON schema**; only bulk numeric arrays move into the buffer. `ObjectDataParser._modifyArray` (`:2215-2292`) builds exactly that buffer from JSON, so the repository contains a de-facto JSON-to-binary encoder to work from.

## Maintenance Health — Correction: Not Dead, and This Review Read the Wrong Branch

**This section previously concluded "dead, with a 2025 rebranding twitch — the core runtime has had no functional change in over six years." That conclusion is wrong.** It was derived from `origin/master` alone and presented as a project-wide verdict "from full git history." An independent citation audit found the defect and it is confirmed against the clone.

`origin/6.0.2` is an active branch with a tip of **2026-01-23** and 33 commits to `DragonBones/src` in 2024–2026:

```
$ git log --format='%ad' --date=format:%Y origin/6.0.2 -- DragonBones/src | sort | uniq -c
   5 2024   27 2025    1 2026
$ git diff --stat origin/master origin/6.0.2 -- DragonBones/src | tail -1
 38 files changed, 2180 insertions(+), 226 deletions(-)
```

The commits are functional, not cosmetic. Verbatim subjects include `fix transform constrain bug`, `fix physics bug`, `fix shape weight parse error`, `fix timeline duration bug`, `shape支持skinned和ffd` (shape supports skinned and FFD), `路径约束的间隔增加百分比模式` (path constraint interval gains a percentage mode), and `修复ik和transform约束的技术顺序` (fix IK and transform constraint ordering). `ObjectDataParser.ts` alone gains **+375 lines** on that branch.

**Three consequences for this review.**

1. The "frozen format specification" framing is withdrawn. Physics, IK, path constraints, and shape skinning are under active change.
2. **The Recovered Schema section below describes the 5.6-era format on `master`, not the current format.** It does not say so and must not be treated as the schema of a live DragonBones.
3. The "bus factor one, dead since 2020" risk framing is withdrawn. The risk is different and arguably worse in a different way: development continues on a **non-default branch**, so the default clone of this repository silently yields six-year-old code.

The disposition remains `adapt` with a decision gate, but the gate now has a second question: which branch is the specification? Nothing in this review may be cited as evidence of DragonBones' maintenance state until it is re-audited against `origin/6.0.2`.

### Evidence that `master` is the stale branch

From `origin/master` only. These figures are why a default clone misleads: they are accurate for `master` and say nothing about the project.

| Period | Commits |
|---|---|
| 2017 | 144 |
| 2018 | 151 |
| 2019 | 38 |
| 2020 | 6 |
| 2021–2024 | **0** |
| 2025 | 2 |

Total 416 commits; **zero in the last 12 months, two in the last 36**. Roughly 60 authors, but `akdcl` and aliases account for about 61%, and that author last committed 2019-11-13. **The last substantive commit to `DragonBones/src` was 2020-03-23.**

The two 2025 commits are not substantive: one bumps a copyright year, the other changes a `console.info` URL to point at a rebrand. A new maintainer attached a Pixi 8 binding and repointed the website; the README now promotes a different commercial editor over the original tooling.

**The transferable lesson, which is why this section exists at all:** a default clone is not a project. Reading `origin/master` and reporting it as "full git history" produced a verdict that was false in every clause. Branch identity belongs in every maintenance claim this repository makes.

## Test Strategy — None

There are no tests, no test framework, and no CI. The files matching test patterns are all demo assets and demo scenes. A roughly 15,400-line runtime full of raw index arithmetic into typed-array buffers has zero automated verification. Any RigTale use inherits an unverified baseline.

## Patterns to Adopt or Adapt

- **Skin-as-overlay composition** (`BaseFactory.ts:184-195`): a base skin supplies all slot displays; a costume skin declares only overrides. Cheap, additive wardrobe — the single most valuable idea here.
- **Slot and display-list indirection**: a slot is a named socket owned by a bone; the thing drawn is a swappable display-list entry. The right cutout abstraction, and it decouples rig from art.
- **Bake easing at load time.** Resampling Bézier curves into a fixed sample table makes runtime evaluation branch-free and reproducible — a good fit for deterministic rendering.
- **Named-reference resolution with forward-reference caching**, so authoring order is free even though runtime order is topological.
- **Separate semantic layer from sequence within layer**, keeping the concept but replacing the `*1000` packing with a proper comparator.
- **Draw order as an animatable channel expressed as permutation deltas** — compact, diff-friendly, and well suited to agent-authored data.
- **Terse-with-defaults schema**, so generated data stays small and diffable.
- **Text and binary sharing one logical schema**: author in JSON, ship binary.

## Patterns to Avoid

- **Silent tolerance of malformed input.** RigTale's boundary must fail loudly with schema validation and hard errors, not non-throwing assertions and `continue`.
- **Positional identity.** Never let array index carry meaning. This is the single largest source of writer footguns here.
- **Unbounded loops as topological sort.** Use a real sort with explicit cycle detection.
- **Object pooling as an architectural commitment**, which couples lifetime to a global pool and is hostile to a pure `pose(t)`.
- **Dirty-flag-driven mutable evaluation.** Pose should be a function of rig, animation, and time with no retained per-frame state.
- **Frame-quantising time caches** that change results depending on whether caching is enabled.
- **Shipping without tests**, which is non-negotiable given RigTale's determinism premise.

## Questions Requiring Executable Evidence

| # | Question | Weight |
|---|---|---|
| 1 | Write a minimal armature from scratch — two bones, two slots, two image displays, one 30-frame timeline — and confirm the parser accepts it and produces the expected pose. | **Go/no-go on skipping the editor** |
| 2 | Author a second skin on the same armature and confirm skin selection and runtime replacement behave. | **Decisive: no shipped data exercises this** |
| 3 | Does seek-then-flush give bit-identical bone matrices regardless of previous time, including backward seeks across a z-order keyframe and across a loop boundary? | Decisive for determinism |
| 4 | What happens when frame durations do not sum to the animation duration, and is there any detectable signal? | |
| 5 | Can an armature be authored at version 5.6 when all shipped samples are 5.5? | |
| 6 | Confirm cyclic parent chains hang the sort, and price a pre-validation pass. | |
| 7 | Verify the 1000-slot cap empirically. | |
| 8 | Can bind poses be computed from a rest-pose rig without editor internals? | Only if mesh deform beyond rigid cutout is wanted |
| 9 | Can the core parse and animate under Node with no DOM, and how much Slot subclass is needed to extract transforms? | |
| 10 | Can the JSON-to-binary array builder be inverted into a standalone encoder that round-trips? | |

Route to `SPIKE-A002` (asset ingestion and rig authoring) and `SPIKE-A001` (orchestration).

## Conclusion

`adapt`, with a decision gate.

The rig model — bones, slots, display lists, named multi-skin overlays, and animatable draw order — maps unusually well onto RigTale's reusable-fixed-cast, layered-compositing premise, and the parser is legible enough that programmatic authoring of cutout rigs is a real option. The renderer boundary is clean, so the format and animation maths can be taken without inheriting a renderer.

It cannot be adopted as a live dependency: dead since 2020, bus factor one, zero tests, no writer, no schema, and a mutable dirty-flag runtime rather than the pure `pose(t)` RigTale requires. Vendoring means owning roughly 15,400 untested lines indefinitely.

The realistic shape is to **treat the JSON schema as a well-documented interchange format RigTale writes** — gaining compatibility with existing DragonBones art and viewers — while reimplementing evaluation as a pure function and discarding the object pool, dirty flags, and positional identity.

**If question 2 fails, DragonBones loses its strongest claim on RigTale and drops to `reference`.**
