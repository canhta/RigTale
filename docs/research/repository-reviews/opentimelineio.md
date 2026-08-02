# Repository Review: OpenTimelineIO

**Screened under:** `SPIKE-C001` (`RGT-S001`), read-only static source inspection with full commit history.

**Repository:** https://github.com/AcademySoftwareFoundation/OpenTimelineIO

**Inspected commit:** `0eebd211b2055f111e2c53d04b5581adc594c1fc`. 854 commits, 2016-09-06 to 2026-07-14. Declared version 0.19.0 (`OTIO_VERSION.json`, `src/opentimelineio/version.h`).

**Licence:** Apache-2.0 across the whole repository (`LICENSE.txt`; `NOTICE.txt` credits Pixar; every source file carries an SPDX identifier). Submodule dependencies — pybind11, RapidJSON, Imath, minizip-ng — are all permissive but are **not present in this clone**, so their contents are not verified from source.

**Disposition:** `reference` (strong), `adapt` for specific mechanisms. Not adoptable as RigTale's contract format.

## Why This Was Screened

RigTale must define versioned production contracts with schema migration, exact time, and content identity (`PR-A001`, `SPIKE-CS001`). OTIO is the most mature open implementation of exactly that requirement. The question was what to learn, not what to adopt.

## The Main Finding: Per-Type Schema Versioning

Every serialisable type declares a nested schema struct with a name and an integer version (`src/opentimelineio/effect.h:17-21`, `linearTimeWarp.h:16-21`). On the wire the pair becomes one string: `"OTIO_SCHEMA": "Clip.2"`.

**There is no top-level file format version.** `docs/tutorials/otio-file-format-specification.md` states each data type has a version instead, "to allow for more granular versioning."

This is the single most transferable design decision for RigTale. It lets `Episode`, `ShotPlan`, `CompiledShot`, and `AudioTimeline` evolve independently instead of forcing a lockstep bump.

### Migration machinery

The registry is `src/opentimelineio/typeRegistry.{h,cpp}`. `_TypeRecord` (`typeRegistry.h:174-190`) holds the current schema version plus maps of upgrade and downgrade functions. **Migrations are dictionary-to-dictionary transforms applied before object construction**, not object-to-object.

Read path (`_instance_from_schema`, `typeRegistry.cpp:359-437`) has three behaviours worth copying:

| Case | Behaviour |
|---|---|
| Unknown schema name | Constructs `UnknownSchema` retaining the original name, version, and raw dictionary, and **round-trips it back out unchanged** (`serialization.cpp:1090-1096`). Unknown data is preserved, not dropped. |
| File version newer than library | **Hard fail** with `SCHEMA_VERSION_UNSUPPORTED` (`:394-408`). Never guessed at. |
| File version older | Applies every registered upgrade in ascending order across the range (`:409-419`). Gaps are allowed. |

Write path (`Writer::_downgrade_dictionary`, `serialization.cpp:455-520`) looks the schema up in a caller-supplied version map and applies downgrades in a strict decrementing loop, **erroring if any step is missing** (`:498-517`). Downgrade must be gapless; upgrade need not be. That asymmetry is deliberate and correct.

Real registered migrations exist as worked examples: `Marker` 1→2 and 2→3, `Clip` 1→2, with matching downgraders (`typeRegistry.cpp:98-231`).

### Labelled version sets

`src/opentimelineio/CORE_VERSION_MAP.cpp` is a compiled-in table mapping a release label to a complete schema-name-to-version set, so a new library can emit a file targeting an old release wholesale — one argument instead of N. The Python layer adds a family indirection so third parties declare their own labelled sets.

**The map is generated and CI-enforced.** `Makefile:191-194` drives a generator, and `tests/test_serialized_schema.py:75-129` regenerates it and diffs against the checked-in file, failing with an instruction to re-run the target. The same pattern guards the generated schema documentation.

For a solo maintainer this is cheap and high-value: a forgotten version bump fails the build rather than shipping.

## Correction: Time Is Not Exact Rational

An earlier documentation-level screening recorded OTIO's time model as "exact rational, not floats". **Source inspection refutes this.**

`RationalTime` is a pair of doubles: `double _value, _rate;` (`src/opentime/rationalTime.h:403`), constructed from doubles (`:28`). It is "rational" only in the sense of value over rate. Rescaling is floating-point (`:70-75`). Addition and subtraction rescale the lower-rate operand (`:285-338`). `operator==` rescales before comparing, so equality is rate-dependent; `strictly_equal()` (`:99`) exists for exact identity of the pair. Rounding is explicit and opt-in via `floor()`, `ceil()`, `round()` (`:106-120`). SMPTE handling is a table of doubles with a snap tolerance of 0.1 (`rationalTime.cpp:17-78,455-470`). The format specification explicitly permits `NaN` and `Inf` in OTIO JSON.

**Verdict for RigTale: the *shape* is right — value plus rate, never seconds-as-float — but the *implementation* does not meet an exact-time bar.** RigTale should keep the shape and use an integer value with an integer rational rate.

Recorded as a rejected claim so the documentation-level version is not reintroduced.

## Composition Model

`Timeline` holds exactly one `Stack` named `tracks` plus an optional global start time (`timeline.h:16-120`). `Stack` and `Track` derive from `Composition` → `Item` → `Composable`; leaves are `Clip`, `Gap`, `Transition`. `Item` carries source range, markers, effects, and an enabled flag.

**`Clip` holds a map of media references plus an active key** (`clip.h:65-106`), defaulting to `"DEFAULT_MEDIA"` — multiple representations of the same shot with one active. That is directly analogous to a RigTale shot having draft, preview, and final renders, and is worth copying.

