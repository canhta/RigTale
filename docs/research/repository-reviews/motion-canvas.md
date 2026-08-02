# Repository Review: Motion Canvas

**Screened under:** `SPIKE-C001` (`RGT-S001`), read-only static source inspection.

**Repository:** https://github.com/motion-canvas/motion-canvas

**Inspected commit:** `7b91435c301d530351dcf5ebb91dd139c002e405` (2026-07-02). The clone is shallow at depth 1; commit cadence and contributor diversity are not derivable from it.

**License:** MIT (`LICENSE`, "Copyright (c) 2022 motion-canvas"). **Divergence inside the repository:** `packages/ffmpeg/package.json` declares `"license": "GPLv3"` — the only non-MIT package. This matters if RigTale ever vendors or links that package.

**Declared version:** `3.17.2` (`packages/core/package.json`).

**Disposition:** `reference`

## Purpose and Production Model

A programmatic video framework: author TypeScript, get frames. It is not a character-animation system. A project is a list of scene modules (`packages/core/src/app/Project.ts:19-29`); a scene is a factory `(view: T) => ThreadGenerator` (`packages/core/src/scenes/GeneratorScene.ts:32-34`).

## Decisive Finding: Production State Is Code, Not Data

To learn a scene's duration, the engine must execute it. `GeneratorScene.recalculate()` (`packages/core/src/scenes/GeneratorScene.ts:208-243`) steps frames until the scene signals it can transition out, then records the duration. `PlaybackManager.recalculate()` (`packages/core/src/app/PlaybackManager.ts:164-187`) does this for every scene to derive total duration.

**Total production length is not knowable without running the animation frame by frame.** There is no timeline intermediate representation, no keyframe table, and no serialisable scene state. `reset()` (`GeneratorScene.ts:285-299`) reconstructs the runner through `threads(...)`; state lives in generator stack frames, which cannot be inspected or serialised.

This is disqualifying for RigTale's production model on three counts: an agent cannot emit it, a validator cannot check it before rendering, and there is no state to snapshot for isolated shot rerender.

The only inbound data contract is `Variables`, a flat `Record<string, unknown>` injected into signals (`packages/core/src/scenes/Variables.ts:17-33`).

## The One Genuine Data Artifact

Motion Canvas persists `.meta` sidecar files (`packages/vite-plugin/src/utils.ts:21`) holding `SerializedTimeEvent` records of the form `{name, targetTime, offset}` (`packages/core/src/scenes/timeEvents/TimeEvent.ts:22-26`) plus a per-scene PRNG `seed` (`packages/core/src/scenes/SceneMetadata.ts:12`).

Named, externally-authorable time markers with a persisted seed are exactly the shape RigTale needs for agent-authorable, validator-checkable timing. This is the most transferable idea in the repository.

## Time Model and Determinism

Float seconds plus integer frames; no rational or exact time. `packages/core/src/app/PlaybackStatus.ts:14-25`: `secondsToFrames = Math.ceil(seconds * fps)`, `framesToSeconds = frames / fps`. Every duration rounds up to a whole frame. `PlaybackManager.ts:45-48,197` advances `this.frame += this.speed`, so `frame` is integral only when `speed === 1`.

Thread time is a float accumulator (`packages/core/src/threading/Thread.ts:113-117`), mitigated by re-anchoring after each `waitFor` (`packages/core/src/flow/scheduling.ts:55-61`), so drift does not compound across waits.

Randomness is reproducible: a per-scene PRNG is re-seeded from persisted metadata on every reset (`GeneratorScene.ts:150,289`).

Rasterisation goes through browser Canvas2D and browser font shaping, so byte-identical output is a property of the browser build, not the framework. No golden-image test exists.

## Frame Addressability

There is no arbitrary-frame seek. `PlaybackManager.seek()` (`packages/core/src/app/PlaybackManager.ts:83-108`) selects a scene, resets to its first frame, and replays linearly to the target. The scene boundary is the finest re-entry point and there is no state snapshot mechanism.

For a 150–210 second production this makes isolated shot rerender cost proportional to the timeline, not the shot.

## No Headless Renderer

A search for `puppeteer|headless` across `packages/` yields exactly one hit, in `packages/e2e/src/app.ts:16`. The FFmpeg exporter is a browser client talking to the Vite dev server over a bridge (`packages/ffmpeg/client/FFmpegExporterClient.ts`, `packages/ffmpeg/server/FFmpegBridge.ts`). Rendering is initiated by a human in the editor UI.

