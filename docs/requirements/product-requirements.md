# RigTale Product Requirements

**Status:** v1 draft.

**Authority:** The approved project charter defines product intent and scope. This document translates it into testable product requirements. Requirements marked as hypotheses must be revised after the linked research or spike; they are not accepted architecture decisions.

## 1. Product Definition

RigTale is an open-source, agent-operated animation production system. It converts creative intent and reusable structured assets into an editable production program, then uses deterministic software to animate and render a fixed cast. AI directs the production; it is not the core pixel-generation or frame-rendering path.

The primary production model is multi-character 2D cutout animation with layered compositing. A reference production is a publication-ready video between 150 and 210 seconds containing multiple shots, at least three simultaneous character instances, a reusable background system, one quadruped character, and one vehicle.

## 2. Requirement Confidence

| Classification | Meaning |
|---|---|
| `charter-backed` | Required by the approved charter and changeable only through an explicit scope revision. |
| `hypothesis` | Plausible product behavior that must be validated through research, a fixture, or a spike. |
| `decision-pending` | Product need is known, but the implementation or quantitative threshold requires evidence and a decision record. |

No hypothesis may be silently promoted to an accepted technical choice.

## 3. Primary User Outcomes

### PR-O01 — Direct a reusable cast (`charter-backed`)

A creator can provide a creative prompt, brief, script, lyrics, audio, or a combination of these inputs. The Studio Agent must turn the available intent into structured scene, shot, character, action, choreography, camera, and timing instructions that use only published asset capabilities.

### PR-O02 — Produce without per-frame manual work (`charter-backed`)

After the required assets, rigs, and reusable motions are published, the reference production must not require manual frame-by-frame drawing or per-frame keyframing. Human approvals and structured shot-level corrections remain supported.

### PR-O03 — Preserve structured editability (`charter-backed`)

The production must retain versioned creative inputs, assets, capabilities, shots, actions, timing, dependencies, validation, and review state. A user must be able to modify and rerender one shot without regenerating unaffected shots.

**Evidence raises this requirement's priority.** `RGT-S009` documented that the dominant cutout tool's library templates are copies rather than links — "Dragging a template into your scene copies the content in your Timeline and does not link it to the original" — so fixing a rig in the library does not propagate to shots already built, and reusable action templates break when layer order or connections change. `RGT-S001` found the same limitation independently in two open-source systems: OpenToonz embeds the skeleton in the scene with copy-import as the only reuse path, and Synfig's bone identifiers are XORed with the runtime root-canvas identifier so they cannot resolve across files at all.

**Automating shot production amplifies this failure mode**, because it increases the number of shots a later rig change invalidates. Version pinning per shot and a dependency graph that identifies exactly what a rig change invalidates are therefore not optional conveniences; they are the requirement that prevents RigTale from making a documented industry problem worse. See `docs/research/small-studio-workflow.md` section 5.

### PR-O04 — Deliver publication-ready output (`charter-backed`)

The complete workflow must produce reviewable animatics and shot previews plus final video, audio, captions, manifests, and quality reports. Delivery must pass deterministic validation, independent Red-Team review, and the approved human quality rubric.

## 4. Production Entry and Gates

### PR-F001 — Flexible production entry (`charter-backed`)

The system must accept a creative prompt or brief as the earliest input. A user may additionally provide an approved script, lyrics, timing data, locked audio, or an existing structured production. Supplied artifacts skip authoring work but not validation or versioning.

### PR-F002 — Structured artifact progression (`hypothesis`)

The product should preserve explicit artifacts and approval gates for creative intent, script or lyrics, audio when applicable, scene plan, storyboard or animatic, published assets, compiled shots, review output, and delivery output. `SPIKE-W001` determines which gates are mandatory, optional, or impractical in real small-studio work.

