# Repository Review: Revideo

**Screened under:** `SPIKE-C001` (`RGT-S001`), read-only static source inspection.

**Repository:** https://github.com/midrender/revideo

**Inspected commit:** `b5de67a009a55aa2768a1e178b0446b2479a0b4e` (2026-07-15). The clone is shallow at depth 1.

**License:** MIT (`LICENSE`), **byte-identical to Motion Canvas's, including the "Copyright (c) 2022 motion-canvas" line**. All 20 package manifests declare MIT; unlike upstream, no GPLv3 package is present.

**Declared version:** `0.11.0` (pre-1.0).

**Relationship:** fork of Motion Canvas. See `docs/research/repository-reviews/motion-canvas.md` for the shared core analysis; this record covers what the fork changes.

**Disposition:** `reference`, leaning `defer`

## What the Fork Adds

**A working headless renderer — the thing upstream lacks entirely.** `packages/renderer/package.json` describes itself as "A headless renderer for revideo" and depends on `puppeteer ^25.3.0`, `vite ^8.1.2`, and `@revideo/ffmpeg`. `packages/renderer/server/render-video.ts:93-114` launches `puppeteer.launch({headless: true, args:['--single-process']})` alongside a programmatic Vite server; parameters travel by URL query string (`:64-75`) and IPC uses `page.exposeFunction` for completion, failure, and progress (`:193-219`).

Public API: `renderVideo({projectFile, variables, settings})` (`:394`) and `renderPartialVideo({workerId, numWorkers, ...})` (`:459-490`).

**Audio mixing moved out of the browser.** `packages/core/src/app/Renderer.ts:279-289` collects a per-frame asset manifest via `getMediaByFrames()` and hands it to `exporter.generateAudio(mediaByFrames, from, to)` (`packages/core/src/app/exporter/FFmpegExporter.ts:123`), then merges (`:140`). The `AssetInfo` shape is `{key, type, src, playbackRate, volume, currentTime, duration}` (`Renderer.ts:17-26`).

**This per-frame asset manifest is the only real intermediate data structure either project produces.**

Also added: `cli`, `telemetry`, `player-react`, and scene-graph `Audio.ts` / `Media.ts` / `Rive.ts` nodes.

## What the Fork Removes — Three Regressions Against RigTale's Needs

| Removed | Consequence |
|---|---|
| `scenes/SceneMetadata.ts`, and `meta` / `random` from `GeneratorScene` | The seeded per-scene PRNG is gone. `Random.ts` still exists but is no longer wired in. **Reproducible randomness is lost.** |
| The whole `scenes/timeEvents/` directory | The `SerializedTimeEvent` `{name, targetTime, offset}` contract — the single most RigTale-shaped artifact upstream had — is deleted. |
| `2d/src/lib/components/Camera.ts` | No camera component. Parallax becomes manual per-layer transforms. |

`PlaybackManager` also loses `goBack` / `goForward` / `goTo` / `seekSlide`.

The fork improved the render path and regressed exactly the properties RigTale would have wanted.

## The Disqualifying Property Is Inherited Intact

`GeneratorScene.recalculate()` (`packages/core/src/scenes/GeneratorScene.ts:208-243`) is unchanged: duration is still discovered by executing the animation frame by frame. Production state remains executable generator code with unserialisable stack-frame state.

## Frame Addressability and Render Cost

Seek is still linear replay from a scene boundary. Worse for range rendering: `packages/core/src/app/Renderer.ts:264-272` runs `recalculate()` — a full simulation of all scenes — then `reset()`, then `seek(from)`; `getMediaByFrames` (`:386-401`) then performs the identical sequence a **second time**.

Rendering a 10-second tail of a 200-second production simulates roughly 200 seconds twice before emitting a frame. Isolated shot rerender at RigTale's benchmark length is therefore not achievable at acceptable cost: every worker replays from frame 0.

## Determinism Exposure

Output bytes depend on the bundled Chromium build, its font stack, and its rasterisation path; `--single-process` is force-appended. The result is hermetic only if Chromium is pinned externally.

The `Rive.ts` node (156 lines) delegates to `@rive-app/canvas-advanced`, a real skeletal runtime, but it is hostile to frame addressability: `Rive.ts:83-97` computes `timeToAdvance = this.time() - this.lastTime`, mutates `lastTime`, and calls `animation.advance(...)` and `artboard.advance(...)` **inside `draw()`**, scheduled through `rive.requestAnimationFrame` (`:117`). Since `GeneratorScene.render()` may invoke `draw()` up to ten times per frame while resolving promises (`:169-177`), and seeking re-draws, a backward seek feeds a negative delta into a stateful animation instance. Not reproducible under seek.