RigTale requires CLI and CI operation. This alone rules out adoption.

## Capability Evidence

**No skeletal rigging.** A search for `skeleton|skeletal|bone|armature|puppet|inverse.kinematic|mesh.deform|morph.target` across all TypeScript in the repository returns zero real hits. The node inventory is vector, shape, text, and image only: `Bezier, Circle, Code, Curve, Grid, Icon, Img, Latex, Layout, Line, Node, Path, Polygon, Ray, Rect, SVG, Shape, Spline, Txt, Video, View2D` (`packages/2d/src/lib/components/`).

Reusable "rigs" would be ordinary TypeScript component composition. There is no rig format, asset registry, or publish/version concept.

**Compositing is genuinely capable.** `packages/2d/src/lib/components/Node.ts` provides `zIndex` (`:83,348`) with children sorted by z (`:516`), `compositeOperation` (`:117,372`), `opacity` (`:406`), `filters` (`:413`), `shaders` (`:433`), and a decision point for routing through an offscreen cache buffer (`:1351-1355`) with `cacheBBox()` (`:1409`).

**Masks are geometric clipping only** — `Layout.ts:188,665` `clip`, `:857-866` `context.clip()`. No matte or alpha-mask node exists.

**Camera is a real strength.** `packages/2d/src/lib/components/Camera.ts` (359 lines) provides `zoom` (`:102`), `reset` (`:139`), `centerOn` (`:160-182`), `followCurve` / `followCurveReverse` / `followCurveWithRotation` (`:212-305`), and `Camera.Stage` (`:343`), the multi-view mechanism that makes parallax practical.

**Audio** is one project-level track (`Project.ts:47-52`) plus per-scene sounds, with real-time desync correction in the player — playback machinery, not render mixing.

## Test Strategy

31 test files concentrated on signals, threading, tweening, and value types, with snapshot directories under `core/src/flow/__logs__`, `core/src/threading/__logs__`, and `2d/src/lib/components/__logs__`.

**There are zero unit tests for `PlaybackManager`, `Player`, `Renderer`, `Scene`, `GeneratorScene`, or `PlaybackStatus`.** The frame-to-time conversion, the seek algorithm, the recalculate loop, and the export loop are untested outside a single end-to-end rendering test. The subsystems RigTale would depend on most are the unverified ones.

## Maintenance Signal

The tip commit is docs-only and dated 2026-07-02. `CHANGELOG.md`'s top entry is `3.17.2` dated **2024-12-14**, matching the declared core version — roughly nineteen months with no core release despite a 2026 tip commit. Pinned toolchain is TypeScript 5.2, Vite 4, ESLint 8.

This is consistent with dormancy or maintenance-only status. It is a signal, not a conclusion: the shallow clone cannot confirm it, and full history is required.

## Patterns to Adopt or Adapt

- **`SerializedTimeEvent` `{name, targetTime, offset}`** as the primitive for agent-authorable, validator-checkable timing.
- **A persisted per-scene seed** re-applied on every reset, so randomness is reproducible by construction.
- **`Camera` with curve-following and a multi-view stage** as a design for RigTale's camera and parallax.
- **The offscreen-buffer decision logic** in `Node.ts:1351-1355` — when to allocate a cache buffer for a subtree.

## Patterns to Avoid

- **Deriving duration by executing the animation.** RigTale must know duration from production data before any frame is rendered.
- **Generator-stack-as-state**, which is unserialisable and forecloses snapshotting.
- **Linear replay-to-seek** with the scene as the finest re-entry point.
- **Float-second accumulation with `Math.ceil` frame quantisation** and no exact-rational option.
- **Requiring a human in the editor UI to start a render.**
- Mixing a GPLv3 package into an otherwise MIT distribution without flagging it.

## Questions Requiring Executable Evidence

| Question | Route |
|---|---|
| Do `.meta` time-event files round-trip losslessly when written by an external tool rather than the editor? | `SPIKE-A001` |
| Is Canvas2D text rendering stable across macOS versions? | `SPIKE-R001`, if any browser-rasterised candidate advances |
| Full-depth git history to confirm or refute dormancy | Cheap follow-up, not an executable spike |

## Conclusion

`reference`. The camera design, the compositing model, the signal and tweening core, and the `.meta` time-event contract are worth studying and selectively reimplementing.

It is not adoptable: production is executable code whose duration requires simulation, there is no headless render path at all, there is no skeletal or cutout capability, seek is linear replay from a scene boundary, and the timing and rendering classes have no unit tests. Core releases appear stalled since December 2024.
