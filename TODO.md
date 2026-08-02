# RigTale Work Tracker

This file is the canonical progress index. Detailed evidence, experiments, and decisions live in the linked documents and must not be duplicated here.

## Status Model

`queued` -> `active` -> `blocked` | `completed` | `rejected`

An item may be marked `completed` only when its linked exit criteria are satisfied and its evidence is committed.

## Active

| ID | Type | Item | Evidence | Status |
|---|---|---|---|---|
| RGT-D000 | Documentation | Review the v1 documentation baseline and authorize evidence work | `docs/README.md` | active |

## Queue

| ID | Type | Item | Depends on | Evidence |
|---|---|---|---|---|
| RGT-S001 | Competitive spike | Discover and screen comparable open-source systems | RGT-D000 | `docs/spikes/SPIKE-C001-competitive-landscape.md` |
| RGT-S002 | Competitive spikes | Deep-review shortlisted repositories; create one spike result per repository | RGT-S001 | `docs/research/repository-reviews/` |
| RGT-S003 | Spike | Define the representative multi-character animation fixture | RGT-D000 | Planned spike document |
| RGT-S008 | Animation spike | Validate production-grade fixed-cast character orchestration and deterministic frame compilation | RGT-S001, RGT-S003 | `docs/spikes/SPIKE-A001-animation-orchestration.md` |
| RGT-S004 | Renderer spike | Compare qualified production backends with the same fixture | RGT-S008 | `docs/spikes/SPIKE-R001-renderer-backends.md` |
| RGT-S005 | Spike | Measure web-preview and final-render parity | RGT-S004 | Planned spike document |
| RGT-S006 | Spike | Compare Swift-to-engine process and native-library integration | RGT-S004 | Planned spike document |
| RGT-S007 | Agent spike | Validate subscription-hosted operation through MCP | RGT-D000 | Planned spike document |
| RGT-D001 | Decision | Select the primary renderer and integration language | RGT-S004, RGT-S005, RGT-S006 | Planned architecture decision record |
| RGT-D009 | Requirements | Incorporate animation and renderer evidence into validated product requirements | RGT-S008, RGT-D001 | `docs/requirements/product-requirements.md` |

## Completed

| ID | Result | Evidence | Commit |
|---|---|---|---|
| RGT-C001 | Project charter approved | `docs/requirements/charter.md` | `1ca3e47` |
| RGT-D003 | Product requirements v1 drafted | `docs/requirements/product-requirements.md` | `e593958` |
| RGT-D004 | Production contracts v1 drafted | `docs/architecture/production-contracts.md` | `e593958` |
| RGT-D005 | Production pipeline v1 drafted | `docs/architecture/production-pipeline.md` | `e593958` |
| RGT-D006 | Agent system v1 drafted | `docs/architecture/agent-system.md` | `e593958` |
| RGT-D002 | System design v1 drafted | `docs/architecture/system-design.md` | `e593958` |
| RGT-D007 | Quality system v1 drafted | `docs/quality/quality-system.md` | `e593958` |
| RGT-D008 | Deployment and operations v1 drafted | `docs/operations/deployment-and-operations.md` | `e593958` |
| RGT-P001 | Evidence-gated implementation plan v1 drafted | `docs/plans/implementation-plan.md` | `e593958` |

## Tracker Rules

- Every active item must link to a document with explicit exit criteria.
- Spikes remain queued until the production documentation baseline and implementation plan are approved.
- Unknowns remain spikes; they must not be silently converted into architecture decisions.
- Competitive claims must cite an exact repository commit, source path, release, or official document.
- A spike result may recommend, reject, or defer a candidate. It must not force a positive selection.
- Accepted technical choices are recorded once in an architecture decision record and then referenced by the system design.
