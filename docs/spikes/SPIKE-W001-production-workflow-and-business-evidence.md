# SPIKE-W001: Production Workflow and Business Evidence

**Tracker:** `RGT-S009` (Part A, desk research) and `RGT-S009B` (Part B, interviews)

**Status:** Part A complete. Part B blocked pending Project Owner authorization to contact participants.

## Part A Result

Evidence locations: `docs/research/small-studio-workflow.md` (workflow map, gate evidence status, ranked problems, interview questions) and `docs/research/manual-baseline-protocol.md` (comparison protocol and time-capture template).

### Exit criteria

| Criterion | Result |
|---|---|
| Every claim distinguishes documented fact, practitioner report, inference, and hypothesis | Met — every statement carries an explicit label |
| Each pipeline gate carries an explicit evidence status | Met |
| Manual comparison protocol is reproducible and does not advantage RigTale | Met, with bias controls that allow the baseline every labour-saving feature its tools already provide |
| Problems only interviews can settle are named and routed to Part B | Met — eleven questions |
| No user-behaviour claim presented as established | Met |

### Three results that change the product's evidence position

1. **No published time or cost baseline exists for small-team 2D cutout production.** Both candidate external sources were retrieved and both fail to supply one: the academic paper is an uncontrolled single case in a different technique, and the union agreement prices labour without rating output — since January 2025 it contains no footage-per-day standard at all. **The charter's 50% reduction claim is therefore currently unfalsifiable.** This is a business risk independent of whether the claim is true, and it is the reason the baseline protocol must run before the claim is used.

2. **The unautomated residue is smaller than assumed.** Cutout as a technique already claims the time saving; in-betweening, motion reuse, and lip sync are commodity features; and one vendor already auto-exports storyboard scenes into the animation tool with panels, soundtrack, and camera moves. The addressable segment may be users of tools that lack that integration.

3. **No source documents the approval-gate model of a two-to-five-person team.** `PR-F002` therefore stays `hypothesis` and cannot be promoted by desk research. This is the largest single gap and it sits on a core design decision.

### Constraints added to downstream design

Recorded in `docs/research/small-studio-workflow.md` section 13. The technical ones affect `PR-O03`, `PR-Q004`, `PR-F003`, `SPIKE-A001`, `SPIKE-A002`, and `SPIKE-CS001`. Two business constraints — narrative differentiation requirements and made-for-kids monetisation limits on the dominant platform — are raised for the Project Owner. **No charter revision is proposed.**

### What Part A could not establish

Measured time data, a small-team gate model, a cutout-specific stage ranking, and any localisation workflow. All are routed to Part B.

## Execution Split

This spike has two parts because they have different authorizations and different evidence strength.

| Part | Tracker | Scope | Blocking condition |
|---|---|---|---|
| A | `RGT-S009` | Source-cited workflow map, gate evidence status, manual comparison protocol, time-capture template, interview instrument, ranked problem hypotheses | none |
| B | `RGT-S009B` | Five qualifying problem interviews and privacy-safe synthesis | Project Owner must authorize participant contact |

Part A cannot substitute for Part B. Desk research establishes what published sources document about the tool-supported workflow; it cannot establish what a specific two-to-five-person team actually does, what it actually spends time on, or what it would actually change. Every Part A output that describes user behaviour is a hypothesis until Part B tests it.

Charter Objective 5 requires the five interviews. Part B therefore carries a charter obligation and cannot be waived by an evidence-state transition.

## Question

Which real small-studio workflow, artifact handoffs, approval gates, cost drivers, and revision problems must RigTale preserve or improve, and how will business value be measured before major technical investment?

## Why This Requires Evidence

The current pipeline is a normalized hypothesis assembled from public production references and product reasoning. It is not a verified internal workflow for any referenced studio. Without target-user evidence, RigTale could automate low-value steps, create impractical gates, or measure time savings against an unrealistic baseline.

## Research Scope

- Independent creators and animation studios of approximately two to five people.
- Children's music and educational animation using reusable characters and assets.
- Brief, script, audio, storyboard, animatic, asset publication, layout, animation, review, render, delivery, reuse, and localization handoffs.
- Manual 2D cutout production using the same class of published assets targeted by RigTale.
- Failure, revision, approval, and archival work that feature lists usually omit.

## Method

1. Review primary production-pipeline documentation and source material without claiming undocumented studio internals.
2. Conduct at least five problem interviews with target creators or small-studio practitioners.
3. Capture current inputs, outputs, tools, roles, gates, rework loops, bottlenecks, and exceptions.
4. Define a comparable manual cutout workflow using the same intended reference assets and production brief.
5. Specify how hands-on layout, animation, review, correction, rendering, and total elapsed time will be recorded.
6. Rank problems by frequency, severity, willingness to change workflow, and fit with structured fixed-cast automation.
7. Review the proposed RigTale artifact and gate model with interview participants without presenting it as a completed product.
8. Update product requirements, pipeline stages, fixture design, business metrics, and non-goals from evidence.

