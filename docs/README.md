# RigTale Documentation Map

This map defines the minimum non-overlapping documentation set required before research spikes or product implementation begin. Documents describe durable product intent, contracts, and boundaries. Unknown technology choices remain explicit spike or decision items.

## Documentation Order

| Order | Document | Owns | State |
|---:|---|---|---|
| 1 | `requirements/charter.md` | Business justification, vision, scope, constraints, and go/no-go criteria | approved |
| 2 | `requirements/product-requirements.md` | User workflows, product capabilities, non-functional requirements, and acceptance criteria | planned |
| 3 | `architecture/production-contracts.md` | Canonical production objects, schemas, lifecycle, versioning, and compatibility | planned |
| 4 | `architecture/production-pipeline.md` | Asset ingestion, rig preparation, scripting, animation, audio, preview, and final rendering | planned |
| 5 | `architecture/agent-system.md` | Development, Studio, and Red-Team agent responsibilities, tools, MCP, context, and failure boundaries | planned |
| 6 | `architecture/system-design.md` | Component topology, execution modes, integration seams, storage, jobs, and deferred technical decisions | planned |
| 7 | `quality/quality-system.md` | Automated validation, red-team review, visual and temporal quality, and production gates | planned |
| 8 | `operations/deployment-and-operations.md` | macOS operation, CLI, future cloud service, security, observability, recovery, and upgrades | planned |
| 9 | `plans/implementation-plan.md` | Build order, test strategy, dependencies, research gates, and production-readiness milestones | planned |

## Supporting Records

- `research/` stores evidence plans and candidate indexes; it does not select technology.
- `spikes/` defines reproducible experiments and later records their results.
- `decisions/` is created only when evidence supports an accepted technical choice.
- `TODO.md` tracks status and dependencies without duplicating document content.
- Stable development workflows may be extracted into agent skills only after the underlying workflow has been implemented and verified.

## Completion Rule

The documentation baseline is complete when every planned document above:

1. has no silent assumptions or unresolved contradictions;
2. routes material unknowns to a named spike or decision item;
3. defines testable interfaces, requirements, or exit criteria;
4. agrees with the charter and the other documents; and
5. is approved before its dependent document is written.

Renderer, server language, cloud infrastructure, and hosted model-provider choices are intentionally not selected during documentation. The design must preserve their integration boundaries, while the implementation plan must block dependent work on the relevant evidence and decision records.