**Evidence status after `RGT-S009` Part A: unchanged, and the gap is now measured.** Desk research found two gates documented in published cutout workflow material — storyboard locked before animatic, and animation approved before compositing — plus formal approval models in three production-tracking tools. **But every one of those sources describes a supervisor role distinct from the artist, and no primary source or first-hand account was found documenting the gate model of a two-to-five-person team.** The best-documented published pipeline states it targets ten to twenty people.

This requirement therefore stays `hypothesis` and cannot be promoted by desk research. It is the largest single evidence gap in the spike and it sits directly on a core design decision: where the human approves. See `docs/research/small-studio-workflow.md` section 4. Resolution requires `RGT-S009B`.

### PR-F003 — Audio is conditional production data (`charter-backed`)

Audio, lyrics, beat, phoneme, viseme, and timing data must be accepted when required by the production. Locked audio constrains synchronized animation but is not the mandatory product entry point or the sole source of character direction.

## 5. Asset and Rig Requirements

### PR-A001 — Versioned published asset packs (`charter-backed`)

Characters, scenes, props, motions, audio timelines, shot plans, and episodes must use typed, versioned production contracts with provenance, license, dependency, and compatibility metadata.

### PR-A002 — Fixed-cast capability declaration (`charter-backed`)

Each published character or asset must declare the actions, expressions, attachments, interactions, deformations, and render features it supports. Unsupported instructions must fail explicitly before final rendering.

### PR-A003 — Layered artwork ingestion (`charter-backed`)

The system must import at least one documented layered-artwork format and preserve the structure required for rigging, masks, draw order, deformation, expression changes, and animation. The source format, authoring workflow, preparation effort, and rig-publication model are `decision-pending` under `SPIKE-A002`; orchestration and backend compatibility follow under `SPIKE-A001` and `SPIKE-R001`.

**New constraint from `RGT-S001`, added to the decision inputs.** Screening established that **a permissively licensed runtime does not imply an open authoring path**, and that the second property is what determines fit. Rive has no file writer anywhere in its repository and its editor is a paid service; Spine requires every downstream user to hold a paid editor licence; Live2D's core is a closed binary absent from its repository; Lottie's default authoring path is a proprietary host application.

Any format selected under `SPIKE-A002` must satisfy: **a program can produce valid content without a graphical interface and without a proprietary tool.** This is now an explicit screening criterion, not an assumption. See `docs/research/landscape.md`.

### PR-A004 — Archetype support (`charter-backed`)

The reference asset library and production path must support biped, quadruped, vehicle, prop, and reusable environment archetypes without episode-specific engine changes.

## 6. Character Orchestration Requirements

### PR-C001 — Multi-instance direction (`charter-backed`)

A shot must address multiple independent character instances, including identity, role, placement, timing, action, reaction, gaze, expression, prop use, and camera relationship.

### PR-C002 — Reusable choreography (`charter-backed`)

The system must express reusable solo motions, synchronized group choreography, and a bounded set of role-based interactions. Repeated musical or educational structures must be reusable without copying opaque low-level animation data.

### PR-C003 — Capability-aware planning (`charter-backed`)

The Studio Agent and deterministic validators must reject, repair, or report any requested action that cannot be satisfied by the selected assets. The system must never silently substitute a visibly incorrect action.

### PR-C004 — Orchestration abstraction (`hypothesis`)

Agent output should remain above per-bone and per-frame control, while deterministic software resolves concrete motion, transforms, constraints, compositing, and frame state. The correct abstraction boundary, motion composition model, interaction representation, and error behavior must be established by `SPIKE-A001`.

### PR-C005 — Interaction correctness (`decision-pending`)

Multi-character and character-prop interactions must preserve role assignment, timing, spatial compatibility, and visible contact. Required anchor, constraint, inverse-kinematics, authored-pair-motion, or procedural techniques must be selected from evidence gathered by `SPIKE-A001`.

## 7. Animation and Rendering Requirements

### PR-R001 — Deterministic production path (`charter-backed`)

