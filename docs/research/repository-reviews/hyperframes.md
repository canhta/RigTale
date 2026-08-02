# Repository Review: HyperFrames

**Screened under:** `SPIKE-C001` (`RGT-S001`), read-only static source inspection with full commit history.

**Repository:** https://github.com/heygen-com/hyperframes

**Inspected commit:** `74fadf69c464c0e0658bd7a6b740986fc3aceba8` (2026-08-01). 3,496 commits, 14 workspace packages.

**Licence:** Apache-2.0 (`LICENSE`, "Copyright 2026 HeyGen, Inc."). Third-party terms in `CREDITS.md`; no vendored GPL source in tree.

**Disposition:** `reference`, bordering on `adapt` for the determinism layer specifically.

**How it entered screening:** it is the renderer Code2MP4 shells out to. Resolving its licence turned it into a candidate in its own right.

## The Determinism Claim Is Substantially Supported

This is the first candidate whose determinism claim is backed by both a mechanism and tests that assert **byte equality rather than similarity**. That makes it the most valuable reference artifact found for RigTale's hardest problem.

### The mechanism

`packages/producer/src/services/fileServer.ts:216-368` builds a virtual-time shim injected as a pre-head script before all authored scripts:

- `Date` is replaced with a virtual constructor whose `now()` returns the virtual time (`:315`), installed via `Object.defineProperty`.
- `performance.now` is redefined to return the same (`:327-334`).
- `requestAnimationFrame` is replaced with a queue; callbacks fire only on an explicit flush invoked from the seek, and receive virtual time as their timestamp (`:336-345`, `:357-361`).
- Optional seeded random and `crypto.getRandomValues`, reseeded per frame from virtual time (`:223-266`).

### Absolute seek, not delta

`packages/engine/src/services/frameCapture.ts:2781` and `:3773` compute the target time from the frame index and quantise it; the seek is issued as an absolute time (`:2400-2401`). **Every frame is an independent absolute seek; no accumulator exists in the loop.**

### Three caveats

1. **Seeded random is off on the default local path** (`fileServer.ts:375`) and **on only for distributed chunks** (`packages/producer/src/services/distributed/renderChunk.ts:690`). The same composition can be reproducible distributed and not reproducible locally, by design.
2. **`setTimeout` and `setInterval` are captured as originals but never replaced** (`fileServer.ts:279-282`). The doc comment at `:204` claiming the shim freezes the timer pipeline overstates what the code does.
3. The project's own documentation concedes that non-container local renders "may show slight differences due to platform-specific font rendering and Chrome version".

## The Tests Are the Most Valuable Finding

**Two tests assert byte-level reproducibility of pixels, not similarity to a golden.**

`packages/producer/src/services/distributed/crossWorkerIdempotency.test.ts` renders the same plan and chunk twice into different directories and asserts raw buffer equality on every output file, across both the image-sequence and encoded-video paths, on two different chunks. Its header states that rendering the same plan and chunk on two different workers must produce byte-identical output.

`packages/producer/src/services/distributed/chunkBoundary.test.ts` renders a 60-frame fixture for each of six animation adapters at one chunk and at four chunks, and asserts **per-frame byte equality between the two runs**. It deliberately uses an image sequence rather than a video container because container bitstreams encode keyframe placement directly and would show legitimately different bytes for identical pixels. It pins the expected frame count so a truncating regression cannot pass vacuously.

**This is precisely the test RigTale needs for isolated shot rerender**: re-render one shot alone and assert its frames are byte-identical to the corresponding range of the full render.

Supporting layer: 929 test files, 72 golden video baselines compared by signal-to-noise checkpoints — approximate similarity, explicitly distinguished from the byte-equality path — with regression running per pull request.

**Weakness:** both byte-equality tests soft-skip when the host browser cannot render. On a macOS development machine they may silently no-op.

## The Two Disqualifying Gaps

### 1. No isolated shot rerender

**RigTale's core requirement does not exist as a user-facing capability.**

The CLI render options are frame rate, quality, workers, encoding parameters, GPU, output, container, and variables. **There is no range, frames, start, end, or segment option.** The `keyframes` subcommand with shot and range arguments is an onion-skin diagnostic image, not a render.

The internal primitive exists and is well specified — `CaptureStageInput.frameRange` (`packages/producer/src/services/render/stages/captureStage.ts:101-112`) documents capturing a sub-range with absolute frame indices so the page's virtual clock matches an in-process render at that frame. But it is consumed only by distributed chunk rendering, and the documentation adds the constraint that the range length **must equal the total frame count** (`:110`). It is a worker-sharding mechanism, not a partial-composition render.

Sub-compositions loaded from separate HTML files mean "render one shot" is achievable by rendering that shot standalone — but **there is no supported path to re-render a frame range of the parent and splice it into an existing master.** RigTale would build that layer.

### 2. No rig or compositing capability

