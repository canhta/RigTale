# SPIKE-R001: Production Renderer Backends

## Question

Which existing engine, DCC backend, runtime, or custom library can compile RigTale's structured production contracts into the highest-quality reproducible video while remaining practical for a solo-maintained macOS and future cloud product?

## Preconditions

- `SPIKE-C001` has screened the candidate landscape.
- The representative animation fixture is versioned and approved.
- `SPIKE-A001` has defined and exercised the renderer-independent orchestration and frame-compilation requirements.
- Required visual features and expected frames are defined before adapter work begins.

## Initial Candidate Families

- Godot as a programmable 2D/3D production runtime.
- Blender as a Python-controlled 2D/3D DCC and rendering backend.
- Rive or another pre-rigged vector runtime where authoring and format constraints permit.
- Web/Node rendering using PixiJS, Skia, or a code-driven video framework.
- A Rust or native renderer only if existing backends fail a material requirement.

Candidate inclusion is provisional until competitive screening verifies its license, control surface, and relevance.

## Shared Fixture

The fixture must contain a ten-second 1920x1080 shot at 30 frames per second with:

- At least three simultaneous character instances.
- One quadruped and one vehicle.
- Hierarchical transforms and reusable motion clips.
- Sprite or expression swapping.
- Mesh deformation, masks, and explicit layer ordering.
- Camera movement and parallax.
- Audio-timed action cues.
- Exact frame stepping and isolated rerendering.

## Measurements

- Visual quality against approved reference frames.
- Ability to express the production without backend-specific episode logic.
- Deterministic frame output and explicit failure behavior.
- Preview and final-render parity.
- Preview latency, render time, peak memory, startup time, and output size.
- macOS packaging and Swift integration complexity.
- Linux/cloud/headless deployment complexity.
- Web preview or playback capability.
- License and redistribution obligations.
- Adapter size, custom code, test burden, and long-term maintenance risk.

## Exit Criteria

- Every qualified backend renders the same versioned fixture or has a documented blocking failure.
- Results include artifacts, commands, versions, measurements, and visual comparisons.
- Unsupported requirements are explicit and reproducible.
- The recommendation identifies a primary backend, optional adapters, and rejected alternatives, or records that more evidence is required.
- No renderer decision is accepted until an architecture decision record is approved.
