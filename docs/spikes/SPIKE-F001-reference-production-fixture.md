# SPIKE-F001: Representative Multi-Character Production Fixture

**Tracker:** `RGT-S003`

**Status:** Active. Unblocked on 2026-08-03 by the Project Owner's sandbox-asset decision, which closed `RGT-O001`.

## Question

What versioned, legally redistributable fixture set can evaluate RigTale's character orchestration, rendering, quality, recovery, editability, and full-production behavior without favoring one engine or rig representation?

## Why This Requires a Spike

A convenient demo scene can make weak architectures look successful. The test fixture must expose multi-character continuity, motion conflicts, role-based interaction, draw-order changes, repetition, cache invalidation, and operational recovery. It must also provide objective expected results without copying a protected cast or visual identity.

## Preconditions

- The v1 charter and documentation baseline are approved for evidence work.
- `SPIKE-C001` has identified relevant production patterns and common failure modes.
- `SPIKE-W001` has established target-user workflow, gate, and value evidence. **Part B was rejected**, so gate and value evidence rest on desk research and owner judgement; see `docs/requirements/charter.md`, Charter Revision 1.
- Reference assets may be created, commissioned, or adapted only from sources with compatible, documented licenses.

## Two Asset Tiers

Owner decision, 2026-08-03. This is what closed `RGT-O001` and it governs every asset this spike touches.

| Tier | May be used for | May never be used for |
|---|---|---|
| **Sandbox** — downloaded from the Internet under its own licence or terms, held in the ignored `.sandbox/` workspace | Local technical experiments: does a renderer composite headlessly, does an importer preserve layer structure, does a rig deform | Fixtures, approval evidence, decision records, the reference production, anything committed, packaged, published, or released |
| **Reference-read-only** — a subset of sandbox whose terms are narrower still, such as Adobe sample puppets and the Spine runtimes | Reading a format or a rig structure | Integration, redistribution, or supplying any shipped artwork |
| **Official** — provable redistribution rights, provenance and licence recorded before use | Everything, including all of the above | — |

**Any result that becomes official evidence must be reproduced on official assets.** A sandbox run may tell you a candidate works; it may not be the record that says so. Full policy: `.sandbox/README.md`.

**`.gitignore` changes what Git tracks and nothing else.** Attribution, share-alike, non-commercial, and no-derivatives terms bind regardless of whether a file is ignored.

## Fixture Structure

The fixture suite must contain three layers.

### Contract fixtures

Small valid and invalid artifacts covering schema versions, dependencies, capabilities, licenses, time boundaries, migrations, stale references, and structured errors.

### Diagnostic shots

Short shots that isolate one difficult behavior at a time:

- hierarchical biped motion and deformation;
- quadruped locomotion and ground contact;
- vehicle motion, wheel or component cycles, and character attachment;
- concurrent locomotion, upper-body action, expression, gaze, viseme, and prop tracks;
- three-character synchronized choreography;
- a role-based two-character interaction with a visible contact frame;
- character-prop handoff or attachment;
- masks, occlusion, draw-order changes, foreground and background layers;
- camera movement, parallax, safe-area boundaries, and aspect-ratio framing;
- unsupported action, motion conflict, missing asset, and incompatible-version failures;
- exact frame addressing, interrupted execution, and isolated rerendering.

### Complete reference production

A 150–210 second, multi-shot 2D cutout production exercising:

- at least three simultaneous character instances;
- reusable biped, quadruped, vehicle, prop, and environment packs;
- repeated sections with controlled variation;
- solo action, group choreography, interaction, reaction, expression, and camera changes;
- synchronized media and timing where the selected story requires them;
- continuity across shot boundaries;
- one structured correction that should invalidate only a known subset of output; and
- final assembly, captions, manifests, QC, export, restore, and rerender.

The subject, script, and visual design must be original or safely licensed. Similar production constraints may be studied, but the fixture must not imitate protected characters, music, artwork, or branding.

## Cast Construction

Owner direction, 2026-08-03. The target look is preschool cutout. **The cast is built from CC0 geometric parts, not copied from any reference channel.**

