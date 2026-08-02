# Repository Review: Rive Runtime

**Screened under:** `SPIKE-C001` (`RGT-S001`), read-only static source inspection.

**Repository:** https://github.com/rive-app/rive-runtime

**Inspected commit:** `4ac7b32798da0482e441ef09304dc3b480ed3ee5` (tag `runtime-v0.1.242`, committed 2026-08-02)

**License:** MIT. `LICENSE` and `renderer/LICENSE`, both "Copyright (c) 2020 Rive", byte-identical, obligation limited to notice retention. These are the only licence files in the repository.

**Disposition:** `reference`

## Purpose and Production Model

Playback runtime only. Content is authored in the proprietary Rive editor, exported as a `.riv` binary, and imported here for state-machine and animation playback through an abstract renderer interface.

`dev/defs/README.md` describes the schema as "Core definitions for Rive editor and runtimes", confirming the schema is shared with an authoring tool that is not in this repository.

## Decisive Finding: No `.riv` Writer Exists

This is the finding that determines the disposition.

| Evidence | Source |
|---|---|
| File magic `"RIVE"` at `include/rive/runtime_header.hpp:15`; the only method is `static bool read(...)` at `:47`. There is no `write`. Verified directly at the pinned commit. | `include/rive/runtime_header.hpp:15,47` |
| Both fingerprint call sites are read paths | `src/file.cpp:255`, `src/file.cpp:1421` |
| The code generator emits `deserialize(uint16_t, BinaryReader&)` only, with no serialize counterpart. Every `serialize` substring match in that file is inside `deserialize`. Verified directly. | `dev/core_generator/lib/src/definition.dart:484,496,499` |
| `BinaryWriter` exists but no consumer writes a `.riv`: property-reset blobs, test render-command serialization, Lua console buffer | `include/rive/property_recorder.hpp`, `include/utils/serializing_factory.hpp`, `include/rive/lua/rive_lua_libs.hpp:2156` |

Consequence: authoring RigTale productions into Rive content would require reverse-engineering and permanently maintaining a `.riv` encoder against `dev/defs/*.json` and a version gate (`File::majorVersion = 7`) that Rive controls unilaterally. Import-stack ordering constraints in `src/file.cpp:298-668` may encode invariants not expressed in the defs at all.

This contradicts RigTale's premise that AI writes structured production direction into a reviewable, diffable format.

**The authoring tool is also a paid proprietary service.** `https://rive.app/pricing` (accessed 2026-08-02) is positioned as "Free to create $9/mo to ship", with tiers Free, Cadet at USD 9 per seat per month capped at three seats, Voyager at USD 32 per seat per month, and Enterprise at USD 120 per seat per month.

An MIT runtime does not make the pipeline open. This is the general pattern the screening must detect: **runtime licence and authoring-path openness are separate questions, and only the second one determines whether an agent can produce content.**

## Data Contracts

`.riv` is an opaque binary: varuint core-object type key, then a stream of varuint property keys and type-dependent values, terminated by property key `0` (`src/file.cpp:128-193`). It is not diffable, not reviewable, and not agent-authorable.

The schema itself is structured and in-repository: 369 JSON definitions under `dev/defs/` with stable integer type and property keys, for example `dev/defs/bones/bone.json` (type key 40, `length` property key 89). There is no prose format specification in the repository; the defs are the closest available documentation.

## Renderer Boundary and Determinism

The `Renderer` and `Factory` abstraction (`include/rive/renderer.hpp`) is genuinely backend-agnostic, with Metal, Vulkan, D3D11/12, OpenGL/WebGL, WebGPU, CoreGraphics, Skia, and a null CPU context all present in source.

Determinism is an explicit, gated mode rather than an accident. `File::deterministicMode` (`include/rive/file.hpp:89`, defined `src/file.cpp:198`) gates every wall-clock and RNG source: `src/animation/state_machine_instance.cpp:155-166`, `src/constraints/scrolling/scroll_physics.cpp:11,37`, `src/animation/text_input_listener_group.cpp:14`. Time stepping is caller-owned via `Scene::advanceAndApply(float elapsedSeconds)` (`include/rive/scene.hpp:47`); the animation path holds no internal clock.

## Headless and Frame-Addressable Rendering

A headless PNG-writing path exists but only as a test binary. `tests/goldens/goldens.cpp` loads a `.riv`, steps `advanceAndApply(frameDuration)` in a loop, and writes PNGs, with `--headless`, `--backend`, and `--output` flags (`tests/goldens/goldens_arguments.hpp:44-92`). Offscreen macOS Metal rendering exists at `tests/common/testing_window_metal_texture.mm`.

Limitations: it is coupled to the test harness and an optional TCP Python harness (`tests/common/test_harness.cpp`), it is not packaged as a supported CLI, and it renders N frames evenly across an animation duration rather than supporting arbitrary time seek or shot-range addressing.

