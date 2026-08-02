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
| RGT-S009 | Workflow spike | Validate small-studio workflow, user problems, and manual business baseline | RGT-D000 | `docs/spikes/SPIKE-W001-production-workflow-and-business-evidence.md` |
| RGT-S001 | Competitive spike | Discover and screen comparable open-source systems | RGT-D000 | `docs/spikes/SPIKE-C001-competitive-landscape.md` |
| RGT-S003 | Fixture spike | Define the representative multi-character production fixture | RGT-S001, RGT-S009 | `docs/spikes/SPIKE-F001-reference-production-fixture.md` |
| RGT-S002 | Competitive spikes | Deep-review shortlisted repositories using approved fixture cases | RGT-S001, RGT-S003 | `docs/research/repository-reviews/` |
| RGT-S010 | Asset spike | Validate layered-asset ingestion and rig publication | RGT-S001, RGT-S003 | `docs/spikes/SPIKE-A002-asset-ingestion-and-rig-authoring.md` |
| RGT-S008 | Orchestration research | Compare and prototype renderer-independent orchestration contracts | RGT-S002, RGT-S003, RGT-S010 | `docs/spikes/SPIKE-A001-animation-orchestration.md` |
| RGT-S004 | Production-engine spike | Execute shortlisted orchestration and renderer pairings | RGT-S008 | `docs/spikes/SPIKE-R001-renderer-backends.md` |
| RGT-S005 | Preview spike | Measure preview and final-render parity | RGT-S004 | `docs/spikes/SPIKE-R002-preview-final-parity.md` |
| RGT-S006 | Integration spike | Compare Swift-to-renderer integration boundaries | RGT-S004, RGT-S005 | `docs/spikes/SPIKE-I001-swift-renderer-integration.md` |
| RGT-S007 | Agent spike | Validate MCP host-operated and embedded-agent execution | RGT-D000 | `docs/spikes/SPIKE-M001-mcp-and-embedded-agent-execution.md` |
| RGT-D001 | Decision | Select the orchestration model and primary renderer | RGT-S004 | Planned architecture decision records |
| RGT-D010 | Decision | Select preview and Swift-renderer integration boundaries | RGT-S005, RGT-S006 | Planned architecture decision records |
| RGT-D011 | Decision | Select MCP and embedded-agent execution strategy | RGT-S007 | Planned architecture decision records |
| RGT-D012 | Decision | Select core languages, contract tooling, and local storage baseline | RGT-S001, RGT-D001, RGT-D010 | Planned architecture decision records |
| RGT-D009 | Requirements | Incorporate accepted evidence into validated product requirements | RGT-S009, RGT-S010, RGT-D001, RGT-D010, RGT-D012 | `docs/requirements/product-requirements.md` |

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
