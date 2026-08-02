# Repository Review: OpenMontage

**Screened under:** `SPIKE-C001` (`RGT-S001`), read-only static source inspection.

**Repository:** https://github.com/calesthio/OpenMontage

**Inspected commit:** `c36e41223e819441748817105635ac4036d41b10` (2026-07-24). The clone is shallow at depth 1; maintenance health is not derivable from it.

**License:** **GNU AGPL v3** (`LICENSE` line 1, confirmed at `README.md:755`). This is decisive for reuse: AGPL-3.0 is viral for a networked service, so RigTale cannot copy code from this repository without adopting AGPL itself.

**Disposition:** `reference` — extract designs, reimplement, do not copy code.

## Why This Is the Closest Prior Art Found

`pipeline_defs/character-animation.yaml:3-8` states RigTale's own thesis: deterministic local motion, explicitly not a remote video-generation replacement. Its artifact vocabulary is close to a superset of what RigTale's contracts need.

Twenty JSON Schema artifacts are registered in `schemas/artifacts/__init__.py` with `validate_artifact` backed by `jsonschema`. The directly relevant ones:

| Schema | Content |
|---|---|
| `rig_plan.schema.json` | parts, joints with 2-D pivots, layers, views, required poses, risks |
| `action_timeline.schema.json` | fps, scenes with start/end seconds, per-action `at_seconds`, `character_id`, `pose`, `emotion`, `easing` |
| `pose_library.schema.json` | reusable pose definitions |
| `character_design.schema.json`, `scene_plan.schema.json`, `asset_manifest.schema.json` | design, plan, and asset records |
| `character_qa_report.schema.json`, `review.schema.json`, `final_review.schema.json` | structured findings |

All use `additionalProperties: false` and `version: const "1.0"`. Pipeline and checkpoint manifests are themselves schema-validated (`schemas/pipelines/pipeline_manifest.schema.json`, `schemas/checkpoints/checkpoint.schema.json`).

**Gaps against RigTale:** `rig_plan` and `action_timeline` carry no layer z-order, no camera, and no interaction or contact constraints. Those are RigTale requirements (`PR-C005`, `PR-R002`) and would have to be added.

## Orchestration and Gates

Stages are declarative. `pipeline_defs/character-animation.yaml` defines ten stages, each with `skill`, `produces`, `required_artifacts_in`, `tools_available`, `checkpoint_required`, `human_approval_default`, `review_focus`, and `success_criteria`, plus a `sub_stages.sample` requiring a 10–15 second proof before full production. Loading and validation live in `lib/pipeline_loader.py`; stage directors are Markdown under `skills/pipelines/character-animation/`.

**Gate enforcement is real and fail-closed.** `lib/checkpoint.py:388-405` raises `GATE VIOLATION` if a manifest-gated stage is written `completed` without `human_approved=True`, and an unknown pipeline type fails closed rather than skipping gates (`:246-252`). Checkpoint writes are atomic via temp file plus `os.replace` (`:458-465`), and superseded checkpoints are archived to `history/`.

Bounds are declared: `budget_default_usd: 2.00`, `max_revisions_per_stage: 3`, `max_send_backs: 3`, `max_wall_time_minutes: 20` (`pipeline_defs/character-animation.yaml:48-51`), with estimate/reserve/reconcile cost governance and `BudgetExceededError` / `ApprovalRequiredError` in `tools/cost_tracker.py`.

## Deterministic Validators Worth Copying in Design

- `lib/slideshow_risk.py` — a six-dimension score with an explicit threshold ("≥ 4.0: fail — should not proceed to compose"). It detects the failure mode where an animation degrades into a slideshow.
- `lib/delivery_promise.py` — a motion-led promise locked at proposal time; the compose stage must stop rather than silently downgrade.
- `lib/variation_checker.py`, `lib/verify_scene_pacing.py`.
- `CharacterAnimationReviewer` (`tools/character/character_animation.py:816-895`) emits a schema-valid `character_qa_report` with pass/revise and a `recommended_action`.

The locked delivery promise is the single most valuable idea here for RigTale: it is exactly the anti-silent-degradation rule the charter demands.

## Blocking Weaknesses

1. **The character renderer is a stub, not a compositor.** `CharacterRigRenderer.execute` (`tools/character/character_animation.py:519-607`) emits a hardcoded generic figure — `<ellipse class="body">`, `<circle class="head">` — with fixed bounce, blink, and arm GSAP timelines. It uses `action_timeline` only for scene count and total duration (`:608-614`) and **ignores `rig_plan` parts and asset paths entirely** (`:524-535` extracts only `character_id`). There is no layered cutout compositing, no per-action pose application, and no camera.

   The schemas describe a system that the renderer does not implement. Any conclusion drawn from the schema vocabulary alone would be a conclusion drawn from a feature checklist.

2. **"Independent review" is self-review.** `skills/meta/reviewer.md` explicitly states it "replaces the Python reviewer class with an instruction-driven self-review protocol" — the same agent reviews its own output — and caps at two rounds before emitting `PASS_WITH_WARNINGS`. RigTale's `PR-Q003` requires a genuinely independent Red-Team Agent; this pattern defeats that gate.

3. **No downstream invalidation.** A search across `lib/`, `tools/`, `schemas/`, and `backlot/` for invalidation, staleness, downstream, or rerender terms returns only unrelated hits. Re-running a stage overwrites its checkpoint and archives the old one; downstream checkpoints remain `completed`.

4. **CDN script tags in render artifacts** (`tools/character/character_animation.py:564,657` load GSAP from `cdn.jsdelivr.net`), contradicting `ink-theater/README.md`'s own no-network determinism rule.

