# RigTale Work Tracker

This file is the canonical progress index. Detailed evidence, experiments, and decisions live in the linked documents and must not be duplicated here.

## Status Model

`queued` -> `active` -> `blocked` | `completed` | `rejected`

An item may be marked `completed` only when its linked exit criteria are satisfied and its evidence is committed.

## Active

| ID | Type | Item | Evidence | Status |
|---|---|---|---|---|
| RGT-D000 | Documentation | Complete and approve the production documentation baseline | `docs/README.md` | active |

## Queue

| ID | Type | Item | Depends on | Evidence |
|---|---|---|---|---|
| RGT-D003 | Requirements | Define product workflows, capabilities, and acceptance criteria | RGT-D000 | `docs/requirements/product-requirements.md` |
| RGT-D004 | Contracts | Define the canonical production model and versioned contracts | RGT-D003 | `docs/architecture/production-contracts.md` |
| RGT-D005 | Pipeline design | Define asset ingestion, rigging, animation, audio, and rendering flow | RGT-D004 | `docs/architecture/production-pipeline.md` |
| RGT-D006 | Agent design | Define Development, Studio, and Red-Team agents plus MCP boundaries | RGT-D004 | `docs/architecture/agent-system.md` |
| RGT-D002 | System design | Define stable architecture, integration seams, and deferred decisions | RGT-D004, RGT-D005, RGT-D006 | `docs/architecture/system-design.md` |
| RGT-D007 | Quality design | Define validation, review, quality gates, and production acceptance | RGT-D002 | `docs/quality/quality-system.md` |
| RGT-D008 | Operations | Define local operation, cloud evolution, security, recovery, and observability | RGT-D002 | `docs/operations/deployment-and-operations.md` |
| RGT-P001 | Plan | Produce the implementation plan with explicit research gates | RGT-D007, RGT-D008 | `docs/plans/implementation-plan.md` |
| RGT-S001 | Competitive spike | Discover and screen comparable open-source systems | RGT-P001 | `docs/spikes/SPIKE-C001-competitive-landscape.md` |
| RGT-S002 | Competitive spikes | Deep-review shortlisted repositories; create one spike result per repository | RGT-S001 | `docs/research/repository-reviews/` |
| RGT-S003 | Spike | Define the representative multi-character animation fixture | RGT-P001 | Planned spike document |
| RGT-S004 | Renderer spike | Compare qualified production backends with the same fixture | RGT-S003 | `docs/spikes/SPIKE-R001-renderer-backends.md` |
| RGT-S005 | Spike | Measure web-preview and final-render parity | RGT-S004 | Planned spike document |
| RGT-S006 | Spike | Compare Swift-to-engine process and native-library integration | RGT-S004 | Planned spike document |
| RGT-S007 | Agent spike | Validate subscription-hosted operation through MCP | RGT-P001 | Planned spike document |
| RGT-D001 | Decision | Select the primary renderer and integration language | RGT-S004, RGT-S005, RGT-S006 | Planned architecture decision record |

## Completed

| ID | Result | Evidence | Commit |
|---|---|---|---|
| RGT-C001 | Project charter approved | `docs/requirements/charter.md` | `1ca3e47` |

## Tracker Rules

- Every active item must link to a document with explicit exit criteria.
- Spikes remain queued until the production documentation baseline and implementation plan are approved.
- Unknowns remain spikes; they must not be silently converted into architecture decisions.
- Competitive claims must cite an exact repository commit, source path, release, or official document.
- A spike result may recommend, reject, or defer a candidate. It must not force a positive selection.
- Accepted technical choices are recorded once in an architecture decision record and then referenced by the system design.
