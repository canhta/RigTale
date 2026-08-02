# SPIKE-W001: Production Workflow and Business Evidence

**Tracker:** `RGT-S009` (Part A, desk research) and `RGT-S009B` (Part B, interviews)

**Status:** Part A complete. **Part B rejected by Project Owner decision, 2026-08-02**, and recorded as `charter.md` Charter Revision 1. This spike is closed. Its Part A findings stand; its Part B questions are permanently unanswered.

## Part A Result

Evidence locations: `docs/research/small-studio-workflow.md` (workflow map, gate evidence status, ranked problems) and `docs/research/manual-baseline-protocol.md` (comparison protocol and time-capture template).

### Exit criteria

| Criterion | Result |
|---|---|
| Every claim distinguishes documented fact, practitioner report, inference, and hypothesis | Met — every statement carries an explicit label |
| Each pipeline gate carries an explicit evidence status | Met |
| Manual comparison protocol is reproducible and does not advantage RigTale | Met, with bias controls that allow the baseline every labour-saving feature its tools already provide |
| Problems only interviews can settle are named as such | Met — `docs/research/small-studio-workflow.md` section 11 |
| No user-behaviour claim presented as established | Met |

### Three results that change the product's evidence position

1. **No published time or cost baseline exists for small-team 2D cutout production.** Both candidate external sources were retrieved and both fail to supply one: the academic paper is an uncontrolled single case in a different technique, and the union agreement prices labour without rating output — since January 2025 it contains no footage-per-day standard at all. **The charter's 50% reduction claim is therefore currently unfalsifiable.** This is a business risk independent of whether the claim is true, and it is the reason the baseline protocol must run before the claim is used.

2. **The unautomated residue is smaller than assumed.** Cutout as a technique already claims the time saving; in-betweening, motion reuse, and lip sync are commodity features; and one vendor already auto-exports storyboard scenes into the animation tool with panels, soundtrack, and camera moves. The addressable segment may be users of tools that lack that integration.

3. **No source documents the approval-gate model of a two-to-five-person team.** `PR-F002` therefore stays `hypothesis` and cannot be promoted by desk research. This is the largest single gap and it sits on a core design decision.

### Constraints added to downstream design

Recorded in `docs/research/small-studio-workflow.md` section 13. The technical ones affect `PR-O03`, `PR-Q004`, `PR-F003`, `SPIKE-A001`, `SPIKE-A002`, and `SPIKE-CS001`. Two business constraints — narrative differentiation requirements and made-for-kids monetisation limits on the dominant platform — are raised for the Project Owner. **No charter revision is proposed.**

### What Part A could not establish

Measured time data, a small-team gate model, a cutout-specific stage ranking, and any localisation workflow. All were routed to Part B. **Part B was rejected by owner decision on 2026-08-02, so all four remain permanently unestablished.**

## Execution Split

This spike has two parts because they have different authorizations and different evidence strength.

| Part | Tracker | Scope | Blocking condition |
|---|---|---|---|
| A | `RGT-S009` | Source-cited workflow map, gate evidence status, manual comparison protocol, time-capture template, ranked problem hypotheses | none — complete |
| B | `RGT-S009B` | Five qualifying problem interviews and privacy-safe synthesis | **rejected by owner decision, 2026-08-02** |

Part A cannot substitute for Part B. Desk research establishes what published sources document about the tool-supported workflow; it cannot establish what a specific small team actually does, what it spends time on, or what it would change.

**Part B will not be run.** The Project Owner is the sole decision-maker and implementer and will conduct no interviews or evaluations with external participants. Charter Objective 5 required the five interviews, so this was recorded as an explicit charter revision rather than an evidence-state transition; see `docs/requirements/charter.md`, Charter Revision 1.

**Every Part A output describing user behaviour therefore stays a hypothesis for the life of the project.** Do not read Part A's labelled desk research as validated user evidence.

## Question