Given the same versioned production data, assets, engine configuration, and random seeds, the system must reproduce the same choreography, timing, scene state, and delivery structure without calling an AI provider.

### PR-R002 — Structured 2D feature set (`charter-backed`)

The production path must support hierarchical transforms, reusable motion clips, sprite or expression swapping, masks, explicit layer ordering, parallax, camera movement, and basic mesh or bone deformation.

### PR-R003 — Preview and final consistency (`hypothesis`)

Preview and final rendering should consume the same authoritative production state so that timing, composition, interactions, and shot boundaries do not drift. Permitted raster differences and the required parity threshold must be measured by `SPIKE-A001`, `SPIKE-R001`, and the preview-parity spike.

### PR-R004 — Frame and shot addressability (`charter-backed`)

The engine must render deterministic frames or time ranges, resume interrupted work, and rerender an isolated shot without rebuilding unaffected shots. Cache keys and invalidation behavior are evidence-pending under `SPIKE-F001`, `SPIKE-A001`, and `SPIKE-R001`.

### PR-R005 — Backend independence (`hypothesis`)

The core production contracts should not expose episode-specific renderer code. The viable adapter boundary and whether one runtime can serve preview and final output must be established through `SPIKE-A001` and `SPIKE-R001`.

**Evidence strengthens the case for this hypothesis rather than weakening it.** `RGT-S001` found **no candidate that supplies both a reusable character rig system and a deterministic frame-addressable renderer.** The systems with the strongest rig models — OpenToonz, Blender Grease Pencil, DragonBones — differ from the systems with the strongest determinism evidence — resvg and tiny-skia, rlottie, MLT. The one format with a published machine validator, Lottie, **cannot express a bone hierarchy at all**: no bone, joint, skin, weight, inverse-kinematics, or deformer concept exists in its schema.

**Working hypothesis, not a decision:** RigTale should expect to own its rig representation and compile it down to whatever renderer is selected, rather than obtaining a rig by choosing a renderer. This must be tested by `SPIKE-A001` and `SPIKE-R001` and settled by `RGT-D010`, not here.

### PR-R006 — Production workload (`decision-pending`)

Quality, latency, throughput, memory, storage, cache, and recovery targets must be measured through `SPIKE-F001`, `SPIKE-R001`, and `SPIKE-I001` on the representative full-length production and supported hardware. A successful short clip is insufficient evidence.

## 8. Review, Correction, and Quality

### PR-Q001 — Deterministic validation (`charter-backed`)

The system must detect schema, dependency, missing-asset, unsupported-action, timing, duration, render, provenance, and licensing failures before delivery.

### PR-Q002 — Visible-quality validation (`charter-backed`)

Review must cover framing, occlusion, layer order, continuity, synchronization, repetition, pacing, educational clarity, audience safety, and mismatch with the production brief.

### PR-Q003 — Independent Red-Team review (`charter-backed`)

The Red-Team Agent must review structured plans and rendered output independently, return structured findings, and require the Studio Agent to revise blocking issues before delivery.

### PR-Q004 — Structured correction (`charter-backed`)

A user or agent must be able to correct a shot, action, timing, placement, expression, interaction, or camera instruction as structured data and observe the minimum necessary rerender scope.

## 9. Product Surfaces and Operation

### PR-P001 — Local studio surface (`charter-backed`)

The product must provide a usable local studio application for project creation, asset inspection, production review, structured correction, validation, and render control on a supported macOS workstation.

### PR-P002 — Automation surface (`charter-backed`)

The product must expose CLI and API operation for repeatable tests, headless rendering, CI, and integration into another product. MCP, embedded provider, and future cloud surfaces must use the same production contracts rather than separate workflows.

### PR-P003 — Provider neutrality (`charter-backed`)

Language, speech, music, alignment, and future generative capabilities must use replaceable provider interfaces. An approved production must remain editable and renderable without provider access.