Media references are URL strings with **no resolver in the core**; relocatability is delegated to a Python media-linker plugin and to the bundling adapters. Effects are opaque: `Effect` is a name plus a metadata dictionary, and only `LinearTimeWarp` and `FreezeFrame` are concrete.

## Serialisation and Round-Trip

JSON via RapidJSON. The specification claims predictable key ordering for change tracking, and non-downgraded objects do emit the schema key first then fields in declaration order (`serialization.cpp:1117-1122`). But **downgraded objects are emitted by iterating an `AnyDictionary`, which is a `std::map` (`anyDictionary.h:28`) and therefore alphabetically sorted** — so downgraded output is not key-order-identical to normal output.

Worth knowing before treating OTIO JSON as byte-stable.

Round-trip evidence is strong: per-type golden baselines under `tests/baselines/`, written, parsed, and compared, then re-read and compared again. But the comparison helper normalises `1.0` against `1` on numeric fields (`src/py-opentimelineio/opentimelineio/test_utils.py:16-28`) — an admission that float formatting is not stable.

**There is no content hashing or digest anywhere in the core.** A search for hash, sha, md5, or checksum returns only `std::type_info::hash_code`. Object instancing is compiled out and the specification states OTIO has none.

This matters for RigTale: content identity is a stated requirement (`SPIKE-CS001`) and OTIO offers no prior art for it.

## Plugin Mechanism

Manifest-driven and Python-side. Plugin kinds are adapters, media linkers, hook scripts, hooks, schemadefs, and version manifests. An adapter is a module path plus suffixes implementing read and write with hooks fired around them. Only three adapters ship in-tree — JSON, and the zip and directory bundles; the README confirms all others moved to separate repositories after v0.16.

`schemadef` plugins let third parties register new schemas with their own versions into the same registry — the extension model RigTale would need if it ever exposed contracts to plugins.

## Test Strategy and Governance

54 test files totalling 16,868 lines, mixing pytest and C++ unit tests plus golden baselines and the generated-artifact diff tests. CI covers Ubuntu, Windows, and macOS across Python 3.9–3.13 including MSYS2, with coverage reporting.

Governance is genuine and verified from source: `GOVERNANCE.md` confirms it is an Academy Software Foundation project under Linux Foundation policies, with a TSC charter, code of conduct, security policy, CLAs, and a DCO sign-off requirement.

## Maintenance Health

854 commits with 68 in the last 12 months. Per year: 2018:107, 2019:113, 2020:76, 2021:158, 2022:135, 2023:27, 2024:47, 2025:62, 2026:34. One hundred distinct author identities; the top contributors span multiple organisations including Netflix and Autodesk.

Since 2025 the active set is thinner — roughly three primary contributors plus about ten others — but it is multi-organisation and clearly alive. Tags run through v0.18.1 with HEAD at 0.19.0 development.

**Verdict: healthy, slowed from its 2021–22 peak, low bus-factor risk relative to a solo project.** This is the only candidate in the screening round with real foundation governance.

## What OTIO Explicitly Does Not Do

Verified by absence, not by claim. Searching the public headers for keyframe, bezier, interpolation, curve, or rig returns **zero hits**. There is no rasteriser, no image buffer type, and no codec path. Effects carry only a name and metadata. There is no character, skeleton, joint, or layer-transform concept.

OTIO models **when a piece of media occupies a slot on a track**, and delegates what the pixels are entirely to external URLs.

For RigTale that is exactly the boundary line: **OTIO models the shot-plan and edit layer and has nothing to say about the compiled-shot pose layer.**

## Patterns to Adopt or Adapt

1. **Per-type schema versioning with no file-level version**, encoded as one string.
2. **Migrations as dictionary-to-dictionary functions** registered against a target version and applied before object construction.
3. **Asymmetric version policy**: upgrade old files silently, hard-error on files newer than the library. Do not guess forward.
4. **Unknown-schema pass-through** so unrecognised nodes survive a read-modify-write cycle.
5. **Labelled version sets** so targeting an older release is one argument.
6. **Generated artifacts diffed in CI**, so a forgotten version bump fails the build.
7. **Per-type golden JSON baselines** with write, parse, compare round-trips.
8. **A media-reference map with an active key**, analogous to a shot carrying draft, proxy, and final renders.

Adapt rather than adopt: the double-based time type, the absence of content identity, and the key-ordering asymmetry under downgrade.

## Questions Requiring Executable Evidence

| Question | Route |
|---|---|
| Empirically probe `RationalTime` drift: chained rescales across 23.976/24/29.97/30/48, 100k accumulated additions at mixed rates, and float formatting stability across platforms | `SPIKE-CS001` |
| Is round-trip byte-stable, especially on the downgrade path where key ordering appears to change? | `SPIKE-CS001` |
| Register a custom schemadef with three versions and both migration chains; confirm the gapless-downgrade constraint and the newer-file hard error end to end | `SPIKE-CS001` |
| Clean-build time and wheel size on macOS with four submodules plus pybind11 | `SPIKE-CS001` |

## Conclusion

`reference` (strong), `adapt` for the versioning architecture.

Do not adopt OTIO as RigTale's contract format: it has no animation, no rig, no exact-integer time, and no content identity, and adopting it pulls a C++ build plus pybind11 plus four submodules into a solo macOS project.

Do adapt its versioning architecture close to wholesale. It is the most mature open implementation of exactly RigTale's stated schema-versioning and migration requirement, and Apache-2.0 makes its ideas and JSON conventions freely reusable. Keep it on the table as a possible **export** target for the shot-plan and edit layer only.
