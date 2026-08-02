# Repository Review: ViMax

**Screened under:** `SPIKE-C001` (`RGT-S001`), read-only static source inspection.

**Repository:** https://github.com/HKUDS/ViMax

**Inspected commit:** `05a48943878312d88fe5a016c12a9654940ecc43` (2026-07-29). The clone is shallow at depth 1.

**License:** MIT (`LICENSE`, "Copyright (c) 2025", no named holder). Package name in `pyproject.toml` is `autolongvideogeneration`, version 1.2.0, requiring Python ≥ 3.12.

**Disposition:** `reject` for architecture; `reference` for two narrow mechanisms.

## Decisive Finding: The Pixel Path Is Irreducibly Generative

Final pixels come from image and video models, with no non-generative path.

| Evidence | Source |
|---|---|
| Per-shot video generation | `pipelines/script2video_pipeline.py:513` `await self.video_generator.generate_single_video(...)` |
| Keyframe image generation | `pipelines/script2video_pipeline.py:424,576` `image_generator.generate_single_image(...)` |
| Assembly is concatenation of model output | `pipelines/script2video_pipeline.py:314` moviepy `concatenate_videoclips` |
| Backend requires both generators in configuration | `tools/render_backend.py` |

This directly conflicts with the charter's product non-goal of replacing the structured animation renderer with black-box text-to-video generation, and with `PR-R001`'s requirement that an approved production render without calling an AI provider.

No amount of orchestration quality changes this. The architecture is rejected.

## Production Model

Three fixed DAG workflows — `idea2video`, `script2video`, `novel2video` (`prompts/workflow.md`). Python classes orchestrate (`pipelines/script2video_pipeline.py`), with an optional agent shell (`agent_runtime/loop.py`) wrapping them as three coarse tools.

## Data Contracts

Pydantic models, no JSON Schema files. `interfaces/` defines `ShotDescription` / `ShotBriefDescription` (`shot_description.py`), `Camera` (with `parent_cam_idx` and `missing_info`), `CharacterInScene`, `Scene`, `Event`, and `Frame`. Validation is `model_validate` at load (`pipelines/script2video_pipeline.py:600,627,749,797`). Persisted artifacts are plain JSON under the working directory.

`interfaces/camera.py` declares `parent_shot_idx` twice — a latent defect.

Because contracts are pydantic-only, cross-language and external tooling validation is unavailable. RigTale requires versioned, migratable, language-neutral contracts (`PR-A001`).

## The Two Mechanisms Worth Keeping as Reference

### 1. An explicit staleness table

`agent_runtime/vimax_adapters.py:787-798` `_stale_keys_for_revision()` is a real dependency-invalidation table: editing `storyboard.json` marks `shot_descriptions, camera_tree, frames, clips, final_video` stale; editing `shot_description.json` marks `frames, clips, final_video` stale. `_revise_narrative_artifact` (`:231-280`) rewrites one artifact, guards against path traversal, and logs before and after previews.

**Critical caveat:** `SessionIndex.mark_stale` only sets boolean flags (`agent_runtime/session_index.py:174-183`). It does not delete or quarantine downstream files, and the pipeline's skip-if-exists logic will still reuse them. Invalidation is advisory, not enforced.

For RigTale this is instructive in both directions: the table shape is right, and the failure mode — flags that do not prevent reuse — is exactly what `PR-Q004` must avoid.

### 2. Protocol-based provider neutrality

`tools/protocols.py` defines `runtime_checkable` `ImageGenerator` and `VideoGenerator` protocols, duck-typed with no inheritance requirement. `tools/render_backend.py` instantiates by `class_path` from YAML, and the chat model resolves through `langchain.init_chat_model` plus `utils/provider_presets.resolve_chat_model_config`. Eight concrete generators exist.

This is a lighter provider-neutrality mechanism than a large tool base class, and it maps onto `PR-P003`.

## Weaknesses