### PR-P004 — Recoverable operation (`charter-backed`)

Installation, production execution, interruption recovery, migration, backup, troubleshooting, and upgrades must be documented and reproducible on a clean supported machine.

## 10. Reference-Production Acceptance

The reference production must:

- run for 150–210 seconds and contain multiple shots;
- show at least three simultaneous character instances;
- exercise biped, quadruped, vehicle, reusable backgrounds, props, expressions, masks, layer ordering, parallax, camera movement, and basic deformation;
- exercise solo action, group choreography, and role-based interaction;
- accept synchronized audio and timing data where required;
- require no manual per-frame drawing or keyframing after asset publication;
- support a structured single-shot correction and isolated rerender;
- produce animatic, preview, final video, captions, manifests, and quality reports;
- have zero blocking deterministic-validation errors; and
- pass Red-Team review and the approved human rubric.

Quantitative visual-quality, performance, parity, recovery, and interaction thresholds remain evidence-pending and must be added after the related spikes.

## 11. Evidence and Revision Plan

| Requirement area | Evidence owner |
|---|---|
| Small-studio workflow, artifact gates, user problems, and manual baseline | `SPIKE-W001` |
| Comparable production and open-source patterns | `SPIKE-C001` and fixture-based repository reviews |
| Reference workload, quality assertions, recovery cases, and rubric-calibration plan | `SPIKE-F001` |
| Schema tooling, serialization, exact time, content identity, migration, local storage, and archive restoration | `SPIKE-CS001` |
| Layered-asset ingestion, rig preparation, authoring effort, and publication | `SPIKE-A002` |
| Orchestration contracts, motion composition, choreography, interaction, and invalidation hypotheses | `SPIKE-A001` |
| Visible orchestration quality, renderer quality, deterministic execution, cache behavior, recovery, packaging, and headless execution | `SPIKE-R001` |
| Preview and final-render parity | `SPIKE-R002` |
| Swift and renderer integration | `SPIKE-I001` |
| MCP host-operated and embedded-agent execution | `SPIKE-M001` |
| Hands-on user evaluation against the approved manual baseline | Implementation Phase 14 |

Every completed research or spike item must identify affected requirement IDs and update this document. Accepted architecture choices belong in decision records; this document records what the product must achieve, not which library is fashionable or convenient.

## 12. Requirement Traceability

