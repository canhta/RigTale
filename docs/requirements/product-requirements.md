# RigTale Product Requirements

**Status:** Draft; evidence-pending.

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

### PR-O04 — Deliver publication-ready output (`charter-backed`)

The complete workflow must produce reviewable animatics and shot previews plus final video, audio, captions, manifests, and quality reports. Delivery must pass deterministic validation, independent Red-Team review, and the approved human quality rubric.

## 4. Production Entry and Gates

### PR-F001 — Flexible production entry (`charter-backed`)

The system must accept a creative prompt or brief as the earliest input. A user may additionally provide an approved script, lyrics, timing data, locked audio, or an existing structured production. Supplied artifacts skip authoring work but not validation or versioning.

### PR-F002 — Structured artifact progression (`hypothesis`)

The product should preserve explicit artifacts and approval gates for creative intent, script or lyrics, audio when applicable, scene plan, storyboard or animatic, published assets, compiled shots, review output, and delivery output. Exact gate names and which gates are mandatory require workflow research.

### PR-F003 — Audio is conditional production data (`charter-backed`)

Audio, lyrics, beat, phoneme, viseme, and timing data must be accepted when required by the production. Locked audio constrains synchronized animation but is not the mandatory product entry point or the sole source of character direction.

## 5. Asset and Rig Requirements

### PR-A001 — Versioned published asset packs (`charter-backed`)

Characters, scenes, props, motions, audio timelines, shot plans, and episodes must use typed, versioned production contracts with provenance, license, dependency, and compatibility metadata.

### PR-A002 — Fixed-cast capability declaration (`charter-backed`)

Each published character or asset must declare the actions, expressions, attachments, interactions, deformations, and render features it supports. Unsupported instructions must fail explicitly before final rendering.

### PR-A003 — Layered artwork ingestion (`charter-backed`)

The system must import at least one documented layered-artwork format and preserve the structure required for rigging, masks, draw order, deformation, expression changes, and animation. The precise import format and rig representation are `decision-pending` under `SPIKE-A001` and `SPIKE-R001`.

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

The engine must render deterministic frames or time ranges, resume interrupted work, and rerender an isolated shot without rebuilding unaffected shots. Cache keys and invalidation behavior are `decision-pending`.

### PR-R005 — Backend independence (`hypothesis`)

The core production contracts should not expose episode-specific renderer code. The viable adapter boundary and whether one runtime can serve preview and final output must be established through `SPIKE-A001` and `SPIKE-R001`.

### PR-R006 — Production workload (`decision-pending`)

Quality, latency, throughput, memory, storage, and recovery targets must be measured on the representative full-length production and supported hardware. A successful short clip is insufficient evidence.

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
| Comparable production and open-source patterns | `SPIKE-C001` and repository-specific reviews |
| Rig, motion composition, choreography, interaction, and frame compilation | `SPIKE-A001` |
| Renderer quality, packaging, headless execution, and backend boundary | `SPIKE-R001` |
| Preview and final-render parity | `RGT-S005` |
| Swift and engine integration | `RGT-S006` |
| MCP subscription-hosted operation | `RGT-S007` |

Every completed research or spike item must identify affected requirement IDs and update this document. Accepted architecture choices belong in decision records; this document records what the product must achieve, not which library is fashionable or convenient.

## 12. Draft Exit Criteria

This draft may advance to `evidence-pending` when:

- every charter objective and release-scope item maps to at least one requirement;
- every technical assumption is labeled and linked to evidence work;
- the reference production has a traceable acceptance requirement;
- contradictions with the charter and other documentation are removed; and
- the Project Owner approves the requirement structure before downstream contract drafts are written.
