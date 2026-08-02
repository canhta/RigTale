# Repository Review: Code2MP4

**Screened under:** `SPIKE-C001` (`RGT-S001`), read-only static source inspection.

**Repository as declared:** https://github.com/code2mp4/code2mp4 (`package.json` `repository.url`, matching the clone's git remote).

**Inspected commit:** `91d7ba4501d8c6e48b4889a647b21af847f8185c` (2026-05-11). The clone is shallow and blob-filtered; only one commit is visible.

**License:** Apache-2.0 (`LICENSE`, `package.json`). Note the inconsistency below.

**Disposition:** `reference`

## Provenance: Canonical Repository Now Partially Resolved

The landscape index recorded this candidate as "canonical repository unverified". Screening narrows but does not close the question.

The source contradicts its own declared identity in several places, all pointing to a prior project named "Open Video" under the org `openvideo-ai`:

- `NOTICE` line 1-2: "Open Video — AI-driven video production / Copyright 2026 Open Video contributors".
- `LICENSE` appendix copyright holder is "Open Video contributors", not Code2MP4.
- `.github/CODEOWNERS`: `* @openvideo-ai`.
- `.env.example` header "Open Video — Environment Configuration", default data directory `.ov`.
- `apps/server/src/agent-runner.ts:62`: "Legacy OV_ prefix kept for backward compat".
- `CHANGELOG.md` records a "Brand reinforcement" entry removing `openvideo-ai/openvideo` references.

`README.md` states "Apache 2.0 © Code2MP4 contributors", which does not match the `LICENSE` file's own holder string. `NOTICE` also declares derivation from Open Design (`nexu-io/open-design`, Apache-2.0) and a dependency on HyperFrames (HeyGen, Inc.). Derivation is visible in code: `apps/server/src/video-skills-loader.ts:6` says "Analogous to Open Design's skills.ts", and every `video-skills/*/SKILL.md` carries an `od:` frontmatter block.

**Unresolved:** whether `code2mp4/code2mp4` is a rename of `openvideo-ai/openvideo` or a third-party rebrand of someone else's repository. The shallow clone cannot answer this. Sole visible author is `AIBUBB技术团队 <driknix@gmail.com>`; `CHANGELOG.md` implies the project was roughly one week old at the pinned commit.

Recorded as an unresolved provenance question, not a finding against the project.

## Decisive Finding: No Renderer of Its Own

Frames and video are produced entirely by an external `hyperframes` CLI. `apps/server/src/renderer/hyperframes-bridge.ts:193-258` spawns `npx hyperframes render --format mp4 ...` with `PUPPETEER_HEADLESS: 'true'`; the same file shells out for lint, validate, inspect, TTS, transcribe, and background removal.

That CLI is **not declared as a dependency anywhere**. The root `package.json` declares only `@hyperframes/player` (a browser preview component); `pnpm-lock.yaml` contains no non-scoped `hyperframes` entry and no `gsap` entry. The renderer is an unpinned global install resolved by `npx` at runtime, and GSAP is fetched from a CDN inside generated output (`apps/server/src/pipeline.ts:447`, `examples/product-launch/motion-source.html:32`).

A "deterministic MP4" claim cannot survive an unpinned renderer plus a runtime CDN fetch.

## Capability Mismatch

There is no character-animation capability at all. A repository-wide search for rig, skeleton, puppet, bone, armature, cutout, sprite, or layered-compositing terms across `apps/`, `packages/`, `video-skills/`, `motion-systems/`, `templates/`, and `examples/` returns only CSS loading-skeleton classes, "character count" readability checks, and typewriter text effects.

The element vocabulary is text and UI primitives only: `headline | subhead | body | card | button | icon | image | counter | code-block | divider | logo | badge` (`packages/contracts/src/index.ts:158`). `SceneMotion` (`:174`) applies entrance, emphasis, and exit to DOM selectors, not to joint hierarchies. Scenes are absolutely positioned full-bleed divs crossfaded by opacity (`pipeline.ts:443`); z-order is incidental CSS, not a compositing model.

Target output is 25–30 second text-card marketing motion graphics, a different medium from RigTale's benchmark.

## Code Versus Data

The pipeline crosses the boundary RigTale intends to hold.

| Stage | Output | Source |
|---|---|---|
| Director | JSON storyboard | `pipeline.ts:296` demands "ONLY a JSON storyboard" |
| Scene Agent | **HTML with `<style>` and `<script>`** | `pipeline.ts:346` |
| Assembly | Deterministic string concatenation into one `index.html` | `pipeline.ts:394` |

Structure is recovered from free-form model text by regex: `parseStoryboard` (`:481`) regex-matches a JSON blob then retries after stripping trailing commas and smart quotes; `extractSceneHtml` (`:500`) tries four successive regexes. There is no tool-call or JSON-mode contract, and neither function has any test.

Three JSON Schema files exist under `packages/contracts/schemas/`, but **no validator is wired in** — a search for `ajv|zod|valibot|json-schema` across `apps/`, `packages/`, and `tools/` matches only the `$schema` strings inside the schema files. Validation is hand-rolled in `validateStoryboard()` (`pipeline.ts:243`). The richest contract, `SceneSpec`, is declared and never consumed.

## Determinism and Isolated Re-render

Determinism is enforced only as prompt text: `pipeline.ts:381` and `apps/server/src/prompts/video-contract.ts:19` forbid `Math.random()`, `Date.now()`, and `repeat:-1`. There is no seed, no fixed-timestep loop, and no frame-hash comparison. `quality-check.ts:113` marks the render-determinism dimension `render-deferred`, so it always passes.

