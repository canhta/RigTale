# RigTale Project Charter

**Project slug:** `rigtale`

**Document status:** Business justification approved. The remaining charter sections will be added only after review and approval.

## Business Justification

### Problem

Small animation studios and independent creators can design appealing 2D characters, but producing a publishable three-minute music video still requires substantial manual work:

- translating lyrics and locked audio into a storyboard and animatic;
- laying out shots, cameras, props, and multiple characters;
- selecting and timing poses, expressions, and reusable motions;
- synchronizing animation with lyrics, phonemes, musical beats, and sound effects;
- managing rig, background, prop, and shot versions;
- reviewing continuity, layer ordering, lip sync, framing, and render output.

General-purpose text-to-video systems are a poor default for this workflow because they do not reliably preserve character identity, are difficult to edit at the shot or action level, have unpredictable generation cost, and produce flattened media rather than a structured production project.

### Opportunity

RigTale will be an open-source animation production system in which designers provide structured puppets, backgrounds, props, and approved motion assets while an AI agent writes the production program that directs them. A deterministic animation engine compiles that program into editable previews and final video.

The MVP will not depend on generative image or video models. It will test whether an agent can direct a fixed cast and reusable asset library to produce a multi-character, approximately three-minute 2D cutout music video with layered compositing, predictable rendering, and production-quality review gates.

### Initial Users

- Independent creators producing children's music or educational animation.
- Small animation studios with approximately two to five team members.
- Educational-content teams that reuse a recurring cast across a video library.
- Developers integrating structured animation generation into another product.

Large broadcast studios are explicitly not the primary MVP customer.

### Core Value

- Preserve the visual quality and style established by a designer.
- Guarantee stable character identity by reusing published rigs and assets.
- Reduce repetitive layout, timing, and animation operations.
- Make videos editable through a typed timeline and scene representation instead of regeneration.
- Reuse characters, motions, sets, props, and production templates across episodes.
- Make renders reproducible, testable, and cost-predictable.
- Support repackaging one production into standalone videos, compilations, short clips, and localized versions.

### Investment Thesis

RigTale's durable advantage will not be ownership of a foundation model. It will come from the production system surrounding the models:

1. A versioned `CharacterPack` format with an explicit capability manifest.
2. A typed scene and animation intermediate representation designed for agent use.
3. A motion grammar appropriate for clear, low-stimulation preschool content.
4. A deterministic multi-character choreography compiler.
5. Asset-aware planning that never requests unsupported actions silently.
6. Automated visual, temporal, audio, and production-quality validation.
7. A license-audited library of reusable casts, motions, sets, props, and production templates.

### Hypothesis to Validate

A small studio or creator will adopt RigTale if it can produce an approximately three-minute video that:

- requires no manual frame-by-frame animation or per-frame keyframing;
- preserves the approved visual style and puppet rig;
- allows individual shots, actions, and timings to be edited as structured data;
- reaches a quality threshold suitable for publication; and
- is materially faster and less expensive to revise than a comparable manual cutout-animation workflow.

## Vision

RigTale enables small creative teams to turn locked audio and a reusable cast into editable, publication-ready animated videos by directing structured assets with AI instead of generating pixels.

RigTale should operate like an agent-controlled animation studio: artists retain authority over character design, rigs, visual style, and reusable motion assets, while the system automates production planning, shot construction, choreography, timing, compositing, validation, and rendering.

Every production must remain inspectable, reproducible, versionable, and editable as structured data. The initial product will focus on multi-character, approximately three-minute 2D cutout music videos. Future character generation, assisted rigging, localization, and alternative 2D or 3D renderers must integrate through stable production contracts rather than requiring a replacement of the core pipeline.

## Objectives

1. **Produce the reference MVP video.** Produce at least one publication-ready 2D cutout music video between 150 and 210 seconds from locked audio, timed lyrics, and versioned asset packs. The benchmark must include multiple shots, at least three simultaneous character instances, a reusable background system, one vehicle, and one quadruped character.
2. **Eliminate per-frame manual animation.** After characters and reusable motions have been published, the benchmark video must be generated without manual frame-by-frame drawing or per-frame keyframing. Human approval and structured shot-level edits remain allowed.
3. **Keep the entire production structured and editable.** Store characters, capabilities, scenes, shots, actions, choreography, camera instructions, timing, dependencies, and validation results in versioned structured formats. A user must be able to modify and re-render one shot without regenerating unaffected shots.
4. **Meet a defined production-quality threshold.** A release candidate must have zero blocking schema, dependency, missing-asset, unsupported-action, render, or audio-duration errors. Visual quality, educational clarity, pacing, synchronization, and repetition must pass a documented human review rubric with an average score of at least 4 out of 5.
5. **Demonstrate business value with target users.** Complete at least five problem interviews and two hands-on pilot evaluations with independent creators or studios of approximately two to five people. The MVP should demonstrate at least a 50% reduction in hands-on layout and animation time for the reference production compared with a documented manual cutout workflow using the same published assets.