## 2D Cutout Capability

Present in source: bones and skinning (`src/bones/`), mesh deformation (`dev/defs/shapes/mesh.json`, `include/rive/bones/skin.hpp`), clipping and masks (`src/shapes/clipping_shape.cpp`), explicit draw order (`include/rive/draw_rules.hpp`, `include/rive/draw_target.hpp`, `src/dependency_sorter.cpp`), nested artboards (`src/nested_artboard.cpp`), state machines (`src/animation/state_machine_instance.cpp`), data binding (`src/data_bind/`, `src/viewmodel/`), text shaping via HarfBuzz (`src/text/font_hb.cpp`), and out-of-band asset loading (`include/rive/file_asset_loader.hpp`).

The capability set is a good match for cutout production. The authoring gap, not the feature set, is what disqualifies it.

## Test Strategy

Three layers, one of which is directly reusable:

1. **Silver tests** — a serializing `Factory` captures the ordered draw-command stream into a buffer and byte-compares it against a checked-in `.sriv` baseline. 252 baselines under `tests/unit_tests/silvers/`; driver `tests/unit_tests/runtime/serialized_rendering_test.cpp` steps a fixed `0.016f` per frame. Rebaseline via `REBASELINE_SILVERS`; mismatches dumped to `silvers/tarnished/`.
2. Golden images — `tests/goldens/`, `tests/gm/`, `tests/imagediff/`.
3. Unit tests — 172 test files with 379 `.riv` fixtures under `tests/unit_tests/`, Catch2.

## Patterns to Adopt or Adapt

- **Silver testing.** A serializing render backend that byte-compares the ordered draw-command stream gives a renderer-independent determinism oracle with no GPU and no pixel-diff flake. This is the strongest transferable pattern found and maps directly onto RigTale's isolated-rerender verification need.
- **An explicit determinism switch** that gates every clock and RNG call site, with the non-deterministic branch visible in source.
- **Caller-owned fixed-delta stepping** instead of a runtime-internal clock.
- **Declarative schema plus code generation** with stable integer keys — but RigTale must generate both reader and writer, and must emit a text production format.
- **Explicit version gate on load** returning a structured `unsupportedVersion` result (`src/file.cpp:274`).
- **Rebaseline-by-environment-variable with failed-output dumping**, which suits a solo maintainer.

## Patterns to Avoid

- A binary-only interchange format with no writer and no specification.
- Shipping only the read half of a schema-driven codegen while the write half lives in a closed tool.
- Coupling the only headless renderer to the test harness rather than to a supported CLI.
- Fetching dependencies with build-time shell scripts (`dependencies/macosx/get_*.sh`, `skia/dependencies/get_skia.sh`) instead of vendoring or lockfile pinning. This also leaves the third-party licence set unverified from source: HarfBuzz, SheenBidi, Yoga, libpng, libjpeg, libwebp, miniaudio, Luau, Skia, FFmpeg, and x264 obligations are not determinable from this repository.
- Divergent RNG behaviour between test and production builds (`include/rive/math/random.hpp`).

## Solo-Maintainer Cost

Approximately 812k lines across C/C++/Objective-C sources with shader pipelines for six graphics APIs, and no C ABI (`extern "C"` appears only in third-party shims). Swift integration would require a bespoke shim owned indefinitely. This exceeds what a solo maintainer can fork or patch meaningfully.

## Questions Requiring Executable Evidence

Routed to later spikes; none may be answered by screening.

| Question | Route |
|---|---|
| Do `dev/defs/*.json` contain enough information to encode a `.riv` this runtime accepts, or does `src/file.cpp:298-668` import-stack sequencing require undocumented knowledge? | Decisive gate; only worth running if the disposition is ever reconsidered |
| Does `deterministicMode` produce bit-identical pixel output across runs and machines? Silver tests prove draw-command equality, not pixel equality. | `SPIKE-R001` |
| Can `goldens --headless --backend metal` render without a window server on macOS, and at what cost for a 150–210 second sequence? | `SPIKE-R001` |
| Are silver buffers identical across Debug/Release and clang versions, given float accumulation in `advance`? | `SPIKE-R001` |
| Can `ViewModelInstanceRuntime` setters drive enough of a scene for a runtime-parameterised approach, or is structure immutably baked into the `.riv`? | `SPIKE-A001` |
| What licences do the script-fetched dependencies impose on a redistributed static library? | `SPIKE-R001` licensing check |

## Conclusion

`reference`. The authoring gap is decisive and no runtime quality offsets it: RigTale cannot adopt a production format it cannot write. The value extracted is pattern-level — silver testing, the gated determinism switch, caller-owned stepping, and schema-driven codegen — and the MIT licence imposes only notice retention on any borrowing.

Reconsideration as `adapt` would require the encoder question above to resolve affirmatively. It is not scheduled, because a format controlled by a closed editor would remain a permanent dependency on a third party's release decisions.