## Interview Evidence

Each record must include participant profile, workflow context, production scale, source artifacts, observed or reported steps, bottlenecks, revision examples, current time or cost estimates, confidence, and permission level for retained notes. Personally identifying or confidential production data must not enter the public repository without explicit consent.

## Manual Baseline

The comparison method must lock:

- production brief, duration, cast, source assets, motions, scenes, and delivery profile;
- which preparation work is shared by both workflows;
- which human actions count as layout or animation time;
- review and correction rounds;
- machine render time versus hands-on time; and
- visible-quality and completion criteria.

The baseline method is approved early; measurement of RigTale's hands-on result occurs later when a usable vertical exists.

## Required Outputs

### Part A (`RGT-S009`)

- Source-cited workflow map for tool-supported 2D cutout production, with an evidence label on every line.
- Evidence status for every pipeline gate: documented, practitioner-reported, or RigTale hypothesis.
- Comparable manual-workflow protocol and time-capture template.
- Interview instrument, screening criteria, consent model, and retention rules.
- Ranked candidate user problems, each with the evidence that would confirm or refute it.
- Explicit list of questions desk research cannot answer.

### Part B (`RGT-S009B`)

- At least five problem-interview records and a privacy-safe synthesis.
- Validated artifact handoff and approval-gate recommendations.
- Confirmed or refuted problem ranking, and explicit product non-problems.
- Early go, revise, or stop recommendation for the fixed-cast production hypothesis.
- Updates to charter only if scope evidence requires owner approval; otherwise updates to requirements, pipeline, fixture, quality, and plan.

## Exit Criteria

### Part A

- Every workflow claim distinguishes documented fact, practitioner report, inference, and hypothesis.
- Each pipeline gate carries an explicit evidence status rather than an implied one.
- The manual comparison protocol is reproducible and does not advantage RigTale artificially.
- Problems that only interviews can settle are named as such and routed to Part B.
- No user-behaviour claim is presented as established.

### Part B

- Five qualifying problem interviews are complete.
- Fixture priorities reflect frequent and costly real production failures.
- Major technical selection has not begun before this evidence is reviewed.

## Bias Controls

The manual baseline is defined before RigTale can be measured, and it must not be constructed to lose:

- The baseline operator uses the tool class that a real small team would use, not a deliberately weak one.
- The baseline is allowed every labour-saving feature its tools already provide, including automatic lip sync, motion or template libraries, symbol and rig reuse, and copy-paste of repeated sections.
- Shared preparation work is excluded from both sides rather than charged to the baseline.
- Machine render time is recorded separately from hands-on time.
- If existing tools already remove most of the repetitive work RigTale intends to automate, that is a finding, not a measurement error.

## Later Validation

The charter's two hands-on production evaluations remain in the production-evaluation phase after a usable vertical exists. They reuse the approved baseline protocol rather than redefining success after implementation.

## Downstream Gating

This list is exhaustive. Every tracker item must appear in exactly one row.

| Items | Gating |
|---|---|
| `RGT-S003`, `RGT-S002`, `RGT-S010`, `RGT-S011` | **May proceed on Part A**, because they gather technical evidence rather than commit to an architecture. |
| `RGT-S012`, `RGT-S013`, `RGT-S004`, `RGT-D001`, `RGT-S005`, `RGT-S006`, `RGT-D015` | **May proceed on Part A**, but only after the fixture is approved. They inherit Part B indirectly through fixture approval, not directly. |
| `RGT-S008` | **Requires Part B.** `SPIKE-A001` states as a precondition that `SPIKE-W001` has *validated* production workflow and user priorities. Part A validated nothing; it recorded labelled desk research. |
| `RGT-D010`, `RGT-D012`, `RGT-D009` | **Require Part B**, because they convert evidence into an accepted product architecture and would otherwise be selected without user-value evidence. |
| `RGT-S007`, `RGT-D011`, `RGT-D013`, `RGT-D014` | Gated transitively through `RGT-D009` and `RGT-D013`. |

**Approval of `RGT-S003` also requires Part B**, even though drafting does not. `SPIKE-F001` names "target-user workflow, gate, and value evidence" as a precondition, and Part B exit criteria require that fixture priorities reflect real production failures. An earlier version of this section listed `RGT-S003` as Part-A-eligible without that distinction, and `TODO.md` propagated the looser reading.