1. **No critic or review stage.** There is no review, QA, or red-team artifact in `interfaces/` or the pipelines. The only visual-inspection affordance is the agent's `view_image` tool, which is advisory and gates nothing. RigTale requires an independent blocking review (`PR-Q003`).
2. **Resume is file-existence checking only.** Every step is `if os.path.exists(path): skip` (`pipelines/script2video_pipeline.py:304,337,497,535,597,624,746,795`). A partially written file reads as done. There is no checkpoint schema and no run manifest beyond `render_status.json` and `render_events.jsonl`.
3. **No cost tracking anywhere.** Bounds are `MAX_TOOL_PASSES = 50` (`agent_runtime/loop.py:17`), environment-tunable step and request timeouts, a three-attempt download retry (`utils/retry.py`), and API rate limiters. The charter requires bounded cost (`Constraints`).
4. **No asset provenance or licensing.** No licence, attribution, or provenance field appears in any `interfaces/` model; generated media is written as bare PNG and MP4 with no manifest. This fails `PR-A001` outright.
5. **The agent surface is too coarse.** `agent_runtime/vimax_adapters.py:47,67,83` expose only `vimax_narrative_planning`, `vimax_novel_planning`, and `vimax_render_video`. The agent cannot address individual stages, so it cannot re-drive one stage.
6. **No CI workflow file exists.**

## Output-Quality Evidence: A Benchmark That Measures Nothing

`vimax_benchmark/` is a prompt dataset, not an evaluation harness. It contains 35 JSON story files plus `benchmark_index.json` declaring `total_stories: 35` and `model_config: {model: "", api: ""}` — unfilled. Each story file holds only `first_frame` and `video_prompt` strings per shot, typed A/B/C for a consistency scenario.

A repository-wide search for "benchmark" outside that directory returns zero hits: there is no runner, no metric, no scoring code, and no reference output. It is input material for an external evaluation, not evidence of output quality.

Any quality claim attached to this directory is unverified from source. Recorded here specifically because a directory named `benchmark` is the kind of signal that a feature-checklist screening would have accepted.

## Strengths

- The staleness table and the Protocol-based provider factory described above.
- Camera-tree modelling with parent/child relationships and an explicit `missing_info` field (`interfaces/camera.py`) is a thoughtful reuse mechanism.
- Operational hygiene in the agent layer: explicit hang guards, bounded tool passes, context compaction (`agent_runtime/context_compactor.py`), and API-key redaction in error text.
- A workflow-confirmation gate preventing the agent from guessing user intent (`prompts/workflow.md`).
- 24 test files totalling 3,272 lines, well targeted at the agent layer (`test_agent_loop.py`, `test_vimax_adapters.py` at 468 lines, `test_hang_guards.py`, `test_wrong_output_guards.py`, `test_robustness.py`).

## Patterns to Adopt or Adapt

- **An explicit staleness table keyed by edited artifact** — but enforcing, by deleting or quarantining derived artifacts rather than flagging them.
- **`runtime_checkable` Protocols plus config-driven `class_path` instantiation** for provider neutrality.
- **Hang guards, bounded tool passes, context compaction, and credential redaction** in the agent runtime.
- **A workflow-confirmation gate** before expensive work begins.

## Patterns to Avoid

- File-existence-as-checkpoint: a partially written file reads as complete.
- Staleness flags that do not prevent reuse of stale files.
- A coarse agent tool surface that prevents per-stage re-drive.
- Pydantic-only contracts with no language-neutral schema.
- Shipping a directory named `benchmark` that contains no runner, metric, or reference output.

## Questions Requiring Executable Evidence

Only one is worth carrying forward, and it is a design question rather than a candidate evaluation:

| Question | Route |
|---|---|
| Can staleness be enforced by deletion or quarantine while preserving expensive unaffected assets and invalidating only affected shots? | `SPIKE-A001`, `SPIKE-CS001` |

## Conclusion

`reject` for architecture. The pixel path is irreducibly generative, which is RigTale's stated non-goal; there is no critic stage, no cost bound, and no provenance; and the benchmark directory measures nothing.

`reference` for two narrow mechanisms: the staleness table shape (with its enforcement gap treated as a lesson) and the Protocol-plus-`class_path` provider factory.
