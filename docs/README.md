# RigTale Documentation Map

This map defines the minimum non-overlapping documentation set required before research spikes or product implementation begin. Documents first establish a coherent draft of product intent, contracts, and boundaries. Research and spikes then replace working hypotheses with evidence-backed requirements and decisions.

## Document Lifecycle

`planned` -> `v1 draft` -> `validated`

- `v1 draft` means the document is coherent enough to expose assumptions, dependencies, and evidence gaps before research begins.
- `validated` means the relevant research and spike evidence has been incorporated and accepted choices are recorded in decision records.
- The project charter follows a separate owner-governed lifecycle: `draft` -> `approved`. Changing approved business scope requires an explicit charter revision rather than an evidence-state transition.
- `charter-backed`, `hypothesis`, and `decision-pending` classify individual requirements inside a document; they are not document lifecycle states.

## Documentation Order

| Order | Document | Owns | State |
|---:|---|---|---|
| 1 | `requirements/charter.md` | Business justification, vision, scope, constraints, and go/no-go criteria | approved |
| 2 | `requirements/product-requirements.md` | User workflows, product capabilities, non-functional requirements, and acceptance criteria | v1 draft |
| 3 | `architecture/production-contracts.md` | Canonical production objects, schemas, lifecycle, versioning, and compatibility | v1 draft |
| 4 | `architecture/production-pipeline.md` | Asset ingestion, rig preparation, scripting, animation, audio, preview, and final rendering | v1 draft |
| 5 | `architecture/agent-system.md` | Development, Studio, and Red-Team agent responsibilities, tools, MCP, context, and failure boundaries | v1 draft |
| 6 | `architecture/system-design.md` | Component topology, execution modes, integration seams, storage, jobs, and deferred technical decisions | v1 draft |
| 7 | `quality/quality-system.md` | Automated validation, red-team review, visual and temporal quality, and production gates | v1 draft |
| 8 | `operations/deployment-and-operations.md` | macOS operation, CLI, future cloud service, security, observability, recovery, and upgrades | v1 draft |
| 9 | `plans/implementation-plan.md` | Build order, test strategy, dependencies, research gates, and production-readiness milestones | v1 draft |

## Supporting Records

- `research/` stores evidence plans and candidate indexes; it does not select technology.
- `spikes/` defines reproducible experiments and later records their results.
- `decisions/` is created only when evidence supports an accepted technical choice.
- `TODO.md` tracks status and dependencies without duplicating document content.
- Stable development workflows may be extracted into agent skills only after the underlying workflow has been implemented and verified.

## Completion Rule

The pre-research documentation baseline is complete when every planned document above:

1. is at least a coherent draft;
2. labels assumptions instead of presenting them as established architecture;
3. routes material unknowns to a named research, spike, or decision item;
4. defines the evidence required to validate uncertain requirements; and
5. agrees with the charter and the other draft documents.

Documents are drafted in dependency order, but downstream drafts may reference explicitly unresolved upstream decisions. After research begins, findings must update the affected requirements, contracts, designs, tests, and plans rather than living only in a spike report.

## Propagation Audit

**The rule above failed its first test.** An independent review of the two completed spikes found that four of their eight material findings never reached a requirement, contract, or plan — including the one the spike itself labelled the sharpest architectural constraint it had found and marked "not deferred." The rule was stated in four documents and executed in none of them.

A propagation audit is therefore a mandatory exit criterion for every spike, not a sentence in this file. Closing a spike requires a table with one row per material finding:

| Column | Meaning |
|---|---|
| Finding | The labelled statement, cited to its source line |
| Target | The exact requirement, contract, design, test, or plan it binds |
| Edit | What changed there, or `none` |
| Commit | Where the edit landed |
| If `none` | An explicit recorded reason, signed off by the Project Owner |

A spike whose findings all land in `Target: none` without recorded reasons is not closed. The four findings that escaped the first audit were: the Music & Effects and textless-picture delivery constraint, the platform monetisation constraint on made-for-kids content, the raster-determinism divergence on Apple platforms, and the licensing obligations of the dependency stack. The first, third, and fourth are now recorded as `PR-F003`, `PR-R007`, and `PR-P005`. The second is an owner decision with no route into any document and remains open.

Renderer, server language, cloud infrastructure, and hosted model-provider choices are intentionally not selected during documentation. The design must preserve their integration boundaries, while the implementation plan must block dependent work on the relevant evidence and decision records.
