# SPIKE-C001: Competitive Landscape and Repository Screening

**Tracker:** `RGT-S001`

**Status:** Screening complete. Candidate execution remains deferred to approved fixture-based reviews and technical spikes.

## Result

Evidence locations: `docs/research/landscape.md` (index and dispositions), `docs/research/candidate-screening.md` (documentation-verified candidates), `docs/research/repository-reviews/` (15 dedicated records).

### Exit criteria

| Criterion | Required | Result |
|---|---|---|
| Candidates screened | ≥ 12 | 19 source-inspected at pinned commits, plus 29 documentation-verified |
| Dedicated deep-review records | ≥ 6 | 15 |
| Candidate groups covered | ≥ 3 | 4 |
| Material conclusions cite primary evidence at an exact revision | yes | yes, with rejected claims recorded where source contradicted documentation |
| No candidate dependency, setup script, example, or renderer executed | yes | confirmed; read-only throughout |
| Renderer candidates handed to `SPIKE-R001` | yes | recorded in the routing column of the index |
| `TODO.md` and the landscape index reflect results | yes | yes, including the shortlist with a gating question per candidate |

### The organising finding

**A permissively licensed runtime does not imply an open authoring path, and the second property is what determines fit.** An agent cannot produce content for a format it cannot write.

This distinction was not in the original screening criteria and is now recorded as an explicit criterion in `PR-A003`: a program must be able to produce valid content without a graphical interface and without a proprietary tool.

### Findings that changed downstream documents

- No candidate supplies **both** a reusable rig system and a deterministic frame-addressable renderer. Recorded against `PR-R005`.
- Lottie, the only animation format with a published machine validator, **cannot express a bone hierarchy**. Recorded against `PR-R005`.
- Rig-change propagation is unsolved or lossy in every system examined. Recorded against `PR-O03`.

### Self-corrections during screening

Three documentation-level claims were rejected because source inspection contradicted them, and one error in this spike's own output was corrected against source: the claim that Godot rig weight painting is editor-only was wrong, and Godot's disposition rose from `reference` to `adapt` as a result. All four are recorded in `docs/research/candidate-screening.md` and the affected review records.

### What screening deliberately did not do

No technology was selected. Every disposition is a screening outcome routed to a later spike or to `RGT-D010`.

### What screening failed to do, found by independent review

These are defects, not scope decisions. They are recorded here because `SPIKE-C001` was closed before they were found.

**1. The screening answered the output question and never asked the input question.** After 48 candidates and 15 review records, **no document in this repository names a single candidate layered-artwork ingestion format.** A scan of `docs/` for `PSD`, `OpenRaster`, `.ora`, `Krita`, `.kra`, `Procreate`, or `Clip Studio` returns exactly one hit, incidental, inside a licensing paragraph in `mlt-glaxnimate-lottie.md`.

`PR-A003` is `charter-backed` and requires ingestion of "at least one documented layered-artwork format". `SPIKE-A002`'s stated precondition is that `SPIKE-C001` "has screened relevant authoring tools, formats, and runtimes". **It screened runtimes and did not screen authoring formats.** The organising finding — that a program must be able to write a format without a GUI — was applied only to the write side, when it applies at least as forcefully to the read side: `.kra` and `.ora` are open ZIP+XML containers a program can write, PSD is reverse-engineered but has MIT read/write libraries, and `.procreate` and `.clip` are closed and are what the target users actually use.

**2. No vector-versus-raster decision exists, yet the determinism shortlist is composed almost entirely of vector rasterisers.** resvg/tiny-skia, ThorVG, Vello, and Skia are all vector paths. If the source artwork is layered raster — which is what "layered artwork ingestion" ordinarily means — the shortlist answers a question nobody asked, and the correct candidate set is a layered-raster compositing set that was never enumerated. This may be a substantial part of why the round concluded that no candidate supplies both a rig and a deterministic renderer: the search ran across two disjoint universes.

**3. "Lottie is the only animation format with a published machine validator" appears to be false.** glTF 2.0 publishes a JSON schema with an official validator, and unlike Lottie it expresses skins, joints, and weights — the exact capability `PR-R005` records Lottie as lacking. **This has not been verified from primary source and must not be relied on until it is.** It is recorded as an open retrieval task precisely because the same failure mode — asserting a superlative from search-index confidence — produced the withdrawn resvg claim.

**4. Colour management and alpha semantics were never asked of any candidate.** A scan of `docs/` for colour space, ICC, sRGB, premultiplied alpha, or linear light returns one hit. For layered cutout compositing, straight-versus-premultiplied alpha and blend space are the most common source of visible edge haloing and the most likely reason two renderer backends will disagree — which is the whole substance of `PR-R003` and `PR-R005`.

**5. No candidate has a throughput figure.** Not one frames-per-second measurement exists across 15 review records. The benchmark is 3,600–5,040 frames.

`RGT-S014` is created to close defect 1 and 2. Defects 3, 4, and 5 are routed in `TODO.md`.

## Question

Which open-source products, animation engines, code-driven video systems, and agentic production pipelines contain proven patterns that can reduce RigTale's product or engineering risk?

## Why This Is a Spike

Public descriptions do not establish how these systems model productions, control renderers, preserve editability, validate agent output, or behave under real workloads. This spike performs read-only discovery and source screening; executable claims are handed to fixture-based deep reviews or technical spikes.

## Scope

Screen candidates across four groups:

1. Animation engines and DCC backends.
2. Skeletal and vector animation runtimes.
3. Code-driven video frameworks.
4. Agentic video-production systems.

The initial candidate index is maintained in `docs/research/landscape.md`.

## Method

1. Discover at least twelve relevant candidates from primary sources.
2. Verify each canonical repository, license, current release, recent activity, and supported platforms.
3. Inspect official documentation and enough source at exact revisions to identify the production model, data flow, renderer boundary, extension mechanism, tests, and packaging model.
4. Score relevance to RigTale without installing dependencies or executing candidate code.
5. Select at least six repositories for dedicated deep-review spikes, covering at least three candidate groups.
6. Record which claims require the approved fixture and route them to repository-specific, orchestration, asset, or renderer spikes.
7. Record exact commits and file paths for every source-based claim.

## Screening Criteria

- Structured and editable production state.
- Fixed-cast or reusable-asset support.
- Skeletal, mesh, sprite, layer, camera, and timeline capabilities.
- Deterministic or frame-addressable rendering.
- Headless and cloud execution.
- Web and macOS integration.
- Agent tool, skill, planning, review, and recovery patterns.
- Asset provenance and licensing model.
- Test quality, maintenance health, and extension cost.
- Evidence of output quality rather than feature claims alone.

## Required Output Per Shortlisted Repository

- Strengths supported by primary documentation or source evidence.
- Weaknesses and failure modes.
- Patterns RigTale should adopt or adapt.
- Patterns RigTale should avoid.
- Questions that require a separate executable spike.
- Final disposition: `adopt`, `adapt`, `reference`, `reject`, or `defer`.

## Exit Criteria

- At least twelve candidates are screened.
- At least six dedicated repository-review spikes are created.
- Every material conclusion cites primary evidence and an exact revision where applicable.
- No candidate dependency, setup script, example, or renderer is executed during screening.
- Renderer candidates for the shared fixture are handed off to `SPIKE-R001`.
- `TODO.md` and `docs/research/landscape.md` reflect the results.