This is a concrete, citable instance of a general rule RigTale should adopt: **a deformation runtime must be a pure `pose(t)` function, not a delta-advanced mutable machine.**

## Telemetry

`packages/telemetry/src/index.ts:4-7` uses `posthog-node` against `https://eu.posthog.com`, fired from the render path at `render-video.ts:178`. Opt-out is environment-only, `DISABLE_TELEMETRY === 'true'` (`telemetry/src/index.ts:53`). Default-on network calls inside a render path are unacceptable for a reproducible, offline-capable pipeline.

## Capability Evidence

Same as upstream: no skeletal rigging, no cutout capability, vector/shape/text/image nodes only, geometric clipping but no matte or alpha-mask node. Compositing (`Node.ts` z-index, composite operation, opacity, filters, offscreen cache) is inherited and remains capable.

## Test Strategy

28 test files, concentrated on signals, threading, tweening, and value types. Dropped upstream's `createDeferredEffect.test.ts`, `createEffect.test.ts`, and `utils/proxyUtils.test.ts`, and the 2d components directory has no snapshot log directory.

**Zero unit tests for `PlaybackManager`, `Player`, `Renderer`, `Scene`, `GeneratorScene`, or `PlaybackStatus`** — the same gap as upstream, covering exactly the subsystems the fork most changed.

## Maintenance Signal

Tip commit is docs-only, 2026-07-15. No `CHANGELOG.md`. Version `0.11.0`. Toolchain is current — Node ≥22.12, TypeScript ^6.0.3, Vite ^8.1.2, ESLint ^10.6.0, lerna ^9.0.7 — against upstream's TypeScript 5.2 / Vite 4 / ESLint 8. This is consistent with active maintenance, in contrast to upstream. The shallow clone cannot establish contributor count or bus factor.

Revideo still imports its Vite plugin under the upstream binding name (`packages/renderer/server/render-video.ts:16`).

## Patterns to Adopt or Adapt

- **The `AssetInfo` per-frame manifest** (`Renderer.ts:17-26`) as a template for a resolved-asset record per shot or frame.
- **The `Variables` injection seam** as the minimal parameterisation contract — but typed and schema-validated, not `Record<string, unknown>`.
- **Worker frame-range partition plus FFmpeg concat** (`render-video.ts:276-323`) as the shape for parallel rendering — adapted so slices are *named shots with independent initial state*, not arithmetic frame slices.
- **`renderPartialVideo` returning `{audioFile, videoFile}`** as an isolated-unit output contract.
- **Audio mixed from a manifest at the FFmpeg layer**, decoupling audio determinism from browser playback.

## Patterns to Avoid

- Inheriting a code-not-data production model while improving only the render path.
- Running the same full simulation twice per render.
- Advancing external animation state inside `draw()`.
- Deleting the seeded PRNG and the persisted timing artifacts that made the upstream reproducible.
- Default-on telemetry in a render path.
- Depending on a bundled browser for rasterisation determinism.

## Questions Requiring Executable Evidence

| Question | Route |
|---|---|
| Does a render of the same project on the same machine produce byte-identical MP4s across runs? Across two Chromium builds? | `SPIKE-R001` |
| Does the multi-worker path match a single-worker render at the seams? `client/render.ts:117` applies an `offset = workerId === 0 ? 0 : 1` frame adjustment that looks like an off-by-one guard and needs empirical checking. | `SPIKE-R001` |
| What is the measured wall-clock cost of the double `recalculate()` over a 200-second production, and does Chromium survive it under `--single-process`? | `SPIKE-R001` |
| Can `renderPartialVideo` be driven with an externally supplied frame range decoupled from `workerId` arithmetic? | `SPIKE-R002` |
| Can a Rive artboard be posed at an absolute time rather than advanced by delta? | `SPIKE-A001` |

## Conclusion

`reference`, leaning `defer`.

Revideo solves two problems upstream does not — headless scripted rendering and parallel worker rendering with FFmpeg-side audio — and those designs are directly instructive. But it inherits the disqualifying property intact: production is executable generator code whose duration requires simulation. It regressed on determinism, timing artifacts, and camera. Isolated shot rerender is not achievable at acceptable cost because every worker replays from frame zero.

Reconsideration would require a spike showing byte-reproducible output and a tolerable double-`recalculate` cost at 200 seconds. Neither is scheduled ahead of the fixture.