1. Assemble bodies, eyes, mouths, hands, and expressions from **Kenney Shape Characters** (CC0, 212 separated PNG parts).
2. Overlay felt or paper texture from **ambientCG Fabric034 or Paper001** (CC0), blended lightly.
3. Compose original characters by choosing colour, hair, clothing, and face. Silhouettes are circle, squircle, or cloud-like; eyes are two large circles with black pupil and white highlight; limbs are separate layers with pivots at shoulder and hip; mouths are separate states for neutral, smile, open, and each phoneme; clothing uses new patterns; shadows are a very soft small blur to read as cut paper.
4. Study Adobe Character Animator sample puppets for **layer and rig structure only**. No artwork from them reaches the fixture.

**Kenney plus ambientCG is the only combination eligible for official assets**, because both are CC0. It is also far lighter than the Adobe puppets.

**No visual identity may be copied** — not shape, colour, hair, costume, or naming. The reference channel is studied for art direction and never used as an asset source; see the YouTube rule in `.sandbox/README.md`.

## Fixture-Neutrality Rules

- Expected behavior is described in production semantics and visible assertions before engine adapters are written.
- Source assets retain an engine-neutral master where practical.
- Backend-specific conversion is generated and versioned as derived evidence.
- The fixture cannot require a feature merely because one preferred engine exposes it.
- A candidate may document an unsupported assertion; the fixture must not be weakened to make every candidate pass.
- Short diagnostic output cannot replace complete-duration evidence.

## Expected Evidence

Each case must provide the applicable subset of:

- source artifacts and exact licenses;
- intended semantic action and required capability;
- approved reference pose, composition, contact frame, or sequence;
- frame and time ranges;
- measurable tolerances where evidence exists;
- expected success or structured failure;
- dependency and invalidation expectations;
- render and environment profile; and
- review rubric and approval record.

Thresholds that cannot be justified before execution remain explicitly evidence-pending and are calibrated without rewriting the intended visible behavior.

## Method

1. Derive a risk catalogue from the charter, v1 requirements, quality system, competitive research, and repository reviews. **Done — `docs/quality/fixture-risk-matrix.md`, 54 risks.**
2. Map each material risk to at least one isolated fixture assertion. **Done in the same document. Three residual risks are unassertable after their assertable parts were split out, two entries are fixture-construction rules audited by reading rather than by execution and are never counted as coverage, and every requirement is either covered or excluded with a reason.**
3. Design an original production brief and cast sufficient to exercise the required archetypes. **Cast done — `fixtures/`, 132 part files holding 78 unique images, covering biped ×3, quadruped, vehicle, prop and environment, with joints and a rig tree. Brief outstanding.**
4. Record provenance and license compatibility before asset work begins, and decide per asset whether it is originated, commissioned, or adapted from a compatibly licensed source. `RGT-O001` fixed the constraint — official assets must be redistributable — and left the route per asset to this step. **Done for the cast — `fixtures/PROVENANCE.json`, tracked, both sources CC0 and adapted. The generator refuses to build unless every archive matches the recorded SHA-256 and byte size, so the record cannot decay unnoticed.**
5. Produce engine-neutral source assets, expected references, semantic descriptions, and invalid cases.
6. Review the fixture for accidental backend bias and missing full-duration risks.
7. Version and publish the fixture manifest before orchestration or renderer experiments.
8. Amend the fixture only through a reviewed version with an explanation of affected results.

## Required Outputs

- Fixture risk-to-requirement matrix.
- Versioned contract and failure corpus.
- Versioned diagnostic-shot manifests and expected evidence.
- Versioned complete-production brief, source assets, timeline, and acceptance rubric.
- Asset provenance, license, attribution, and redistribution report.
- Fixture authoring and execution instructions.
- Quality, recovery, cache-invalidation, and human-rubric calibration plan.
- A decision record approving the fixture version used for comparative spikes.
- Updates to product requirements, quality rules, and downstream spike preconditions.

## Exit Criteria

- Every charter reference-production constraint maps to fixture evidence.
- Every `SPIKE-A001` and `SPIKE-R001` material measurement has an input case.
- The fixture exposes multi-character, interaction, continuity, repetition, recovery, and isolated-rerender behavior.
- All redistributable artifacts have verified provenance and compatible licenses.
- Expected outcomes are defined before candidate adapter work.
- The Project Owner approves the fixture without selecting a renderer or orchestration architecture.

## Stop Conditions

- Stop if required assets lack provable redistribution rights. A sandbox asset does not satisfy this and never converts into one by being used; it must be replaced.
- Stop if any fixture manifest, expected-evidence record, or approval artifact references a path under `.sandbox/`.
- Stop if expected results can be satisfied only through one candidate's private representation.
- Stop and revise the fixture if a material production risk has no observable assertion.
