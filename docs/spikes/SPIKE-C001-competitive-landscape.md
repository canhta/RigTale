# SPIKE-C001: Competitive Landscape and Repository Screening

**Tracker:** `RGT-S001`

**Status:** Active. Screening is read-only; candidate execution is deferred to approved fixture-based reviews and technical spikes.

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