Absent entirely. No rig, skeleton, bone, IK, puppet, cutout, character, or lip-sync concept exists anywhere in the core, producer, or engine packages. "Layering" is DOM plus CSS stacking order, and the documentation is explicit that the track-index attribute **does not** control z-ordering. There is no compositor, no layer graph, and no per-layer render target.

## Composition Input Model: Hybrid, and It Fails RigTale's Standard

The declarative half is real and rich — data attributes for composition identity, start, duration, track index, media start, playback rate, volume, nested composition source, and variables, including relative timing expressions.

**But motion is JavaScript.** The canonical composition contains a script tag loading an animation library and an inline script building a timeline assigned to a global registry. The linter *requires* it: rule `missing_timeline_registry` (`packages/lint/src/rules/core.ts:363-365`).

Tellingly, **HyperFrames itself had to build an AST parser and writer for the animation JavaScript** (`packages/parsers/src/gsapParserAcorn.ts`, `gsapWriterAcorn.ts`, with golden fixtures) to make motion editable as data. That is precise evidence that the durable artifact is code, and that recovering structured data from it requires parsing arbitrary JavaScript.

**Assessed against RigTale's standard:** the timing and layout layer is data and adoptable; the animation layer is executable code with an AST-parsing escape hatch. HyperFrames does not clear the bar that disqualified Motion Canvas, Revideo, and Code2MP4 — unless RigTale generates the script deterministically from its own data model and treats the HTML as a compiled artifact rather than a source of truth.

## Animation Adapters

All first-party adapters are absolute-seek; none is delta-advanced.

| Adapter | Verdict |
|---|---|
| GSAP | Absolute. Pauses, nudges to force dirty state, then seeks total time. |
| CSS | Absolute. Sets current time per element and pauses. |
| WAAPI | Absolute but **baseline-relative**; correctness depends on a baseline captured at discovery time. Most fragile under random access. |
| Anime.js | Absolute. Requires manual registration. |
| Lottie | Absolute. The legacy percentage path rounds through duration; lowest precision of the set. |
| Three.js | **Delegated, not enforced.** The adapter sets a global and dispatches an event; the composition must listen and redraw. A clock-driven scene would be delta-advanced and the adapter would not stop it. |
| d3, leaflet, map providers | Readiness gates only; they do not seek. |

The adapter contract is documented and requires idempotent seek, random-access support, and no post-commit async.

## Dependency and Licence Posture

**GSAP is not a dependency of the render path** — it appears only in the browser UI packages, is not vendored, and compositions **fetch it from a CDN at render time**. That contradicts the project's own documented rule against render-time network fetches, and the README example pins only a major version.

**FFmpeg is expected on PATH, not bundled**, resolved through an environment variable then standard locations including the Apple Silicon Homebrew prefix. Default encoding uses GPL-licensed codecs, invoked as a separate process, so there is no contamination of Apache-2.0 source — but a GPL-enabled FFmpeg is required for the default path. No bit-exact or deterministic muxing flags were found; encode determinism rests on fixed quality settings and pinned group-of-pictures parameters.

## Validation Behaviour

`lint` runs rule files covering core, composition, adapters, animation library, media, captions, fonts, textures, and slideshow. Named rules include a **`non_deterministic_code`** rule (`packages/lint/src/rules/core.ts:620`) that pattern-matches wall-clock and random calls at **error** severity, with the explicit reason that each render worker initialises independently so random values diverge across chunks.

**Lint is a pre-render gate** (`packages/cli/src/commands/render/execute.ts:166-175`), but blocking is strictness-gated — it refuses only under strict flags, not by default.

Additional commands validate console output and contrast, sample layout at hero frames with machine-readable output for agents, sample midpoints for overflow, and check the toolchain.

## Determinism Enforced at Plan Time

`packages/producer/src/services/render/planValidation.ts:1-27,86` **hard-rejects GPU encoding, hardware browser GL, and system fonts at plan time** for distributed renders — a deliberate determinism-over-speed trade, refusing before the plan is frozen rather than failing mid-render.

Seam handling is by construction: every worker seeks by absolute frame index, so there is no cross-worker state. Encoder seams are handled explicitly by forcing a keyframe at each chunk boundary and disabling alt-ref frames so chunks concatenate losslessly (`packages/engine/src/services/chunkEncoder.ts:242-243,332-336`).

**Risk:** a static-frame deduplication heuristic is on by default (`frameCapture.ts:2461-2712`), reusing the previous frame's buffer for frames predicted static from timeline analysis. A wrong prediction silently duplicates a frame — in a system whose main claim is determinism.

## Maintenance and Governance: High Risk

- 3,496 commits, first on 2026-03-10, HEAD 2026-08-01 — **project age 144 days**. There is no historical baseline.
- **The public history is a squash export.** The seventh commit lands 401 files and 54,545 insertions after an eleven-day gap. Pre-publication development history does not exist publicly.
- Author concentration: top one 45.1%, top two 68.4%, top three 88.5%. **Bus factor 1–3.** One corporate domain accounts for 93.7% of non-merge commits.
- **Explicit vendor-controlled governance.** `CONTRIBUTING.md:193-197` states a benevolent-dictator model where core maintainers at the vendor have final say. No governance file, no CLA, no DCO.
- **353 tags in 132 days — roughly 2.65 releases per day**, decelerating. Still `0.x`; the security policy supports only `0.x`.
- Community surface is thin: external contributors account for roughly 6% of commits.
- Telemetry is on by default in the CLI, opt-out only.

