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

The production system will not depend on generative image or video models for its core rendering path. It will enable an agent to direct a fixed cast and reusable asset library to produce multi-character, approximately three-minute 2D cutout music videos with layered compositing, predictable rendering, and production-quality review gates.

### Initial Users

- Independent creators producing children's music or educational animation.
- Small animation studios with approximately two to five team members.
- Educational-content teams that reuse a recurring cast across a video library.
- Developers integrating structured animation generation into another product.

Large broadcast studios are explicitly not the initial target customer.

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

1. **Produce the reference production.** Produce at least one publication-ready 2D cutout music video between 150 and 210 seconds from locked audio, timed lyrics, and versioned asset packs. The benchmark must include multiple shots, at least three simultaneous character instances, a reusable background system, one vehicle, and one quadruped character.
2. **Eliminate per-frame manual animation.** After characters and reusable motions have been published, the benchmark video must be generated without manual frame-by-frame drawing or per-frame keyframing. Human approval and structured shot-level edits remain allowed.
3. **Keep the entire production structured and editable.** Store characters, capabilities, scenes, shots, actions, choreography, camera instructions, timing, dependencies, and validation results in versioned structured formats. A user must be able to modify and re-render one shot without regenerating unaffected shots.
4. **Meet a defined production-quality threshold.** A release candidate must have zero blocking schema, dependency, missing-asset, unsupported-action, render, or audio-duration errors. Visual quality, educational clarity, pacing, synchronization, and repetition must pass a documented human review rubric with an average score of at least 4 out of 5.
5. **Demonstrate business value with target users.** Complete at least five problem interviews and two hands-on production evaluations with independent creators or studios of approximately two to five people. RigTale should demonstrate at least a 50% reduction in hands-on layout and animation time for the reference production compared with a documented manual cutout workflow using the same published assets.

## Scope Boundary

### Long-Term Product Scope

RigTale is a production-ready, agent-operated animation system covering the complete workflow from creative intent to publishable delivery:

- Educational or creative brief, script, lyrics, and audio-lock workflows.
- Storyboard, shot planning, animatic, layout, animation, compositing, review, rendering, QC, and delivery.
- Reusable fixed casts, backgrounds, props, motions, expressions, interactions, and production templates.
- Multi-character 2D cutout animation as the primary production model.
- Biped, quadruped, vehicle, prop, and environment asset archetypes.
- User-uploaded layered artwork and versioned production asset packs.
- Assisted layer mapping, pivot detection, rigging, and capability authoring.
- Future AI-generated characters and assets, provided they compile into the same validated production contracts.
- Typed, versioned `CharacterPack`, `ScenePack`, `PropPack`, `MotionPack`, `AudioTimeline`, `ShotPlan`, and `Episode` representations.
- Capability-aware agent planning that cannot silently request unsupported actions.
- Reusable solo motions, group choreography, role-based interactions, lip sync, expressions, camera direction, parallax, and layered compositing.
- Structured timeline editing and isolated shot regeneration or re-rendering.
- Deterministic preview and final-render pipelines.
- Automated visual, temporal, audio, dependency, licensing, and delivery validation.
- Human approval gates with versioned review notes and audit history.
- Local single-operator, collaborative studio, CI, and headless-server deployment profiles.
- Provider-neutral interfaces for language, speech, music, alignment, and future generative models.
- Localization, captioning, alternative aspect ratios, compilations, and reusable content packaging.
- Extensible renderer interfaces, with 2D cutout as the primary renderer and future 2D or 3D adapters permitted without changing the production model.
- Asset provenance, license metadata, reproducible builds, observability, backup, migration, and archival workflows.
- Complete operator, asset-authoring, deployment, troubleshooting, API, and contributor documentation.

### Release 1 Production Scope

Release 1 will be a complete production vertical, not a disposable prototype:

- Produce 150–210 second publication-ready 2D cutout music videos.
- Support multiple shots and at least three simultaneous character instances.
- Include biped, quadruped, and vehicle animation.
- Import at least one documented layered-asset format.
- Provide a license-audited reference asset library.
- Accept locked audio, lyrics, beat, phoneme/viseme, and timing data.
- Generate capability-valid shot plans, blocking, choreography, actions, reactions, and camera instructions.
- Support hierarchical transforms, motion clips, sprite swapping, masks, layer ordering, parallax, camera movement, and basic mesh or bone deformation.
- Provide group choreography and a bounded set of role-based interactions.
- Generate animatics, shot previews, final video, captions, manifests, and QC reports.
- Allow shot-level structured corrections and isolated re-rendering.
- Provide a usable local studio interface plus CLI/API automation.
- Include production tests, reproducible installation, failure recovery, and documented upgrade paths.
- Pass the reference-production quality and business objectives defined in the charter.

### Product Non-Goals

- Replacing the structured animation renderer with black-box text-to-video generation.
- Becoming a general-purpose professional drawing or frame-by-frame animation application.
- Reimplementing every capability of Harmony, After Effects, Moho, or Blender.
- Training proprietary foundation models as a core business requirement.
- Bundling unlicensed assets or imitating protected characters and visual identities.
- Silently generating unsupported motions or flattening projects into non-editable media.
- Making native 3D authoring a dependency of the primary 2D production workflow.
- Optimizing first for large broadcast-studio procurement, live performance capture, or mobile-only authoring.

