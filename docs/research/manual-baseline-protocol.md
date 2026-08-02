# Manual Cutout Baseline Protocol

**Evidence owner:** `SPIKE-W001` Part A (`RGT-S009`).

**Status:** Approved for use by owner decision, 2026-08-02, **with two requirements waived rather than satisfied** (`docs/requirements/charter.md`, Charter Revision 1). The tool class, cast size, and revision behaviour assumed below are owner-selected rather than evidence-confirmed, and scoring is non-blind. Both limitations must appear in any reported result.

**Purpose:** Define, before RigTale exists, how the charter's "at least 50% reduction in hands-on layout and animation time" will be measured. Defining it afterwards would let the threshold be fitted to whatever RigTale happens to achieve.

## Protocol Version

`baseline-protocol/v0.1`. Any change after first use creates a new version and invalidates comparisons made under the previous one.

## What Is Compared

One operator produces the same production twice: once through a documented manual 2D cutout workflow, once through RigTale. Both runs start from the same locked inputs and target the same visible result.

| Locked input | Definition |
|---|---|
| Production brief | The `SPIKE-F001` reference brief, fixed before either run |
| Duration | 150–210 seconds, identical target for both runs |
| Cast | Identical published characters, including one quadruped and one vehicle |
| Assets | Identical layered artwork, backgrounds, props, and motion library |
| Audio | Identical locked audio and lyric timing, where the production uses them |
| Delivery profile | Identical resolution, frame rate, container, and caption requirements |
| Quality bar | Identical acceptance rubric and identical reviewer |

If either run cannot produce a comparable result under these locks, that is recorded as a finding rather than resolved by relaxing a lock for one side.

## Excluded Shared Work

The following is performed once and charged to neither run:

- character design and artwork production;
- layered-file preparation and layer naming;
- rig construction and capability authoring;
- motion library authoring;
- script, lyric, and audio production;
- tool installation and licence acquisition; and
- operator training on either workflow.

Rationale: RigTale's hypothesis is explicitly about the production phase *after* assets are published. Charging asset preparation to the manual side would manufacture a saving RigTale does not create.

**Red-team note:** this exclusion is also the protocol's largest threat to validity. If asset and rig preparation dominates real small-team cost, then a 50% saving in the measured phase may be a small saving in total production cost — and nothing in this project will establish whether it does. The protocol therefore also records total elapsed preparation time as context, even though it is excluded from the headline metric.

## Baseline Fairness Rules

The manual baseline must represent a competent small team, not a handicapped one.

1. The baseline operator uses a production tool that a two-to-five-person cutout studio would realistically use, named and versioned in the run record.
2. The baseline may use every labour-saving feature its tool already provides, including automatic lip sync, symbol and rig reuse, template scenes, motion or action libraries, onion skinning, and copying repeated sections.
3. The baseline operator is competent in that tool. If the operator is not, that is recorded as a validity limitation on the result.
4. The baseline is run first, so knowledge of RigTale's output cannot shape it.
5. The baseline workflow is documented step by step before the run and is not edited during it.

A baseline that ignores features the tool already has does not measure RigTale's value; it measures the tool being used badly.

## Measured Quantities

### Primary metric

**Hands-on layout and animation time.** Human time actively spent on:

- placing characters, props, and backgrounds in a shot;
- setting camera framing and movement;
- selecting, timing, and adjusting motions and poses;
- keyframing, interpolation, and easing adjustments;
- lip sync placement and correction;
- layer ordering, masking, and occlusion fixes; and
- interaction and contact alignment between characters or with props.

### Separately recorded, not in the primary metric

| Quantity | Why separate |
|---|---|
| Scripting and creative authoring time | Both workflows may share it; conflating it hides the automation effect |
| Review time | Human judgement cost, not layout or animation cost |
| Correction time after review | Recorded per round; a workflow that is fast but needs more rounds must not appear cheaper |
| Machine render time | Not human effort; a fast human workflow with slow renders is a different trade |
| Waiting and blocked time | Distinguishes tool latency from human effort |
| Total elapsed wall-clock time | Captures the cost a studio actually schedules around |
| Failure and rework time | Includes crashes, lost work, and re-doing invalidated shots |

Splitting these prevents the most common way this comparison is faked: moving effort out of the "animation" bucket and declaring a saving.

## Time Capture

Time is captured per work session, per shot where practical, using this record:

| Field | Value |
|---|---|
| `run_id` | baseline or rigtale, plus attempt number |
| `protocol_version` | `baseline-protocol/v0.1` |
| `operator` | pseudonymous identifier |
| `tool` | name and exact version |
| `hardware` | machine model, CPU, GPU, RAM |
| `session_start` / `session_end` | ISO-8601 timestamps |
| `shot_id` | fixture shot identifier, or `episode` for whole-production work |
| `activity` | one of the measured categories above |
| `active_minutes` | human active minutes, excluding breaks and machine waits |
| `wait_minutes` | blocked on the machine |
| `round` | review round number, `0` for first pass |
| `notes` | what was done, what failed |
| `evidence` | screen recording reference or saved project version |

Rules:

- Sessions are timed from a recording or a timer, not reconstructed from memory afterwards.
- Any interval longer than five minutes with no recorded activity is excluded from `active_minutes`.
- Self-reported estimates are recorded in a separate field and never substituted for measured time.
- Both runs use the same capture method. A measured RigTale run compared against an estimated manual run is not evidence.

## Completion and Quality Criteria

A run is complete only when its output:

- runs 150–210 seconds and covers the whole brief;
- contains every required shot, cast member, and interaction in the fixture;
- passes the same acceptance rubric used for the other run; and
- is scored by the Project Owner against the written rubric, non-blind.

**Blind review is waived, and the reason it existed has not gone away:** a reviewer who knows the output is RigTale's will not score it the same way. `RGT-O002` is closed by recorded deviation — a solo project with no external participants cannot supply an unaware reviewer.

The protocol's largest bias is therefore uncontrolled. Any reported quality parity between the two runs is an owner self-assessment, and the 50% time result rests on that parity holding. Two mitigations cost nothing and are required: score both runs in randomised order after a delay, and record raw per-criterion scores rather than only the average, so a later reader can re-judge.

If one run fails the quality bar, its time is not comparable and the result is reported as "did not reach comparable quality", never as a time saving.

## Reporting Rules

The result is reported as:

- measured hands-on layout and animation minutes for each run;
- the ratio, with the shot count and revision rounds it covers;
- every separately recorded quantity above;
- validity limitations, including operator skill asymmetry, single-operator sample size, and the excluded preparation work; and
- an explicit statement that a single operator producing one production is a weak sample.

The charter threshold is a pass/fail gate, not a headline. A 50% figure derived from one operator, one production, and one reviewer is preliminary evidence and must be labelled as such.

## Stop Conditions

- Stop if the fixture is not locked before the baseline run begins.
- Stop if the baseline tool cannot use the same published assets, since the comparison would then measure asset conversion rather than production effort.
- Stop and revise if the measured categories cannot be separated cleanly in practice.

## Unverified Assumptions This Protocol Rests On

`RGT-S009B` was to settle these. It was rejected, so they are owner-selected and stay unverified for the life of the project:

- which tool and version a real target studio would use for this production;
- how many review and correction rounds a real production of this length takes;
- what share of total cost is asset and rig preparation versus layout and animation;
- which activities practitioners themselves count as "animation time".

**The core risk is a fifth assumption:** that hands-on time is the cost that actually blocks these teams, rather than elapsed schedule, review latency, or revision risk. The protocol measures the quantity the charter names, which may not be the quantity users care about.
