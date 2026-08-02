# RigTale Work Tracker

This file is the canonical progress index. Detailed evidence, experiments, and decisions live in the linked documents and must not be duplicated here.

## Status Model

`queued` -> `active` -> `blocked` | `completed` | `rejected`

An item may be marked `completed` only when its linked exit criteria are satisfied and its evidence is committed.

## Active

| ID | Type | Item | Evidence | Status |
|---|---|---|---|---|
| RGT-S001 | Competitive spike | Discover and screen comparable open-source systems | `docs/spikes/SPIKE-C001-competitive-landscape.md` | active |

## Queue

| ID | Type | Item | Depends on | Evidence |
|---|---|---|---|---|
| RGT-S002 | Competitive spikes | Deep-review shortlisted repositories; create one spike result per repository | RGT-S001 | `docs/research/repository-reviews/` |
| RGT-S003 | Spike | Define the representative multi-character animation fixture | RGT-S001 | Planned spike document |
| RGT-S004 | Renderer spike | Compare qualified production backends with the same fixture | RGT-S003 | `docs/spikes/SPIKE-R001-renderer-backends.md` |
| RGT-S005 | Spike | Measure web-preview and final-render parity | RGT-S004 | Planned spike document |
| RGT-S006 | Spike | Compare Swift-to-engine process and native-library integration | RGT-S004 | Planned spike document |
| RGT-S007 | Agent spike | Validate subscription-hosted operation through MCP | RGT-S001 | Planned spike document |
| RGT-D001 | Decision | Select the primary renderer and integration language | RGT-S004, RGT-S005, RGT-S006 | Planned architecture decision record |
| RGT-D002 | Design | Complete and approve the system design | RGT-D001, RGT-S007 | `docs/architecture/system-design.md` |
| RGT-P001 | Plan | Produce the implementation plan from the approved design | RGT-D002 | Planned implementation plan |

## Completed

| ID | Result | Evidence | Commit |
|---|---|---|---|
| RGT-C001 | Project charter approved | `docs/requirements/charter.md` | `1ca3e47` |

## Tracker Rules

- Every active item must link to a document with explicit exit criteria.
- Unknowns remain spikes; they must not be silently converted into architecture decisions.
- Competitive claims must cite an exact repository commit, source path, release, or official document.
- A spike result may recommend, reject, or defer a candidate. It must not force a positive selection.
- Accepted technical choices are recorded once in an architecture decision record and then referenced by the system design.