Isolated re-render does not exist. `POST /api/pipeline/:jobId/scene/:num/retry` (`server.ts:756-822`) re-runs the agent for one scene, but rendering is always whole-composition (`server.ts:894-935`), and assembly is blocked unless all scenes are done (`server.ts:833`). There is no content hashing, no cache key, no dependency graph, and no dirty tracking. A one-word text change re-renders the entire video.

Configuration is also not plumbed: `server.ts:770,834` hardcode the motion palette and `:900` hardcodes the music track, contradicting the UI's pickers.

## Test and Output Evidence

Eight test files, roughly 1,000 lines, all pure unit tests with no rendering: SQLite CRUD, PATH detection, loader and project IO, prompt composition, quality heuristics. **Zero tests touch `hyperframes-bridge.ts`, `media.ts`, `assembleComposition`, `parseStoryboard`, or `extractSceneHtml`** — the fragile joints and the entire render path are untested. CI runs typecheck, build, and tests on Ubuntu only; no render smoke test, no macOS runner.

Real rendered artifacts are committed (`docs/demos/*.mp4`, 25–30 seconds each) alongside hand-written `examples/*/motion-source.html`. That is genuine evidence HTML plus GSAP reaches MP4 at 1920×1080/30fps for text-card graphics. However, the example HTML files do not match `assembleComposition`'s output structure, no test exercises them, and there are no golden frames or output hashes. Nothing proves rerunning the pipeline reproduces those files.

Per the research plan, a committed demo is a discovery signal, not evidence of pipeline quality.

## Patterns to Adopt or Adapt

- **Layered prompt stack with the hard contract pinned last**, plus unit tests asserting order and a size budget (`apps/server/src/prompts/system.ts`, `apps/server/tests/prompts.test.ts:51,93`).
- **`AGENTS.md` as a numbered non-negotiable contract with an explicit "Never do" list.**
- **A single-file renderer bridge** with typed progress events and a `checkSystemRequirements()` preflight (`hyperframes-bridge.ts:369`) — but with the renderer pinned as a real dependency.
- **Filesystem-first job state reloaded before every mutation** (`server.ts:793`), so runs survive restarts and stay diffable.
- **A pre-render gate that hard-fails** and persists a machine-readable report (`server.ts:906-926`).
- **Cheap deterministic content heuristics** instead of an LLM judge (`quality-check.ts:69-97`).
- **Deterministic FFmpeg-synthesised sound effects** via `lavfi` graphs (`apps/server/src/audio.ts`) as a zero-asset audio fallback.
- **Credential hygiene**: strip `*_API_KEY` and `*_TOKEN` from the spawned child environment (`agent-runner.ts:48-54`), and path-traversal defence with a test (`projects.ts`, `modules.test.ts:170`).

## Patterns to Avoid

This repository is most useful to RigTale as a documented negative example.

- **The agent's durable artifact being executable animation code.** This is the central divergence from RigTale's premise, and it visibly produces regex scraping, untestability, per-scene style drift, and unbounded failure modes.
- Recovering structure from free-form model text by regex instead of constrained output plus schema validation.
- Declaring JSON Schemas without wiring a validator.
- CDN-loaded runtime libraries inside output artifacts.
- Invoking the renderer via `npx` against an undeclared package.
- Whole-timeline-only rendering with no dependency graph.
- Hardcoding style and asset defaults in HTTP handlers while exposing pickers in the UI.
- Passing scene-to-scene visual coherence by feeding the first 200 characters of each previous scene's HTML into the next prompt (`pipeline.ts:352`) — unreliable and grows with scene count.

## Licensing Obligations

Apache-2.0 with a `NOTICE` file, so any reuse must preserve `LICENSE` and `NOTICE`, state changes, and carry forward the Open Design and HeyGen attributions. Two additional obligations are not surfaced in `NOTICE`:

- `music/*` are CC-BY-3.0 (Kevin MacLeod / incompetech.com) per `music/MUSIC.md`; attribution is required in any video shipping those beds.
- `NOTICE` lists "GSAP (Standard License)", which is not an OSI licence and carries commercial-use restrictions. GSAP is loaded into every generated composition.

`@hyperframes/player` and the `hyperframes` CLI are HeyGen copyright with terms not stated in this repository.

## Questions Requiring Executable Evidence

None are scheduled, because the disposition does not depend on them.

| Question | Note |
|---|---|
| Does `assembleComposition` output actually pass `hyperframes lint/validate/inspect` and render? | Nothing in-repo demonstrates the assembler's own output being rendered |
| Is HyperFrames rendering bit-reproducible across runs and platforms? | Deferred entirely by the repository |
| ~~What are the actual licence terms of the `hyperframes` CLI?~~ **Resolved.** `https://github.com/heygen-com/hyperframes` is Apache-2.0 (`https://raw.githubusercontent.com/heygen-com/hyperframes/main/LICENSE`, "Copyright 2026 HeyGen, Inc."), accessed 2026-08-02. HyperFrames is therefore a candidate in its own right and is added to the index; see `docs/research/candidate-screening.md`. | Closed |
| Terms of `@hyperframes/player` specifically | Open |
| Does HyperFrames support subrange rendering with frame-accurate stitching? | Would matter only for engine-layer reuse |
| Is DOM capture viable at 150–210 seconds on macOS? | Committed demos are 25–30 seconds |

## Conclusion

`reference`. Code2MP4 has no character-rig, fixed-cast, cutout, layered-compositing, camera, or interaction capability; no isolated re-render or caching; no renderer of its own; and no enforced determinism. Its medium and duration differ from RigTale's benchmark, its maintenance signal is a single author over roughly one week, and its provenance is unresolved.

Its value is in agent-orchestration mechanics — the prompt stack, the filesystem-first job state, the hard-failing pre-render gate, the renderer bridge shape, and the credential hygiene — and in concretely demonstrating what breaks when the agent emits executable animation code rather than structured direction.