| Requirement | Primary contracts or design | Pipeline or quality gate | Implementation phase | Evidence owner |
|---|---|---|---|---|
| `PR-O01` | `CreativeBrief`, `Episode`, `ShotPlan`, asset packs | Intent, asset, shot-plan gates | 8, 9, 11 | `W001`, `A001`, `R001` |
| `PR-O02` | `MotionPack`, `CapabilityManifest`, `CompiledShot` | Asset, compilation, preview gates | 8, 9, 14 | `A002`, `A001`, `R001` |
| `PR-O03` | `Production`, `AssetLock`, `CompiledShot`, manifests | Dependency, correction, archive gates | 7, 9, 10 | `F001`, `CS001`, `A001`, `R001` |
| `PR-O04` | `ValidationReport`, `ReviewReport`, `DeliveryManifest` | Preview, final, delivery gates | 10, 13, 14 | `W001`, `F001`, `R001` |
| `PR-F001` | `CreativeBrief`, `Script`, `Episode` | Intent and creative approval | 11, 12 | `W001` |
| `PR-F002` | All authoring artifacts and lifecycle states | All artifact handoff gates | 1, 11, 12 | `W001` |
| `PR-F003` | `AudioTimeline`, `ShotPlan` | Media lock when applicable | 10, 11 | `W001`, provider evidence during Phase 11 |
| `PR-A001` | Asset packs, `AssetLock`, common envelope | Asset publication | 7, 8 | `A002`, `CS001` |
| `PR-A002` | `CapabilityManifest`, `MotionPack` | Capability and compile validation | 8, 9 | `A002`, `A001` |
| `PR-A003` | `CharacterPack`, `ScenePack`, `PropPack` | Asset ingestion and publication | 8 | `A002` |
| `PR-A004` | All asset-pack archetypes | Asset and fixture approval | 8 | `F001`, `A002` |
| `PR-C001` | `ShotPlan`, character instances | Shot-plan and compilation gates | 9, 11 | `A001`, `R001` |
| `PR-C002` | `MotionPack`, choreography in `ShotPlan` | Compilation and preview gates | 9 | `A001`, `R001` |
| `PR-C003` | `CapabilityManifest`, structured errors | Capability validation | 8, 9, 11 | `A001`, `R001` |
| `PR-C004` | `ShotPlan`, `CompiledShot` | Compilation | 9 | `A001`, `R001` |
| `PR-C005` | Interaction instructions and compiled tracks | Compilation and visible preview | 9, 13 | `A001`, `R001` |
| `PR-R001` | `CompiledShot`, `RenderJob`, `RenderManifest` | Compilation and final render | 9, 10 | `R001` |
| `PR-R002` | Asset packs and compiled tracks | Asset, compilation, final render | 8, 9, 10 | `A002`, `R001` |
| `PR-R003` | `CompiledShot`, renderer capabilities | Preview and final parity | 4, 10 | `R002` |
| `PR-R004` | `RenderJob`, dependency digests, manifests | Render, correction, recovery | 9, 10 | `F001`, `R001`, `I001` |
| `PR-R005` | `CompiledShot`, renderer adapter contract | Compilation and renderer qualification | 9, 10 | `A001`, `R001` |
| `PR-R006` | `RenderJob`, `RenderManifest` measurements | Full-production qualification | 4, 10, 13 | `R001`, `I001` |
| `PR-Q001` | `ValidationReport`, structured errors | Deterministic gates 1–7 | 7–13 | `F001` and each technical spike |
| `PR-Q002` | `ValidationReport`, `ReviewReport` | Preview and final visible review | 13, 14 | `W001`, `F001`, `R001` |
| `PR-Q003` | `ReviewReport`, approval state | Red-Team and delivery gates | 11, 13, 14 | agent evaluation in Phase 11 |
| `PR-Q004` | Source maps, dependency graph, new artifact versions | Correction and isolated rerender | 9, 10, 12 | `F001`, `A001`, `R001` |
| `PR-P001` | Application operations, jobs, artifact repository | Local operational qualification | 12, 13 | `I001` |
| `PR-P002` | Application API, CLI operations, MCP adapter | Automation and integration qualification | 11, 12, 15 | `I001`, `M001` |
| `PR-P003` | Provider adapters, provenance, run records | Agent and offline-render gates | 11 | `M001`, provider evaluation in Phase 11 |
| `PR-P004` | Jobs, manifests, migrations, archives | Recovery and operational qualification | 10, 13 | `F001`, `CS001`, `R001`, `I001` |

The matrix is updated whenever an artifact, phase, evidence owner, or accepted decision changes. A requirement with no contract, gate, phase, or evidence owner blocks baseline validation.

`RGT-D009` reconciles the core and local subset after its technical evidence. MCP and embedded-agent requirements remain explicitly evidence-pending until `RGT-D011` and are reconciled by `RGT-D014`. Full business validation still requires the Phase 14 hands-on evaluations.

## 13. Baseline Review Criteria

This v1 draft is ready to authorize evidence work when:

- every charter objective and release-scope item maps to at least one requirement;
- every technical assumption is labeled and linked to evidence work;
- the reference production has a traceable acceptance requirement;
- contradictions with the charter and other documentation are removed; and
- the Project Owner confirms that the complete v1 documentation set captures the intended product and evidence sequence.

Downstream architecture drafts may already exist during baseline review. They remain provisional and must be revised when research changes an upstream requirement.