5. **The "no Python orchestrator" design.** `docs/ARCHITECTURE.md` states the coding assistant is the control plane and Python supplies tools and persistence only. This makes every guarantee prompt-dependent and unbounded — the opposite of RigTale's deterministic-coordination constraint.

6. **Documented but empty**: `lib/providers/` is empty despite being named in `docs/ARCHITECTURE.md`. Real abstraction is the selector pattern (`tools/video/video_selector.py`, `tools/graphics/image_selector.py`, `tools/audio/tts_selector.py`) plus `BaseTool.fallback_tools`.

7. **Maintenance surface**: roughly 2,000 files, of which about 1,000 are duplicated skill Markdown across `.agents/skills/` and `.claude/skills/`. Unmaintainable at solo scale.

## The Ink Theater Determinism Contract

`ink-theater/README.md` documents a deterministic, seek-safe 2D engine: closed-form springs, seeded PRNG, no infinite repeats, locally embedded fonts, and no render-time network fetch. `ink-theater/THIRD_PARTY_NOTICES.md` documents bundled Patrick Hand under SIL OFL with the licence shipped at `ink-theater/assets/OFL.txt`, and CMU Motion Capture Database clips with per-clip trial IDs in `ink-theater/mocap/catalog.json`.

This checklist is directly adoptable as a hard render-invariant list. Note the contradiction: the character renderer violates the no-network rule that the engine's own documentation states.

## Provenance Model

`schemas/artifacts/asset_manifest.schema.json` requires `id`, `type`, `path`, `source_tool`, and `scene_id`, with optional `prompt`, `seed`, `model`, `provider`, `license`, `original_url`, and `cost_usd`. `schemas/artifacts/source_media_review.schema.json` covers user-supplied media. This is a workable starting shape for RigTale's provenance requirement (`PR-A001`).

## Test and Output Evidence

Roughly 90 test files across `tests/contracts/`, `tests/backlot/`, `tests/lib/`, `tests/qa/`, and `tests/tools/`, plus an evaluation layer: `tests/eval/bench_runner.py` runs a synthetic scenario matrix asserting slideshow-risk, variation, and delivery-promise verdicts, and `tests/eval/replay_harness/harness.py` provides golden scenario replay with deterministic and stochastic modes. CI runs lint and tests on Ubuntu with FFmpeg.

**Output-quality evidence is thin.** One produced example is committed (`assets/signal-from-tomorrow-demo.mp4`, 20.9 MB) plus board screenshots. The sole golden scenario (`tests/eval/golden_scenarios/talking_head_basic.json`) has a hardcoded Windows path for its input footage and is therefore not reproducible. `tests/eval/golden_outputs/` and `fixtures/` contain only `.gitkeep`. Quality enforcement is heuristic, not measured against ground truth.

There is no rendered multi-character cutout output anywhere in the repository.

## Patterns to Adopt or Adapt

1. **Manifest-declared stage contracts** — `produces`, `required_artifacts_in`, `success_criteria`, `review_focus`, `human_approval_default` per stage, machine-validated. This makes gates data rather than code and gives the Red-Team Agent a declarative target.
2. **Fail-closed gate enforcement at the persistence boundary** — refuse to write `completed` without recorded approval; unknown pipeline type raises rather than skipping.
3. **Atomic checkpoint write plus `history/` archival.**
4. **`rig_plan` / `pose_library` / `action_timeline` schema shapes** as a starting vocabulary, extended with layer z-order, camera, and interaction constraints.
5. **A locked delivery promise** — encode "multi-character cutout animation, not stills" as a promise the render stage must honour or halt.
6. **Structured findings with severity, disposition, and a required proposed fix**, mapping onto RigTale's Red-Team output.
7. **A sample-first sub-stage** — a short gated proof before full-length production.
8. **Estimate/reserve/reconcile cost governance** with typed budget and approval exceptions.
9. **The Ink Theater determinism checklist** as a hard render-invariant list.

## Patterns to Avoid

- **Copying any code**: AGPL-3.0 would propagate to RigTale.
- The agent-as-only-orchestrator design.
- Self-review presented as independent review, and a "two rounds then pass with warnings" escape hatch.
- Duplicating a thousand Markdown skill files across two directories.
- CDN script tags inside render artifacts.
- Publishing rich schemas that the renderer does not implement.

## Questions Requiring Executable Evidence

| Question | Route |
|---|---|
| Can Playwright frame capture plus FFmpeg sustain deterministic capture over a 150–210 second multi-character production on macOS, and at what wall-clock cost? | `SPIKE-R001` |
| Do CMU mocap clips retarget acceptably to layered cutout rigs rather than stick figures? `ink-puppet.js` builds only a stick figure. | `SPIKE-A001` |
| Is a paused GSAP timeline plus `seek(t)` frame-exact under headless capture? Asserted in documentation, verified by no test. | `SPIKE-R002` |
| Does JSON Schema validation of a 200-second `action_timeline` stay fast enough to run on every write, and how large does the artifact become? | `SPIKE-CS001` |

## Conclusion

`reference`, with code reuse blocked by AGPL-3.0.

OpenMontage's artifact schemas, fail-closed gate enforcement, checkpoint semantics, locked delivery promise, and determinism checklist are the closest prior art to RigTale found in this screening round. But its actual renderer is a hardcoded stub that ignores the rig plan, its independent review is self-review, it has no downstream invalidation, and it has produced no multi-character cutout output.

The correct use is to extract designs and reimplement them cleanly. No conclusion in this review rests on the schema vocabulary alone: the renderer gap is the reason the schemas cannot be treated as demonstrated capability.