Which real small-studio workflow, artifact handoffs, approval gates, cost drivers, and revision problems must RigTale preserve or improve, and how will business value be measured before major technical investment?

## Why This Requires Evidence

The current pipeline is a normalized hypothesis assembled from public production references and product reasoning. It is not a verified internal workflow for any referenced studio. Without target-user evidence, RigTale could automate low-value steps, create impractical gates, or measure time savings against an unrealistic baseline.

## Research Scope

Desk research only. Interviews are out of scope; see the Execution Split below.

- Independent creators and animation studios of approximately two to five people.
- Children's music and educational animation using reusable characters and assets.
- Brief, script, audio, storyboard, animatic, asset publication, layout, animation, review, render, delivery, reuse, and localization handoffs.
- Manual 2D cutout production using the same class of published assets targeted by RigTale.
- Failure, revision, approval, and archival work that feature lists usually omit.

## Method

1. Review primary production-pipeline documentation and source material without claiming undocumented studio internals.
2. Capture documented inputs, outputs, tools, roles, gates, rework loops, bottlenecks, and exceptions.
3. Define a comparable manual cutout workflow using the same intended reference assets and production brief.
4. Specify how hands-on layout, animation, review, correction, rendering, and total elapsed time will be recorded.
5. Rank problems by frequency, severity, and fit with structured fixed-cast automation.
6. Update product requirements, pipeline stages, fixture design, business metrics, and non-goals from evidence.

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
- Ranked candidate user problems, each with the evidence that would confirm or refute it.
- Explicit list of questions desk research cannot answer.

### Part B (`RGT-S009B`) — not produced

Rejected by owner decision, 2026-08-02. No interview records, no validated gate model, no confirmed problem ranking, and no go/revise/stop recommendation exist. Consequences:

- `PR-F002` is permanently `hypothesis`.
- The problem ranking in `docs/research/small-studio-workflow.md` section 10 keeps its `[FACT]`, `[UNKNOWN]`, and `[HYPOTHESIS]` labels as final.
- The fixed-cast premise is first exercised by the owner-operated reference production, after implementation rather than before it.

## Exit Criteria

### Part A

- Every workflow claim distinguishes documented fact, practitioner report, inference, and hypothesis.
- Each pipeline gate carries an explicit evidence status rather than an implied one.
- The manual comparison protocol is reproducible and does not advantage RigTale artificially.
- Problems that only interviews can settle are named as such.
- No user-behaviour claim is presented as established.

### Part B — waived, not met

The Part B exit criteria are recorded as unmet. Fixture priorities will reflect documented and hypothesised failures plus owner judgement rather than observed ones, and `RGT-D010` and `RGT-D012` now proceed without user-value evidence. That is the largest change caused by Charter Revision 1.

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

Part B gates nothing, because it will not be produced. This list is exhaustive.

| Items | Gating |
|---|---|
| `RGT-S003`, `RGT-S002`, `RGT-S010`, `RGT-S011` | May proceed. They gather technical evidence rather than commit to an architecture. |
| `RGT-S012`, `RGT-S013`, `RGT-S004`, `RGT-D001`, `RGT-S005`, `RGT-S006`, `RGT-D015` | May proceed after the fixture is approved. |
| `RGT-S008` | May proceed on desk research. `SPIKE-A001` requires that this spike has *validated* production workflow and user priorities; nothing will validate them, so `SPIKE-A001` must record that its precondition was met by charter revision, not by evidence. |
| `RGT-D010`, `RGT-D012`, `RGT-D009` | May proceed **without user-value evidence**. Each resulting decision record must state that limitation in its own text. |
| `RGT-S007`, `RGT-D011`, `RGT-D013`, `RGT-D014` | Gated transitively through `RGT-D009` and `RGT-D013`. |

`SPIKE-F001` names "target-user workflow, gate, and value evidence" as a precondition of fixture approval, and Part B was the only route to the second and third. That precondition is now met by owner judgement over desk research. `RGT-O001` is the sole remaining blocker on fixture approval.