**Verdict: a 4.7-month-old, vendor-controlled, `0.x` project shipping 2.65 releases per day with a bus factor of 1–3 and no pre-publication history is a fast-moving dependency, not a stable substrate.** Apache-2.0 makes forking legally clean; the author concentration makes forking practically expensive.

## macOS

macOS is clearly the maintainers' development platform, with concrete handling for browser resolution, a Gatekeeper crash hint, FFmpeg discovery accounting for GUI-spawned processes not inheriting shell PATH, and hardware-accelerated encoders selected under a GPU flag.

**But hardware encoders are not bit-reproducible, and the project knows it** — plan validation hard-rejects GPU encoding for distributed renders. The GPU flag is a determinism-off switch.

**CI runs macOS only for a trivial shim test.** Every render, regression, and byte-equality job runs on Linux. **No macOS render is covered by CI** — which is also why the byte-equality tests may silently skip on a Mac.

## Patterns to Adopt or Adapt

1. **The virtual-time shim as a pre-head injected script.** Roughly 150 lines, self-contained, Apache-2.0, and directly liftable. Adapt it to also replace the timer functions — the gap HyperFrames left.
2. **A shared frame-quantisation function used on both sides of the process boundary**, computed identically in the host and the page. Divergent rounding across that boundary is a classic off-by-one-frame bug.
3. **The chunk-boundary equality test as a per-adapter contract**: render at one worker versus four, assert per-frame byte equality, output an image sequence so container keyframe placement cannot mask the comparison, and pin the absolute frame count so truncation cannot pass vacuously.
4. **Ban nondeterminism at plan time, not at render time**, with typed non-retryable error codes.
5. **A lint rule that fails on wall-clock and random calls in authored content**, with the divergence rationale in the message.
6. **Closed-GOP encoding for concatenation seams.** Directly applicable to splicing a re-rendered shot into a master without re-encoding the rest.
7. **A discarded warm-up capture** so the first real frame in a worker sees what the same frame in a single-worker render saw. A subtle seam bug RigTale would otherwise hit.
8. **Content-addressed plan hashing** as the cache key for whether a shot has changed.

## Patterns to Avoid

- Motion as script blocks requiring an AST parser to read back. RigTale's direction-as-data premise should not need one.
- Differing determinism guarantees between local and distributed paths.
- Doc comments that overstate the code.
- Fetching animation libraries from a CDN at render time.
- Frame-reuse heuristics enabled by default in a system whose main claim is determinism.
- Soft-skipping determinism tests when the host browser is unavailable — a determinism test that silently no-ops on the maintainer's own platform is not covering that platform.
- A flag that silently disables reproducibility.

## Questions Requiring Executable Evidence

| Question | Route |
|---|---|
| Can chunk rendering be driven directly to render only one shot's frame range, and does the result concatenate cleanly into an existing master? The equal-length constraint suggests the plan must be re-frozen per shot — measure whether that cost destroys the point. | `SPIKE-R002` |
| Do the byte-equality tests actually run on macOS, or do they soft-skip? If they skip, macOS determinism is entirely unverified. | `SPIKE-R001` |
| Byte- or metric-identical output for two full renders of a 150–210 second composition on the same Mac, hours apart, outside a container? | `SPIKE-R001` |
| Wall-clock and memory for roughly 5,400 frames with 4–6 animated character groups, and does eight workers hold byte equality at that scale? | `SPIKE-R001`, `PR-R006` |
| Does the baseline-relative adapter survive true random access — seek far forward, back, then forward again — with identical pixels? | `SPIKE-R002` |
| Does disabling static deduplication change output pixels on a representative composition? | `SPIKE-R001` |

## Conclusion

`reference`, bordering on `adapt` for the determinism layer.

HyperFrames is the first candidate whose determinism claim is backed by a mechanism **and** by tests asserting byte equality rather than similarity. The virtual-time shim and the two reproducibility tests are a genuine Apache-2.0 reference implementation of the hardest problem RigTale faces, and those specific artifacts are worth lifting.

As a platform it fails on two independent grounds: **isolated shot rerender does not exist as a user-facing capability**, and there is **zero rig, character, or layered-compositing capability**. A third concern compounds them: the durable artifact is HTML plus animation JavaScript — the executable-production-state pattern RigTale has already rejected — and the project's own AST parser is the proof that the pattern is costly.

Governance adds risk rather than deciding it. Apache-2.0 keeps a fork legally clean; a 4.7-month-old vendor-controlled `0.x` project at 2.65 releases per day is not a stable dependency for a solo maintainer.
