# RigTale Evidence and Research Plan

## Purpose

RigTale will choose its production architecture from reproducible evidence rather than familiarity, popularity, or README claims. Research must cover both production backends and comparable products or open-source workflows.

## Evidence Types

1. **Primary documentation** establishes supported features, interfaces, platform constraints, and licensing claims.
2. **Repository inspection** establishes how a system is actually structured, tested, packaged, and maintained.
3. **Executable spikes** establish whether a candidate satisfies a RigTale production requirement with a representative fixture.
4. **Architecture decision records** capture accepted choices only after relevant evidence exists.

Search results, marketing pages, and generated summaries may identify candidates but are not sufficient evidence for a technical decision.

## Competitive Evidence Workflow

1. Discover candidates through official sites, GitHub, Product Hunt, papers, and targeted web search.
2. Verify the canonical repository, license, release history, recent activity, and documentation.
3. Screen candidates against RigTale's actual production model before spending time on a deep review.
4. Create a dedicated review record for every shortlisted repository.
5. Clone the exact revision into `.research/clones/<repository>` and record its commit SHA. The ignored research workspace is local-only and external clones are never committed into RigTale.
6. Inspect source layout, contracts, renderer boundaries, asset model, agent instructions, tests, examples, packaging, and failure handling.
7. Keep `SPIKE-C001` read-only. Execute candidate code only in a later fixture-based repository review or technical spike after its preconditions are approved. Treat third-party setup scripts as untrusted and run them without project secrets.
8. Record strengths, weaknesses, reusable patterns, rejected patterns, and unresolved questions with file-level evidence.

## Production-Backend Spike Workflow

1. Define one versioned fixture and expected output before implementing any backend adapter.
2. Compile the same RigTale production contracts into every qualified backend.
3. Measure output quality, controllability, determinism, preview parity, performance, packaging, deployment, and maintenance cost.
4. Reject candidates that require UI automation, flatten editable production state, silently ignore unsupported actions, or create incompatible license obligations.
5. Select a primary backend only through an architecture decision record.

## Repository Review Record

Every deep review must include:

- Repository URL, exact commit SHA, release, and license.
- Project purpose and production model.
- Relevant directories and execution entry points.
- Data contracts and intermediate representations.
- Asset, timeline, rendering, and agent architecture.
- Test strategy and observable quality evidence.
- What RigTale can reuse or learn.
- What RigTale must avoid.
- Open questions and required executable tests.
- A conclusion: `adopt`, `adapt`, `reference`, `reject`, or `defer`.

## Decision Discipline

- Research findings do not modify the approved charter.
- A candidate remains unselected until its required spike passes.
- Missing evidence is written as a tracked spike, not filled with an assumption.
- The work tracker records status; research and spike files hold evidence; decision records hold accepted choices. The system design distinguishes approved product constraints, provisional integration boundaries, deferred decisions, and ADR-backed selected architecture.