## Solo Studio Operating Model

RigTale uses one development agent and two production agents supported by deterministic production tools.

### Development Agent

The Development Agent supports the Project Owner throughout the construction of RigTale:

- Researches business and technical questions using verifiable sources.
- Challenges assumptions and records unresolved questions as spike items.
- Maintains product requirements, architecture, implementation plans, and decisions.
- Implements, tests, reviews, and documents the repository.
- Protects product scope and validates each increment against the reference production.

The Development Agent is not part of the video production runtime.

Initially, its workflow is defined at repository level. Repeated and stable workflows will later be extracted into focused RigTale skills instead of creating one large skill.

### Studio Agent

The Studio Agent owns the complete creative workflow:

- Researches the subject when necessary.
- Writes the script, lyrics, and scene plan.
- Analyzes audio and timing.
- Selects available characters, sets, props, and motions.
- Produces structured shot, choreography, and animation instructions.
- Revises the production based on validation results.

The Studio Agent operates through specialized tools and structured production contracts rather than generating final video pixels.

### Red-Team Agent

The Red-Team Agent independently reviews the production plan and rendered output for:

- Factual or audience-safety problems.
- Unsupported assets or character actions.
- Timing, continuity, framing, and occlusion defects.
- Weak storytelling or mismatch with the production brief.

It returns structured findings to the Studio Agent for revision.

### Production Engine

All predictable operations remain deterministic software:

- Asset and rig validation.
- Timeline and scene compilation.
- Animation runtime.
- Rendering and compositing.
- Media encoding, caching, and versioning.

## Constraints

- RigTale must remain practical for one developer to build, operate, and maintain.
- The primary renderer must use structured 2D assets, rigs, motions, and scene data rather than direct AI video generation.
- The production runtime requires only the Studio Agent and Red-Team Agent. The Development Agent supports repository construction and does not run during video production.
- Predictable work must remain deterministic software.
- Existing productions must remain editable and renderable without calling an AI provider.
- Agent execution must use bounded context, retries, time, and cost.
- Rendering must be reproducible from versioned assets, production data, engine configuration, and random seeds.
- Unsupported character actions must produce explicit validation errors rather than silent visual degradation.
- Core production formats must be versioned and support documented migrations.
- The system must run locally on a standard creator workstation. Cloud AI and hardware acceleration may be optional extensions.
- Source code and bundled reference assets must permit legal open-source redistribution. Imported assets must retain license and provenance metadata.
- RigTale may study comparable production techniques but must not copy protected characters, artwork, music, or brand identity.

## Success Criteria

RigTale is successful when:

- It produces the reference three-minute, multi-character video through the complete structured workflow.
- It produces a second, materially different video without modifying engine source code.
- A production can be installed, opened, edited, resumed, and rendered on a clean supported machine using documented steps.
- A single shot can be changed and re-rendered without rebuilding unaffected shots.
- Final output passes deterministic validation, Red-Team review, and the defined human quality threshold.
- The workflow reduces hands-on layout and animation time by at least 50% against the documented manual baseline.
- Every distributed or imported asset has traceable provenance and license metadata.

## Key Risks

| Risk | Response |
|---|---|
| Structured animation cannot reach the required visual quality | Evaluate complete rendered shots early and expand reusable rigs, motions, expressions, and compositions based on visible gaps. |
| The product becomes too broad for solo development | Keep 2D cutout as the primary renderer and build complete vertical workflows before adding alternative renderers or advanced authoring. |
| Agents produce invalid or visually weak instructions | Restrict agents to typed contracts, declared asset capabilities, deterministic validators, and independent Red-Team review. |
| Asset preparation becomes the main production bottleneck | Define a strict import and rigging workflow, provide reusable reference packs, and automate only the repeated steps proven expensive. |
| Assets introduce copyright or redistribution problems | Require provenance and license metadata, audit bundled assets, and reject unknown or incompatible licenses. |
| The system depends too heavily on one AI provider | Keep provider adapters replaceable and ensure approved productions can be edited and rendered without an AI connection. |
| Technical success does not create sufficient user value | Validate the workflow with independent creators and compare hands-on production time against a documented manual baseline. |

## Go/No-Go Criteria

RigTale proceeds to broader production use only when all of the following are true:

- Two materially different productions can be completed without episode-specific engine changes.
- Final output meets the defined quality gates without manual frame-by-frame correction.
- A clean installation can reproduce, edit, resume, and render an existing production.
- Independent evaluations demonstrate at least a 50% reduction in hands-on layout and animation time.
- The asset pipeline can operate with legally usable, provenance-tracked resources.
- The system remains practical for one developer to maintain and one operator to run.

The product direction must be reconsidered if visual quality still requires extensive manual animation, each new production requires engine modification, or measured production cost approaches the equivalent manual workflow.
