# RigTale Agent System

**Status:** v1 draft.

## Purpose

This document defines how agents participate in repository development and video production while deterministic software retains control of validation, compilation, rendering, storage, and recovery.

## Agent Set

### Development Agent

Supports the Project Owner in building RigTale. It researches claims, maintains requirements and plans, implements and tests the repository, reviews changes, and protects the reference-production goal. It is not deployed as part of the video production runtime.

Repeated, verified development workflows may later become focused skills. Skills must not embed unvalidated architectural assumptions.

### Studio Agent

Owns the creative production loop. It may research a subject, prepare or revise script and lyrics, build scene intent, select published assets, produce semantic shot and choreography instructions, inspect structured validation, and revise affected artifacts.

It does not generate final frames, mutate published assets, write arbitrary engine scripts into an episode, or bypass blocking validation.

### Red-Team Agent

Reviews creative artifacts, production plans, previews, and final candidates independently. It checks factual accuracy, audience safety, brief alignment, asset capability, continuity, pacing, framing, occlusion, interaction, synchronization, repetition, and visible output quality.

It returns structured findings and never modifies the reviewed artifacts directly.

## Deterministic Tool Boundary

Agents operate only through typed tools backed by production services. Candidate tool families are:

- project and artifact read/write/version tools;
- research and source-evidence tools;
- asset search, inspection, compatibility, and publication tools;
- script, timing, scene, shot, and choreography authoring tools;
- deterministic validation and compilation tools;
- preview, render, media inspection, and comparison tools;
- finding, approval, correction, and delivery tools.

Every mutating tool validates its input, records actor and source references, is idempotent or has an idempotency key, and returns a structured artifact or error. Raw filesystem and unrestricted shell access are development conveniences, not production-agent interfaces.

## Production Loop

```text
read current production state
-> identify the next unmet gate
-> propose or create one bounded artifact change
-> run deterministic validation
-> inspect structured findings and relevant preview media
-> revise or request user approval
-> publish the approved artifact
-> continue until delivery gates pass
```

The loop is artifact-driven. A new agent session can resume from stored state without replaying an entire conversation.

## Context and Memory

- The current brief, selected artifact versions, unresolved findings, and gate state form the minimum task context.
- Large scripts, asset catalogs, and histories are retrieved by ID and section, not injected wholesale.
- Decisions and approvals live in artifacts, not model memory.
- Agent summaries are non-authoritative and must link back to source artifacts.
- Every run records provider, model class where available, tool calls, token or cost measurements, retries, and produced artifact versions without storing hidden reasoning.

Exact context budgets and model routing require operational evidence.

## Planning Constraints

- Agent plans may reference only published assets or explicit placeholders that block compilation.
- Capability queries precede action selection.
- The Studio Agent must report when the available cast cannot satisfy creative intent.
- Automated repair is bounded by finding type and retry count.
- Repeated deterministic failures stop the loop and request changed input or user direction.
- Creative alternatives must preserve approved facts, audience constraints, and artifact locks.

## Review Independence

The Red-Team Agent receives the approved brief, rubric, target artifacts, rendered evidence, and known constraints. It should not inherit the Studio Agent's persuasive narrative or private scratch context. Its findings contain severity, evidence, location, rationale, and required resolution.

A blocking finding can be resolved only by a revised artifact, a reproducible invalidation of the finding, or an explicit human waiver recorded in the audit trail. The same agent run cannot both author and independently approve a production gate.

## MCP and Host Integration

RigTale should expose production tools through an MCP adapter so a compatible host can operate projects using the user's existing interactive subscription where the host permits it. MCP is a tool transport and does not convert a ChatGPT or Claude subscription into general API credentials.

Two execution modes must remain distinct:

- **Host-operated:** an external agent host invokes RigTale MCP tools under the user's interactive session and approval model.
- **Embedded or unattended:** RigTale runs its own agent loop and requires configured provider credentials or another explicitly supported provider mechanism.

Both modes must use the same typed production tools and artifacts. Subscription availability, host limits, long-running job behavior, and approval UX are evidence-pending under `SPIKE-M001`.

## Provider Adapters

Language, speech, music, alignment, and future generative services sit behind replaceable adapters. Provider output is imported as a versioned artifact with origin, model or service metadata where available, settings, and validation state.

Rendering and approved structured edits must continue when all AI providers are unavailable. Provider failure may block new creative authoring, but it must not corrupt or make existing productions unreadable.

## Safety and Security

- Production tools receive scoped project and artifact identifiers.
- Secrets are resolved by the host or secret store and never embedded in artifacts or logs.
- Imported text and assets are untrusted data, not agent instructions.
- Research content cannot authorize tool calls or override production policies.
- File paths, URLs, media decoders, and third-party project files require validation and isolation.
- Cost, time, tool-call, and retry budgets are enforced outside model output.
- Destructive actions and approval waivers require explicit user confirmation.

## Failure Handling

| Failure | Required behavior |
|---|---|
| Invalid agent output | Reject against schema and return localized repair feedback. |
| Unsupported action | Return capability evidence and safe alternatives; never fake success. |
| Repeated repair loop | Stop at the configured limit and preserve attempts. |
| Provider outage | Preserve production state and allow deterministic work to continue. |
| Tool timeout | Return attempt ID and resumable status where applicable. |
| Conflicting approvals | Block downstream publication and request resolution. |
| Unsafe or unlicensed input | Quarantine the artifact and create a blocking finding. |

## Agent Evaluation

Evaluation uses versioned production fixtures, not subjective chat transcripts. Measures include:

- valid-artifact rate on first submission and after repair;
- unsupported-action request rate;
- number and severity of Red-Team findings;
- unnecessary shot or asset churn;
- tool calls, context volume, time, and provider cost;
- recovery from interrupted sessions; and
- visible quality and editability of the resulting production.

## Evidence Required

- `SPIKE-W001` for real workflow gates, user interventions, and value priorities.
- `SPIKE-C001` and fixture-based repository reviews for proven agent-production patterns.
- `SPIKE-A001` for the correct semantic control boundary.
- `SPIKE-M001` for MCP host-operated behavior, embedded execution, and subscription constraints.
- Full-production evaluations for context, retry, cost, and review effectiveness.

Accepted model providers, agent frameworks, context limits, and orchestration libraries require separate decisions after evidence.
